from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import SignUpSerializer


class SignUpView(generics.GenericAPIView):
    """
    User sign up view.
    """
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        """
        Create a new user.
        """
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
