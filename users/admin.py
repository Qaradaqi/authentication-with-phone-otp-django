# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     list_display = ('id', 'phone_number', 'otp_field')
#     search_fields = ('phone_number')
#     ordering = ('phone_number',)

#     fieldsets = (
#         (None, {'fields': ('phone_number', 'password')}),
#         ('Personal Info', {'fields': ('username', 'email', 'otp_field')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'password1', 'password2', 'username', 'email'),
#         }),
#     )

#     def get_form(self, request, obj=None, **kwargs):
#         # Customize the form to make 'username' optional
#         form = super().get_form(request, obj, **kwargs)
#         form.base_fields['username'].required = False
#         return form

admin.site.register(CustomUser)
