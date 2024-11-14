from django.db import models



class Division(models.Model):

    class Meta:
        db_table = 'division'
        verbose_name = 'division'
        verbose_name_plural = 'divisions'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['public_id']),
        ]

    public_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Region(models.Model):
    class Meta:
        db_table = 'region'
        verbose_name = 'region'
        verbose_name_plural = 'regions'
        indexes = []

    public_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='regions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name