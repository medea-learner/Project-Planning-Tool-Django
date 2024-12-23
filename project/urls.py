from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('projects/',
         views.ProjectList.as_view(),
         name='project-list'),
    path('projects/<int:pk>/',
         views.ProjectDetail.as_view(),
         name='project-detail'),
    path('project-categories/',
         views.ProjectCategoryList.as_view(),
         name='project-category-list'),
    path('generate-description-summary/',
         views.GenerateAIDescriptionSummary.as_view(),
         name='generate_ai_description_summary'),
    path('export-pdf/<int:project_id>/',
         views.export_project_pdf,
         name='export_project_pdf'),
    path('send-email/<int:project_id>/',
         views.send_project_email,
         name='send_project_email'),
    path('', views.index, name='index'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
