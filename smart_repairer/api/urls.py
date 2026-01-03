from django.urls import path
from . import views

urlpatterns = [
    # --- Public Pages ---
    path('', views.home, name='home'),
    path('work-stats/', views.work_management_public, name='work_management_public'),

    # --- Authentication (Login/Register) ---
    path('login-as/', views.login_as_view, name='login_as'),  # <--- The one you were missing
    path('login/', views.login_form_view, name='login_form'),
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register, name='register'),
    path('register/driver/', views.register_driver, name='register_driver'),
    path('register/repairer/', views.register_repairer, name='register_repairer'),

    # --- Driver Views ---
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('create-request/', views.create_request, name='create_request'),
    path('dummy-payment/<int:request_id>/', views.dummy_payment, name='dummy_payment'),
    path('payment-success/<int:request_id>/', views.payment_success, name='payment_success'),
    path('leave-review/<int:request_id>/', views.leave_review, name='leave_review'),

    # --- Repairer Views ---
    path('repairer-dashboard/', views.repairer_dashboard, name='repairer_dashboard'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('start-job/<int:request_id>/', views.start_job, name='start_job'),
    path('finalize-job/<int:request_id>/', views.finalize_job, name='finalize_job'),
]