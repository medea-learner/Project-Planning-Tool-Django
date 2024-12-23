import json
from rest_framework import serializers
from project.models import Image, Project, ProjectCategory


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at']


from rest_framework import serializers
from .models import Project, Image

class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # For GET requests

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'category',
            'priority',
            'status',
            'images'
        ]

    def create(self, validated_data):
        uploaded_images = [
            file for key, file
            in self.context['request'].FILES.items()
            if key.startswith('uploaded_images')
        ]

        # Extract existing image IDs
        existing_images = json.loads(self.context['request'].data.get(
            'existing_images', "[]"))

        # Create the Project instance
        instance = super().create(validated_data)

        # Remove images that are no longer part of the project
        current_image_ids = [image.id for image in instance.images.all()]
        images_to_remove = set(current_image_ids) - set(existing_images)

        for image_id in images_to_remove:
            image = instance.images.get(id=image_id)
            instance.images.remove(image)

        # Add existing images that are still part of the project
        for image_id in existing_images:
            try:
                image = Image.objects.get(id=image_id)
                instance.images.add(image)
            except Image.DoesNotExist:
                continue

        # Add uploaded images to the instance (newly uploaded images)
        if uploaded_images:
            for image in uploaded_images:
                new_image = Image.objects.create(image=image)
                instance.images.add(new_image)

        return instance

    def update(self, instance, validated_data):
        uploaded_images = [
            file for key, file
            in self.context['request'].data.items()
            if key.startswith('uploaded_images')
        ]
        print(uploaded_images, validated_data)

        # Extract existing image IDs
        existing_images = json.loads(self.context['request'].data.get(
            'existing_images', "[]"))

        # Update the instance with the validated data
        instance = super().update(instance, validated_data)

        # Remove images that are no longer part of the project
        current_image_ids = [image.id for image in instance.images.all()]
        images_to_remove = set(current_image_ids) - set(existing_images)

        for image_id in images_to_remove:
            image = instance.images.get(id=image_id)
            instance.images.remove(image)

        # Add existing images that are still part of the project
        for image_id in existing_images:
            try:
                image = Image.objects.get(id=image_id)
                instance.images.add(image)
            except Image.DoesNotExist:
                continue

        # Add uploaded images to the instance (newly uploaded images)
        if uploaded_images:
            for image in uploaded_images:
                new_image = Image.objects.create(image=image)
                instance.images.add(new_image)

        return instance


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name']
