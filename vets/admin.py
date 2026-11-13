from django.contrib import admin
from .models import Vet


@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'shift', 'phone', 'is_available', 'created_at')
    list_filter = ('shift', 'is_available')
    search_fields = ('name', 'specialization', 'clinic_address', 'phone')
    list_editable = ('is_available', 'shift')
    fieldsets = (
        ('Personal & Professional Info', {
            'fields': ('name', 'specialization', 'bio', 'image')
        }),
        ('Shift & Working Hours', {
            'fields': ('shift', 'is_available')
        }),
        ('Contact & Clinic', {
            'fields': ('phone', 'email', 'clinic_address')
        }),
    )

