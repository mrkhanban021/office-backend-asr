from django.contrib import admin
from .models import OTP, ProfileUser, CustomUser, OTPRequest
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm

# Register your models here.


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ("id", 'otp', "request_time")
    search_fields = ("id", 'otp')
    ordering = ('request_time',)
    list_display_links = ("id", 'otp')
    list_per_page = 13


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ("id", 'user', 'name', 'last_name', 'id_code', 'created_at')
    search_fields = ("id", 'user', 'name', 'last_name', 'id_code')
    ordering = ('created_at',)
    list_display_links = ("id", 'user', 'name', 'last_name', 'id_code', 'created_at')
    list_per_page = 13


class ProfileInline(admin.StackedInline):
    model = ProfileUser
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('id', "phone_number", "role", "is_active", "is_staff", "is_superuser",)
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    inlines = (ProfileInline,)
    list_display_links = ("id", 'phone_number')
    list_per_page = 13

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'role', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(OTP)
class OTPModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'created_at', 'expires_at', 'is_verified')
    list_display_links = ('id', 'user', 'code', 'created_at', 'expires_at', 'is_verified')
