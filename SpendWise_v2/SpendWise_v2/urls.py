"""
URL configuration for SpendWise_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    # home page
    path('', views.home_view, name='home'),
    
    # login pages
    path('login/', views.Login, name='login'),
    path('signup/', views.Signup, name='signup'),
    path('home2/', views.home_pg, name='pg'),
    path('logout/', views.Logout, name='logout'),

    # profile page
    path('profile/<str:pk>', views.profile, name='profile'),

    # edit expense
    path('profile/<str:pk>/<int:id>', views.editExpView, name='edit'),

    # set balence 
    path('profile/<str:pk>/bal', views.setBal, name='setBal')
]
