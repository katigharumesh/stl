from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework_simplejwt.tokens import OutstandingToken


class Users(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resend_link_flag = models.BooleanField(default=True)
    activation_code = models.IntegerField(null=True,db_index=True)
    is_activated = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True,db_index=True)
    referral_code = models.CharField(max_length=150, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']

    objects = BaseUserManager()


class Services(models.Model):
    service_name = models.CharField(max_length=255, unique=True)
    is_year_required = models.BooleanField(default=False)
    is_reason_required = models.BooleanField(default=False)
    is_entity_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Tickets(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    service_year_value = models.IntegerField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    disable_chatbox = models.BooleanField(default=False)
    tax_organiser_id = models.IntegerField(null=True, blank=True)
    tax_draft_id = models.IntegerField(null=True, blank=True)
    document_id = models.IntegerField(null=True, blank=True)
    invoice_id = models.IntegerField(null=True, blank=True)
    p_document_id = models.IntegerField(null=True, blank=True)
    ticket_status = models.CharField(max_length=50, null=True, blank=True)
    assigned_agent_id = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
