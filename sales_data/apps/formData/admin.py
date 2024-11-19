from django.contrib import admin
from .models.division import Division, Region
from .models.timezone import Timezone
from .models.products import Products

admin.site.register(Division)
admin.site.register(Region)
admin.site.register(Timezone)
admin.site.register(Products)