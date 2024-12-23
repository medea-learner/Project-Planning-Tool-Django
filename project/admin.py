from django.contrib import admin

from .models import Project, ProjectCategory


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "status", "priority", "created_by"]

    @admin.display()
    def description(self, obj):
        return (
            (obj.description[:50] + "...")
            if len(obj.description) > 50 else obj.description
        )


admin.site.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
