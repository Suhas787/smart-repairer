from django.db import models
from django.contrib.auth.models import User

# --- Profile for a Driver ---
class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_number}"

# --- Profile for a Repairer ---
class RepairerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.workshop_name}"

# --- The "Ticket" for a Repair Job ---
# --- In repair/models.py ---

class RepairRequest(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    repairer = models.ForeignKey(RepairerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    issue_description = models.TextField()
    problem_image = models.ImageField(upload_to='problem_images/', null=True, blank=True)
    priority = models.CharField(max_length=10, default='Basic')
    
    # --- NEW FIELDS FOR RATINGS & EARNINGS ---
    final_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True) # 1-5 stars
    review_comment = models.TextField(null=True, blank=True)

    # ... (inside your RepairRequest class) ...

    # --- UPDATED STATUS CHOICES ---
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('In Progress', 'In Progress'), # <-- ADD THIS LINE
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
# ... (rest of your model) ...
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.user.username} - {self.status}"
rating = models.IntegerField(null=True, blank=True)
review_comment = models.TextField(null=True, blank=True)
final_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)