from django.contrib import admin
from .models.customGroup import CustomGroup
from .models.timezone import Timezone
from .models.products import Products
from .models.Vertical import Vertical

admin.site.register(CustomGroup)
admin.site.register(Timezone)
admin.site.register(Products)
admin.site.register(Vertical)