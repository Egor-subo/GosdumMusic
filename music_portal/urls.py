from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('requests/new/', views.create_request_view, name='create_request'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
]
