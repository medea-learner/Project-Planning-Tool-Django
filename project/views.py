import os
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from project.models import Project, ProjectCategory
from project.serializers import ProjectSerializer, ProjectCategorySerializer
from project.permissions import IsOwner #, IsOwnerOrReadOnly
from project.utils import generate_pdf


class ProjectList(generics.ListCreateAPIView):
    """
    List all projects, or create a new project.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    permission_classes = [
        permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return the list of projects where the logged-in user is the owner.
        """
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Setting the user to the current logged in user.
        """
        user = self.request.user
        serializer.save(created_by=user)
        return super().perform_create(serializer)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project instance.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser, FormParser]

    permission_classes = [
        permissions.IsAuthenticated,
        # IsOwnerOrReadOnly,
        IsOwner]


class ProjectCategoryList(generics.ListAPIView):
    """
    List all project categories.
    """
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer


class GenerateAIDescriptionSummary(APIView):
    """
    Generate a detailed description for a project
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        handle post http method
        """
        project_description = request.data.get('project_description')
        project_title = request.data.get('project_title')
        project_category = request.data.get('project_category')

        # Validate that project_description exists and is not empty
        if not project_description or project_description.strip() == "":
            return Response(
                {
                    "error": "Project description is required and cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST)

        # Construct the prompt based on the provided data
        prompt = "Generate a summary for the following project description"

        if project_title:
            prompt += f" for the project titled '{project_title}'"
            if project_category:
                prompt += f" in the category of '{project_category}'"
        elif project_category:
            prompt += f" in the category of '{project_category}'"
        
        prompt += f". Here is the description: {project_description}"

        # Prepare the headers for Hugging Face API
        headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_ACCESS_TOKEN')}"
        }

        # Send request to Hugging Face model
        try:
            response = requests.post(
                f"{settings.HUGGINGFACE_API_URL}/models/EleutherAI/gpt-neo-2.7B",
                headers=headers,
                json={"inputs": prompt},
                timeout=10
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()
            if isinstance(response_data, list):
                ai_description = response_data[0].get(
                    'generated_text',
                    'AI-generated description unavailable.')
            elif isinstance(response_data, dict):
                ai_description = response_data.get(
                    'generated_text',
                    'AI-generated description unavailable.')
            else:
                ai_description = 'AI-generated description unavailable.'

            # Return the AI-generated description summary
            return Response({"description": ai_description})

        except requests.exceptions.RequestException as e:
            # Handle request errors (e.g., network issues, invalid API)
            return Response(
                {"error": f"Error contacting the AI service: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_project_pdf(request, project_id):
    """
    Export project details as a formatted PDF, including all fields
    (title, description, dates, etc.) and associated images.
    """
    project = get_object_or_404(Project, id=project_id)
    buffer = generate_pdf(project)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=project_{project.id}.pdf'  # Set filename for download
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_project_email(request, project_id):
    """
    Send project details via email to a specified recipient.
    """
    # Validate Project ID
    project = get_object_or_404(Project, id=project_id)

    # Validate Email Address
    recipient = request.GET.get('email')
    if not recipient:
        return JsonResponse({'error': 'Email address is required.'}, status=400)

    include_pdf = request.GET.get('include_pdf', 'false').lower() == 'true'

    subject = f"Project Details: {project.title}"
    message = f"Description:\n\n{project.description}"

    email = EmailMessage(subject, message, to=[recipient])

    # Include PDF if requested
    if include_pdf:
        buffer = generate_pdf(project)
        email.attach(f"{project.title}.pdf", buffer.read(), 'application/pdf')

    email.send()

    return JsonResponse({'message': 'Email sent successfully!'}, status=200)


def index(request):
    """
    Serve React App
    """
    return render(request, 'index.html')
