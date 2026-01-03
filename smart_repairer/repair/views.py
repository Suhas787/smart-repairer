from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DriverProfile, RepairerProfile, RepairRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
import datetime
import json
# --- NEW IMPORTS FOR YOUR GRAPHS AND RATINGS ---
from django.db.models import Count, Avg, Sum
from django.db.models.functions import ExtractYear
# We do NOT import razorpay

def home(request):
    return render(request, 'repair/home.html')

# --- THIS IS THE NEW VIEW FOR YOUR PUBLIC PAGE ---
def about_us(request):
    
    # 1. Get data for the "Repairs per Year" graph
    yearly_data = RepairRequest.objects.filter(
        status='Completed'
    ).annotate(
        year=ExtractYear('created_at') # Group by year
    ).values(
        'year'
    ).annotate(
        count=Count('id') # Count jobs in that year
    ).order_by('year')
    
    # Format data for Chart.js
    chart_labels = [d['year'] for d in yearly_data]
    chart_data = [d['count'] for d in yearly_data]

    # 2. Get the 5 best/newest reviews
    reviews = RepairRequest.objects.filter(
        status='Completed',
        rating__gte=4, # Get 4 and 5-star reviews
        review_comment__isnull=False # Make sure they wrote a comment
    ).order_by('-created_at')[:5] # Get the 5 newest

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'reviews': reviews
    }
    return render(request, 'repair/about_us.html', context)


# ============================
# REGISTRATION & LOGIN VIEWS
# ============================

def register(request):
    return render(request, 'repair/register.html')

