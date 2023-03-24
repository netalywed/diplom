"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.serializers import ProductInfoSerializer
from backend.views import ShopViewSet, CategoryViewSet, ProductInfoViewSet, RegisterAccount, LoginAccount, \
    ConfirmAccount, AccountDetails

r = DefaultRouter()
r.register('categories', CategoryViewSet)
r.register('shops', ShopViewSet)
r.register('products', ProductInfoViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    # path('user/contact', ContactView.as_view(), name='user-contact'),
    # path('user/password_reset', reset_password_request_token, name='password-reset'),
    # path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
] + r.urls
