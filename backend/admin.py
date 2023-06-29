from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shop, ProductInfo, User, Category, Product, Parameter, ProductParameter, Order, OrderItem, Contact, \
    ConfirmEmailToken
# from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


class ImportFrom(forms.Form):
    url = forms.URLField()


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    change_list_template = 'admin/shop_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_data)
        ]
        return urls + my_urls

    def import_data(self, request):
        if request.method == "POST":
            form = ImportFrom(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                Shop.load_goods(url)
                self.message_user(request, "Data imported successfully")
                return redirect("..")
        else:
            form = ImportFrom()
        return render(request, 'admin/import.html', {'form': form})


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'state', 'dt', 'contact',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)