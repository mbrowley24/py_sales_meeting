from django.contrib import admin
from .models.division import Division, Region
from .models.timezone import Timezone
from .models.products import Products
from .models.Vertical import Vertical

admin.site.register(Division)
admin.site.register(Region)
admin.site.register(Timezone)
admin.site.register(Products)
admin.site.register(Vertical)