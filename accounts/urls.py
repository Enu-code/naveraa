from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Uses Django's built-in secure login system!
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/update/<int:ticket_id>/', views.update_ticket_status, name='update_ticket'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]