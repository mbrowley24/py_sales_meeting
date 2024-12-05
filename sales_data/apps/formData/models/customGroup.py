from django.contrib.auth.models import User
from django.db import models

from apps.organization.models import Organization


class CustomGroup(models.Model):

    class Meta:

        db_table            = 'custom_groups'
        verbose_name        = 'custom_group'
        verbose_name_plural = 'custom_groups'

    public_id     = models.CharField(max_length = 100, unique = True)
    name          = models.CharField(max_length = 100)
    description   = models.CharField(max_length = 100)
    organization  = models.ForeignKey(Organization,
                                      on_delete    = models.CASCADE,
                                      related_name = 'custom_groups',
                                      null         = True
                                      )
    create_by     = models.ForeignKey(User,
                                      on_delete    = models.CASCADE,
                                      related_name = 'custom_groups',
                                      null = True,
                                      blank = True
                                      )
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now     = True)


class UserGroup(models.Model):

    class Meta:
        db_table            = 'custom_user_groups'
        verbose_name        = 'custom_user_group'
        verbose_name_plural = 'custom_user_groups'
        indexes             = [
            models.Index(fields = ['user'], name = 'user_group_user_index'),
            models.Index(fields = ['group'], name = 'user_group_group_index')
        ]

    group      = models.ForeignKey(CustomGroup, on_delete = models.CASCADE, related_name = 'user_groups')
    user       = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_groups')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
