from django.db import models
from django.contrib.auth.models import User
from apps.formData.models.timezone import Timezone
from apps.formData.models.division import Region

class UserProfile(models.Model):

    def _str_(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        indexes = [
            models.Index(fields=['public_id']),
        ]


    public_id = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_engineers', null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    reset_password = models.BooleanField(default=True)
    reset_password_token = models.CharField(max_length=15)
    reset_token_expiration = models.DateTimeField(null=True, blank=True)
    time_zone = models.ForeignKey(Timezone, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_engineers')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
