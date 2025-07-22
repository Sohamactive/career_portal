from django.contrib import admin
from .models import *
# from applications.models import Application
# Register your models here.

# class ApplicationInline(admin.TabularInline):  # or admin.StackedInline
#     model = Application
#     extra = 1  # How many empty forms to show
#     fields = ('user', 'resume', 'status')  # Customize as needed
#     readonly_fields = ()  # Optional


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
    prepopulated_fields = {'slug':('name',)}


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'type',
        'location',
        'duration',
        'application_deadline',
        'is_active',
        'has_vacancy'

    )

    list_filter = (
        'is_active',
        'type',
        'location',
    )

    search_fields = (
        'title',
        'description',
        'requirements',
    )

    readonly_fields = (
        'created_at',
        'current_accepted',
    )

    fieldsets = (
        ('Internship Details', {
            'fields': ('title', 'description', 'type', 'location', 'duration')
        }),
        ('Requirements & Skills', {
            'fields': ('requirements', 'eligibility', 'skills_required')
        }),
        ('Important Dates', {
            'fields': ('application_deadline', 'created_at')
        }),
        ('Vacancy Status', {
            'fields': ('max_positions', 'current_accepted', 'is_active')
        }),
    )
    ordering = ('-created_at',)
    # inlines = [ApplicationInline,]
