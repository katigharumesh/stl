
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Users, Services, Tickets, Entity,YearDropdown,TaxOrganizer,Notifications,TicketFiles
from .serializers import UserSerializer, ServiceSerializer, TicketSerializer, CustomTokenObtainPairSerializer ,EntitySerializer,YearDropdownSerializer,TaxOrganizerSerializer,TicketFilesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.http import JsonResponse


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
            return Response({"success": False,'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_check.is_activated:
            return Response({"success": True,'message': 'User is activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({"success": True,'message': 'User is not activated.'}, status=status.HTTP_200_OK)
        

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
            "success": True,
            'message': 'Login successful',
            'access_token':access_token,
            'refresh_token':refresh_token
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
        refresh_token = request.get('refresh_token')
        if not refresh_token:
            return Response({"success": False,'message': "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            data = {"access": str(refresh.access_token)}
            
            response = Response({"success": True,'message': "access token is generated.","access_token":data['access']}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return response
        except Exception as e:
            return Response({"success": False,"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceListView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class EntityListView(generics.ListAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #throttle_classes = [UserRateThrottle]

class YearDropdownListView(generics.ListAPIView):
    queryset = YearDropdown.objects.all()
    serializer_class = YearDropdownSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CreateTaxOrganizerTicketNotificationView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        username = user.username
        service_id = request.data.get('service_id')
        service_year_value = request.data.get('service_year_value')
        reason = request.data.get('reason')
        entity_value = request.data.get('entity_value')

        if not service_id or not service_year_value or not reason or not entity_value:
            return Response({"success": False,'message': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Insert into TaxOrganizer
        tax_organizer = TaxOrganizer.objects.create(username=username)

        # Insert into Ticket
        ticket = Tickets.objects.create(
            username=username,
            service_id=service_id,
            service_year_value=service_year_value,
            reason=reason,
            entity_value=entity_value,
            tax_organizer_id=tax_organizer.tax_organizer_id
        )

        # Insert into Notification
        Notifications.objects.create(
            username=username,
            sender_type="user",
            message_content="A new ticket is created",
            ticket_id=ticket.ticket_id
        )

        return Response({"success": True,'message': 'Ticket Created successfully'}, status=status.HTTP_201_CREATED)
    

class UpdateTaxOrganizerFieldView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        username = user.username
        tax_organizer_id = request.data.get('tax_organizer_id')
        column_name = request.data.get('column_name')
        json_value = request.data.get('column_value')

        if not tax_organizer_id or not column_name or not json_value:
            return Response({'error': 'tax_organizer_id, column_name, and form values are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tax_organizer = TaxOrganizer.objects.get(pk=tax_organizer_id, username=username)
        except TaxOrganizer.DoesNotExist:
            return Response({"success": False,'message': 'TaxOrganizer not found.'}, status=status.HTTP_404_NOT_FOUND)

        if column_name not in ['basic_details_form', 'dependents_details', 'state_details', 'income_details', 'rental_details', 'expenses_details', 'entity_details', 'shareholder_details', 'balance_sheet_details', 'link_form_details', 'home_expenses_details', 'business_formation_details']:
            return Response({"success": False,'Message': 'Invalid column name.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the specified JSON field
        setattr(tax_organizer, column_name, json_value)
        # Update the corresponding timestamp field
        timestamp_field = f"{column_name}_updated_at"
        setattr(tax_organizer, timestamp_field, timezone.now())
        
        tax_organizer.save()

        return Response({"success": True,'message': 'Form saved successfully'}, status=status.HTTP_200_OK)
    

class UserTicketsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        return Tickets.objects.filter(username=user.username)
    


class TaxOrganizerDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        tax_organizer_id = request.data.get('tax_organizer_id')
        column_names = request.data.get('column_names', '').split(',')

        if not tax_organizer_id:
            return JsonResponse({"success": False,'message': 'tax_organizer_id is required'}, status=400)

        try:
            tax_organizer = TaxOrganizer.objects.get(pk=tax_organizer_id, username=request.user.username)
        except TaxOrganizer.DoesNotExist:
            return JsonResponse({"success": False,'message': 'TaxOrganizer not found'}, status=404)

        if column_names == ['']:
            serializer = TaxOrganizerSerializer(tax_organizer)
            return Response(serializer.data)
        else:
            result = {}
            for column_name in column_names:
                column_name = column_name.strip()
                if hasattr(tax_organizer, column_name):
                    result[column_name] = getattr(tax_organizer, column_name)
                else:
                    return JsonResponse({'error': f'Column {column_name} not found in TaxOrganizer'}, status=400)
            return JsonResponse(result, safe=False)
    
class CreateTicketFileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TicketFilesSerializer(data=request.data)
        if serializer.is_valid():
            # Save the file with the username from the token
            file_instance = serializer.save(username=request.user.username)
            
            # Construct a success message
            success_message = {
                'file_name': file_instance.file_name,
                'message': 'File uploaded successfully.'
            }
            
            return Response(success_message, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetTicketFilesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('ticket_id')
        if not ticket_id:
            return Response({'error': 'ticket_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        files = TicketFiles.objects.filter(ticket_id=ticket_id, username=request.user.username).order_by('-upload_date')
        serializer = TicketFilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)