from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework_simplejwt.tokens import OutstandingToken


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
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
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255, unique=True)
    is_year_required = models.BooleanField(default=False)
    is_reason_required = models.BooleanField(default=False)
    is_entity_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Entity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_value = models.CharField(max_length=255,null=True)

class YearDropdown(models.Model):
    service_year_id = models.AutoField(primary_key=True)
    service_year_value = models.IntegerField(null=True)

    def __str__(self):
        return str(self.service_year_value)

class TaxOrganizer(models.Model):
    tax_organizer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    basic_details_form = models.JSONField(null=True, blank=True)
    dependents_details = models.JSONField(null=True, blank=True)
    state_details = models.JSONField(null=True, blank=True)
    income_details = models.JSONField(null=True, blank=True)
    rental_details = models.JSONField(null=True, blank=True)
    expenses_details = models.JSONField(null=True, blank=True)
    entity_details = models.JSONField(null=True, blank=True)
    shareholder_details = models.JSONField(null=True, blank=True)
    balance_sheet_details = models.JSONField(null=True, blank=True)
    link_form_details = models.JSONField(null=True, blank=True)
    home_expenses_details = models.JSONField(null=True, blank=True)
    business_formation_details = models.JSONField(null=True, blank=True)
    basic_details_updated_at = models.DateTimeField(null=True, blank=True)
    dependents_details_updated_at = models.DateTimeField(null=True, blank=True)
    state_details_updated_at = models.DateTimeField(null=True, blank=True)
    income_details_updated_at = models.DateTimeField(null=True, blank=True)
    rental_details_updated_at = models.DateTimeField(null=True, blank=True)
    expenses_details_updated_at = models.DateTimeField(null=True, blank=True)
    entity_details_updated_at = models.DateTimeField(null=True, blank=True)
    shareholder_details_updated_at = models.DateTimeField(null=True, blank=True)
    balance_sheet_details_updated_at = models.DateTimeField(null=True, blank=True)
    link_form_details_updated_at = models.DateTimeField(null=True, blank=True)
    home_expenses_details_updated_at = models.DateTimeField(null=True, blank=True)
    business_formation_details_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Tickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,null=True)
    service_id = models.IntegerField(null=True,db_index=True)
    service_year_value = models.IntegerField(db_index=True)
    reason = models.TextField()
    entity_value = models.IntegerField(null=True,db_index=True)
    disable_chatbox = models.BooleanField(default=False)
    disable_chatbox_updated_at = models.DateTimeField(null=True, blank=True)
    tax_organizer_id = models.IntegerField(db_index=True,null=True)
    invoice_id = models.IntegerField(null=True, blank=True)
    invoice_id_updated_at = models.DateTimeField(null=True, blank=True)
    ticket_status = models.CharField(max_length=50)
    assignee_agent_name = models.CharField(max_length=100, null=True, blank=True)
    assignee_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_status_updated_at = models.DateTimeField(auto_now=True)

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    agent_name = models.CharField(max_length=255, null=True, blank=True)
    sender_type = models.CharField(max_length=10, choices=[('user', 'User'), ('agent', 'Agent')])
    message_content = models.TextField()
    message_status = models.CharField(max_length=10, default='Unread')
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket_id = models.IntegerField(db_index=True)



class TicketFiles(models.Model):
    file_id = models.AutoField(primary_key=True)
    ticket_id = models.IntegerField()
    username = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.username}"
    

