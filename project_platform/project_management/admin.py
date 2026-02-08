from django.contrib import admin
from .models import Client, Project, Assignment, ProfessionalProfile


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "seniority")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "start_date", "end_date")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("project", "collaborator", "role", "assigned_hours", "assigned_at")