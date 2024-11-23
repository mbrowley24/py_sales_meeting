from apps.formData.models.Vertical import Vertical
from apps.salesreps.models import SalesRepresentative
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    class Meta:
        db_table     = 'customers'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        indexes = [
            models.Index(fields=['public_id'], name='public_id_idx'),
            models.Index(fields=['name'], name = 'customer_name_idx'),
        ]


    public_id      = models.CharField(unique = True, max_length = 100)
    name           = models.CharField(max_length = 100, unique = True, null = True, blank = True)
    sales_engineer = models.ForeignKey(User,
                                    on_delete = models.SET_NULL,
                                    null      = True,
                                    blank     = True
                                    )
    sales_rep      = models.ForeignKey(SalesRepresentative,
                                    null      = True,
                                    on_delete = models.SET_NULL,
                                    blank     = True
                                   )
    notes          = models.CharField(max_length = 255, null = True, blank = True)
    vertical       = models.ForeignKey(Vertical,
                                       on_delete    = models.SET_NULL,
                                       null         = True,
                                       blank        = True,
                                       related_name = 'companies')

    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now     = True)
