from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .utils import generate_access_token, random_number_generator
import datetime
from django.contrib.auth.hashers import make_password


class DeviceID(models.Model):
    """
    Model for Saving Device Id
    """
    device_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.device_id


class UserProfile(models.Model):
    """
    Model for saving extra user credentials like access token, reset key etc.
    This model can be inherited to get make appropriate user profile models
    """
    CHOICE = (
        ('-', '-'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=100, blank=True, null=True)
    access_token_expiration = models.DateField(default=timezone.now)
    device_id = models.ManyToManyField(DeviceID, blank=True)
    reset_key = models.CharField(max_length=30, blank=True, null=True, default='')
    reset_key_expiration = models.DateTimeField(default=None, blank=True, null=True)
    otp = models.CharField(max_length=500, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True, default=None)
    phone_number = models.BigIntegerField(default=0)
    profile_image = models.ImageField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=CHOICE, default='-')
    date_updated = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.user.username

    def set_reset_key(self):
        self.reset_key = generate_access_token(self.user.id)
        self.reset_key_expiration = timezone.now() + datetime.timedelta(hours=1)

    def verify_reset_key_expiry(self):
        if timezone.now() <= self.reset_key_expiration:
            return True
        else:
            return False

    def set_access_token(self, user_id):
        self.access_token = generate_access_token(user_id)
        self.access_token_expiration = timezone.now() + datetime.timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    def verify_access_token_expiry(self):
        if timezone.now() <= self.access_token_expiration:
            return True
        else:
            return False

    def set_otp(self):
        raw_otp = random_number_generator(6, '0123456789')
        self.otp = make_password(raw_otp)
        self.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        self.raw_otp = raw_otp

    def verify_otp(self, raw_otp):
        if self.otp is not None:
            try:
                salt = self.otp.split('$')[2]
                hashed_otp = make_password(raw_otp, salt)
                if self.otp == hashed_otp:
                    if timezone.now() <= self.otp_expiry:
                        return True
                    else:
                        return False
            except IndexError:
                return None
        else:
            return None

    def refresh_access_token(self):
        current_date = datetime.datetime.today().date()
        if current_date > self.access_token_expiration:
            access_token = generate_access_token(self.user.id)
            self.access_token = access_token
            self.access_token_expiration = current_date + datetime.timedelta(
                days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
            self.save()

        return self.access_token

    def add_device_id(self, device_id):
        try:
            DeviceID.objects.get(device_id=device_id)

        except DeviceID.DoesNotExist:
            device_obj = DeviceID(device_id=device_id)
            device_obj.save()

            self.device_id.add(device_obj)

        return device_id



