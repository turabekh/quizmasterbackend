from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentGroup

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'group',)
    list_filter = ('email', 'first_name', 'last_name', 'group')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'group')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_teacher')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Security', {'fields': ('failed_login_attempts', 'lockout_until')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'group', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'year', 'semester',)
    list_filter = ('year', 'semester',)
    search_fields = ('group_name',)
    ordering = ('year', 'semester', 'group_name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
