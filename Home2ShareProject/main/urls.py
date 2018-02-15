from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('logout/', views.logout_view, name='Logout'),
    path('user/<slug>/', views.ProfileView.as_view(), name='profile'),
    path('user/<slug>/update', views.UpdateUserView.as_view(), name='user-update'),
    path('register/',views.UserCreateView.as_view(),name='register'),
]
