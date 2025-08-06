from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')  # Ensure 'token' from frontend
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request())

            if 'email' not in idinfo:
                return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            email = idinfo['email']
            name = idinfo.get('name', email.split('@')[0])  # Fallback to email prefix if name is missing

            # Get or create user in Django's DB
            user, created = User.objects.get_or_create(email=email, defaults={'username': email, 'first_name': name})

            # Generate JWT Tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'name': user.first_name
                }
            })

        except ValueError:
            return Response({'error': 'Invalid ID Token'}, status=status.HTTP_400_BAD_REQUEST)

