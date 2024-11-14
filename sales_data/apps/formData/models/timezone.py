from django.db import models



class Timezone(models.Model):

    class Meta:
        db_table = 'timezones'
        verbose_name = 'timezone'
        verbose_name_plural = 'timezones'
        indexes = [
            models.Index(fields=['name'], name='time_zone_name_idx'),
        ]

    public_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name