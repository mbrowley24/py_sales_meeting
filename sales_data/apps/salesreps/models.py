from django.db import models
from django.contrib.auth.models import User


class SalesRoles(models.Model):
    class Meta:
        db_table = 'sales_roles'
        verbose_name = 'Sales Role'
        verbose_name_plural = 'Sales Roles'
        indexes = [
            models.Index(fields=['public_id'])
        ]

    public_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()


class SalesRepresentative(models.Model):

    class Meta:
        db_table = 'sales_representatives'
        # verbose_name = 'Sales Representative'
        # verbose_name_plural = 'Sales Representatives'


    public_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False)
    sales_engineer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_reps')
    Role = models.ForeignKey(SalesRoles, on_delete=models.CASCADE, related_name='roles')
    quota = models.BigIntegerField(default=0)
    Created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Coverage(models.Model):
    class Meta:
        db_table = 'coverages'
        verbose_name = 'coverage'
        verbose_name_plural = 'coverages'
        indexes = [
            models.Index(fields=['public_id']),
        ]

    public_id = models.CharField(max_length=100, unique=True)
    sales_engineer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rep_coverages')
    sales_representative = models.ForeignKey(SalesRepresentative, on_delete=models.CASCADE, related_name='se_coverages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)