from django.contrib import admin
from .models.division import Division, Region
from .models.timezone import Timezone

admin.site.register(Division)
admin.site.register(Region)
admin.site.register(Timezone)
