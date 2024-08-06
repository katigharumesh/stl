
from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserCreateView,ActivateUserView,CheckActivationStatusView,YearDropdownListView, EntityListView, CreateTaxOrganizerTicketNotificationView, UpdateTaxOrganizerFieldView, UserTicketsView,TaxOrganizerDetailView

urlpatterns = [
    path('api/signup/', UserCreateView.as_view(), name='user_signup'),
    path('api/activate/<int:activation_code>/', ActivateUserView.as_view(), name='activate_user'),
    path('api/check-activation-status/', CheckActivationStatusView.as_view(), name='check-activation-status'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/year-dropdown/', YearDropdownListView.as_view(), name='year-dropdown-list'),
    path('api/entities/', EntityListView.as_view(), name='entity-list'),
    path('api/create_tax_organizer_ticket_notification/', CreateTaxOrganizerTicketNotificationView.as_view(), name='create_tax_organizer_ticket_notification'),
    path('api/update_tax_organizer_field/', UpdateTaxOrganizerFieldView.as_view(), name='update_tax_organizer_field'),
    path('api/user_tickets/', UserTicketsView.as_view(), name='user_tickets'),
    path('api/tax_organizer_details/', TaxOrganizerDetailView.as_view(), name='tax_organizer_detail'),
]