def register_driver(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        vehicle_number = request.POST['vehicle_number']
        phone = request.POST['phone']
        location = request.POST['location']

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register_driver')
        
        try:
            user = User.objects.create_user(username=username, password=pass1)
            DriverProfile.objects.create(
                user=user,
                vehicle_number=vehicle_number,
                phone=phone,
                location=location
            )
            login(request, user)
            messages.success(request, 'Driver account created successfully!')
            return redirect('driver_dashboard')
        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('register_driver')
    
    return render(request, 'repair/register_driver.html')

def register_repairer(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        workshop_name = request.POST['workshop_name']
        service_type = request.POST['service_type']
        phone = request.POST['phone']
        location = request.POST['location']

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register_repairer')

        try:
            user = User.objects.create_user(username=username, password=pass1)
            RepairerProfile.objects.create(
                user=user,
                workshop_name=workshop_name,
                service_type=service_type,
                phone=phone,
                location=location
            )
            login(request, user)
            messages.success(request, 'Repairer account created successfully!')
            return redirect('repairer_dashboard')
        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('register_repairer')
            
    return render(request, 'repair/register_repairer.html')

def login_as_view(request):
    return render(request, 'repair/login_as.html')

def login_form_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['password']
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=passw)

        if user is not None:
            if role == 'driver':
                if hasattr(user, 'driverprofile'):
                    login(request, user)
                    return redirect('driver_dashboard')
                else:
                    messages.error(request, 'This is not a Driver account.')
                    return redirect(f"{reverse('login_form')}?role=driver")
            elif role == 'repairer':
                if hasattr(user, 'repairerprofile'):
                    login(request, user)
                    return redirect('repairer_dashboard')
                else:
                    messages.error(request, 'This is not a Repairer account.')
                    return redirect(f"{reverse('login_form')}?role=repairer")
            else:
                messages.error(request, 'No role was selected. Please go back.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect(f"{reverse('login_form')}?role={role}")
    return render(request, 'repair/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ============================
# DRIVER & "DUMMY" PAYMENT VIEWS
# ============================

@login_required
def create_request(request):
    if request.method == 'POST':
        issue = request.POST['issue_description']
        location_coords = request.POST['location']
        image = request.FILES.get('problem_image', None)
        priority = request.POST['priority']

        amount_in_rupees = 0
        if priority == 'Priority':
            amount_in_rupees = 100
        elif priority == 'Express':
            amount_in_rupees = 250
        
        try:
            driver_profile = request.user.driverprofile
        except DriverProfile.DoesNotExist:
            messages.error(request, 'You must be a driver to make a request.')
            return redirect('home')

        new_request = RepairRequest.objects.create(
            driver=driver_profile,
            issue_description=issue,
            location=location_coords,
            problem_image=image,
            priority=priority,
            status='Unpaid' if amount_in_rupees > 0 else 'Pending'
        )

        if amount_in_rupees > 0:
            messages.info(request, 'Please confirm your premium service payment.')
            return redirect('dummy_payment', request_id=new_request.id)
        else:
            messages.success(request, 'Your (Basic) request has been submitted!')
            return redirect('driver_dashboard')

    return render(request, 'repair/create_request.html')


@login_required
def dummy_payment(request, request_id):
    job = get_object_or_404(RepairRequest, id=request_id)
    
    amount_in_rupees = 0
    if job.priority == 'Priority':
        amount_in_rupees = 100
    elif job.priority == 'Express':
        amount_in_rupees = 250

    context = { 'job': job, 'amount_rupees': amount_in_rupees }
    return render(request, 'repair/dummy_payment.html', context)


@login_required
def payment_success(request, request_id):
    job = get_object_or_404(RepairRequest, id=request_id)
    if job.status == 'Unpaid':
        job.status = 'Pending'
        job.save()
        messages.success(request, 'Payment confirmed! Your request is now active.')
    else:
        messages.error(request, 'This request has already been paid for.')
    return redirect('driver_dashboard')


@login_required
def driver_dashboard(request):
    try:
        driver_profile = request.user.driverprofile
    except DriverProfile.DoesNotExist:
        messages.error(request, 'You do not have a driver profile.')
        return redirect('home')

    active_requests = RepairRequest.objects.filter(
        driver=driver_profile
    ).exclude(
        status='Completed'
    ).order_by('-created_at')

    completed_requests = RepairRequest.objects.filter(
        driver=driver_profile,
        status='Completed'
    ).order_by('-created_at')

    context = {
        'active_requests': active_requests,
        'completed_requests': completed_requests,
    }
    return render(request, 'repair/driver_dashboard.html', context)


@login_required
def leave_review(request, request_id):
    job = get_object_or_404(RepairRequest, id=request_id, driver=request.user.driverprofile)
    if request.method == 'POST':
        job.rating = request.POST['rating']
        job.review_comment = request.POST['review_comment']
        job.save()
        messages.success(request, 'Thank you for your review!')
        return redirect('driver_dashboard')
    return render(request, 'repair/leave_review.html', {'job': job})

# ============================
# REPAIRER VIEWS
# ============================

@login_required
def repairer_dashboard(request):
    try:
        repairer_profile = request.user.repairerprofile
    except RepairerProfile.DoesNotExist:
        messages.error(request, 'You do not have a repairer profile.')
        return redirect('home')

    # --- 1. Get Job Lists ---
    express_jobs = RepairRequest.objects.filter(
        status='Pending', priority='Express'
    ).order_by('-created_at')
    
    priority_jobs = RepairRequest.objects.filter(
        status='Pending', priority='Priority'
    ).order_by('-created_at')
    
    basic_jobs = RepairRequest.objects.filter(
        status='Pending', priority='Basic'
    ).order_by('-created_at')

    my_active_jobs = RepairRequest.objects.filter(
        repairer=repairer_profile
    ).exclude(
        status='Completed'
    ).order_by('-created_at')

    # --- 2. Get Data for Ratings & Reviews ---
    completed_jobs = RepairRequest.objects.filter(
        repairer=repairer_profile,
        status='Completed'
    )
    
    average_rating = completed_jobs.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg']
    if average_rating:
        average_rating = round(average_rating, 1)
    else:
        average_rating = "N/A"
    
    review_list = completed_jobs.filter(review_comment__isnull=False).order_by('-created_at')[:10]

    # --- 3. Get Data for Earnings Graph ---
    chart_labels = []
    chart_data = []
    today = timezone.now()

    for i in range(5, -1, -1):
        month_start = (today - datetime.timedelta(days=i*30)).replace(day=1)
        month_name = month_start.strftime("%B")
        chart_labels.append(month_name)
        
        month_earnings = completed_jobs.filter(
            created_at__year=month_start.year,
            created_at__month=month_start.month
        ).aggregate(Sum('final_bill_amount'))['final_bill_amount__sum'] or 0
        
        chart_data.append(month_earnings)

    context = {
        'express_jobs': express_jobs,
        'priority_jobs': priority_jobs,
        'basic_jobs': basic_jobs,
        'my_active_jobs': my_active_jobs,
        'average_rating': average_rating,
        'review_list': review_list,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'repair/repairer_dashboard.html', context)


@login_required
def accept_request(request, request_id):
    try:
        repairer_profile = request.user.repairerprofile
    except RepairerProfile.DoesNotExist:
        messages.error(request, 'You are not authorized.')
        return redirect('home')
    
    job = get_object_or_404(RepairRequest, id=request_id)

    if job.status == 'Pending':
        job.repairer = repairer_profile
        job.status = 'Accepted'
        job.save()
        messages.success(request, 'Job accepted! You can now contact the driver.')
    else:
        messages.error(request, 'This job has already been taken.')

    return redirect('repairer_dashboard')


@login_required
def start_job(request, request_id):
    job = get_object_or_404(RepairRequest, id=request_id, repairer=request.user.repairerprofile)
    if job.status == 'Accepted':
        job.status = 'In Progress'
        job.save()
        messages.success(request, 'Job started! The driver will be notified.')
    else:
        messages.error(request, 'This job is not in "Accepted" status.')
    return redirect('repairer_dashboard')


@login_required
def finalize_job(request, request_id):
    job = get_object_or_404(RepairRequest, id=request_id, repairer=request.user.repairerprofile)
    
    if request.method == 'POST':
        job.final_bill_amount = request.POST['final_bill_amount']
        job.status = 'Completed'
        job.save()
        messages.success(request, 'Job finalized and marked as complete!')
        return redirect('repairer_dashboard')

    return render(request, 'repair/finalize_job.html', {'job': job})
# --- In repair/views.py ---
# (Add the imports for Count, ExtractYear if they are missing)
from django.db.models import Count
from django.db.models.functions import ExtractYear

# ... (your 'home' function) ...

# --- RENAME THIS FUNCTION from 'about_us' ---
# --- In repair/views.py ---

def work_management_public(request):
    
    # 1. Get data for the "Repairs per Year" graph
    yearly_data = RepairRequest.objects.filter(
        status='Completed'
    ).annotate(
        year=ExtractYear('created_at')
    ).values(
        'year'
    ).annotate(
        count=Count('id')
    ).order_by('year')
    
    chart_labels = [d['year'] for d in yearly_data]
    chart_data = [d['count'] for d in yearly_data]

    # 2. Get the 5 best reviews
    reviews = RepairRequest.objects.filter(
        status='Completed',
        rating__gte=4,
        review_comment__isnull=False
    ).order_by('-created_at')[:5]

    context = {
        # --- WE NOW USE json.dumps TO MAKE IT A SAFE STRING ---
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
        'reviews': reviews
    }
    return render(request, 'repair/work_management_public.html', context)