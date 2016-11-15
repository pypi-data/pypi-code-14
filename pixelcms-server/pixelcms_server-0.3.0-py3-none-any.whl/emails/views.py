from rest_framework import generics

# from .models import Message
from .serializers import ContactFormSerializer


class ContactFormView(generics.CreateAPIView):
    serializer_class = ContactFormSerializer
