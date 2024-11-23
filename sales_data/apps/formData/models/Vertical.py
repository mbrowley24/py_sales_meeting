from django.db import models





class Vertical(models.Model):

    class Meta:
        db_table = 'verticals'
        verbose_name = 'vertical'
        verbose_name_plural = 'verticals'

    public_id = models.CharField(unique=True, max_length=100)
    name      = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)