from django.contrib import admin
from .models import (Country, Year, SuicideCase)


# Register your models here.

admin.site.register(Country)
admin.site.register(Year)
admin.site.register(SuicideCase)