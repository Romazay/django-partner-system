from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-partner/<int:partner_id>/',
         views.approve_partner, name='approve_partner'),
    path('create-promo-code/<int:partner_id>/',
         views.create_promo_code, name='create_promo_code'),
    path('toggle-promo-code/<int:code_id>/',
         views.toggle_promo_code, name='toggle_promo_code'),
    path('delete-promo-code/<int:code_id>/',
         views.delete_promo_code, name='delete_promo_code'),
]
