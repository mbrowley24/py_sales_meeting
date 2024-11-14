from django.contrib import admin
from .models import SalesRoles, SalesRepresentative, Coverage

admin.site.register(SalesRoles)
admin.site.register(SalesRepresentative)
admin.site.register(Coverage)