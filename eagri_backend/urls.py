"""
URL configuration for eagri_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse

# A simple view to test the server
def index(request):
    return HttpResponse("Welcome to EAgri Backend API")

urlpatterns = [
    path('', index, name='index'),
    path('users/', include('users.urls')),
    path('e_loan/', include('E_Loan.urls')),
    path('e_market/', include('E_Market.urls')),
    path('e_munshi/', include('E_Munshi.urls')),
]
