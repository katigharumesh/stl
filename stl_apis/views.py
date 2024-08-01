
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Users, Services, Tickets
from .serializers import UserSerializer, ServiceSerializer, TicketSerializer, CustomTokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomTokenRefreshView(TokenRefreshView):
    pass

class UserCreateView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "success": True,
                "message": "User creation successful. An activation link has been sent to your email. Please validate the activation code to complete signup."
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, activation_code):
        try:
            user = Users.objects.get(activation_code=activation_code)
            if user.is_activated:
                return Response({'message': 'User already activated.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_activated = True
            #user.activation_code = None  # Clear the activation code after successful activation
            user.save()

            return Response({'message': 'User activated successfully.'}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({'message': 'Invalid activation code.'}, status=status.HTTP_400_BAD_REQUEST)

class CheckActivationStatusView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        try:
            user_to_check = Users.objects.get(username=user.username)
        except Users.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_check.is_activated:
            return Response({'activated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'activated': False}, status=status.HTTP_200_OK)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

        # Set the tokens in cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response
    
class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            data = {"access": str(refresh.access_token)}
            
            response = Response(data, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceListView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='100/30m', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)