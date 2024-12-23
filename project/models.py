from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='project_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    class ProjectPriority(models.TextChoices):
        CRITICAL = 'Critical', _('Critical')
        HIGH = 'High', _('High')
        MEDIUM = 'Medium', _('Medium')
        TRIVIAL = 'Trivial', _('Trivial')
        LOW = 'Low', _('Low')

    class ProjectStatus(models.TextChoices):
        WAITING = 'Waiting', _('Waiting')
        IN_PROGRESS = 'In Progress', _('In Progress')
        DONE = 'Done', _('Done')

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)

    # created_at = models.DateTimeField(auto_now_add=True, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    category = models.ForeignKey(ProjectCategory, related_name='projects',
                                 on_delete=models.CASCADE, null=False)

    priority = models.CharField(
        max_length=8,
        choices=ProjectPriority.choices,
        default=ProjectPriority.TRIVIAL
    )

    status = models.CharField(
        max_length=11,
        choices=ProjectStatus.choices,
        default=ProjectStatus.WAITING
    )

    created_by = models.ForeignKey(User, related_name='projects',
                                   on_delete=models.CASCADE, null=False)

    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.title
