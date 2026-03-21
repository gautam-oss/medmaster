from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Patient, Doctor


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone_number', 'aadhaar_status')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('aadhaar_front_preview', 'aadhaar_back_preview')

    def phone_number(self, obj):
        return obj.user.phone
    phone_number.short_description = 'Phone'

    def aadhaar_status(self, obj):
        if obj.aadhaar_front and obj.aadhaar_back:
            return format_html('<span style="color:green;">✓ Both sides</span>')
        elif obj.aadhaar_front or obj.aadhaar_back:
            return format_html('<span style="color:orange;">⚠ Partial</span>')
        return format_html('<span style="color:red;">✗ Not uploaded</span>')
    aadhaar_status.short_description = 'Aadhaar'

    def aadhaar_front_preview(self, obj):
        if obj.aadhaar_front:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.aadhaar_front.url)
        return "Not uploaded"
    aadhaar_front_preview.short_description = 'Aadhaar Front'

    def aadhaar_back_preview(self, obj):
        if obj.aadhaar_back:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.aadhaar_back.url)
        return "Not uploaded"
    aadhaar_back_preview.short_description = 'Aadhaar Back'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'experience_years', 'consultation_fee', 'aadhaar_status')
    list_filter = ('specialization',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    readonly_fields = ('aadhaar_front_preview', 'aadhaar_back_preview')

    def aadhaar_status(self, obj):
        if obj.aadhaar_front and obj.aadhaar_back:
            return format_html('<span style="color:green;">✓ Both sides</span>')
        elif obj.aadhaar_front or obj.aadhaar_back:
            return format_html('<span style="color:orange;">⚠ Partial</span>')
        return format_html('<span style="color:red;">✗ Not uploaded</span>')
    aadhaar_status.short_description = 'Aadhaar'

    def aadhaar_front_preview(self, obj):
        if obj.aadhaar_front:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.aadhaar_front.url)
        return "Not uploaded"
    aadhaar_front_preview.short_description = 'Aadhaar Front'

    def aadhaar_back_preview(self, obj):
        if obj.aadhaar_back:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.aadhaar_back.url)
        return "Not uploaded"
    aadhaar_back_preview.short_description = 'Aadhaar Back'
