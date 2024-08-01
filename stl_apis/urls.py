
from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserCreateView, TicketListCreateView,ActivateUserView,CheckActivationStatusView

urlpatterns = [
    path('api/signup/', UserCreateView.as_view(), name='user_signup'),
    path('api/activate/<int:activation_code>/', ActivateUserView.as_view(), name='activate_user'),
    path('api/check-activation-status/', CheckActivationStatusView.as_view(), name='check-activation-status'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/tickets/', TicketListCreateView.as_view(), name='tickets'),

]