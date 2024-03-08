from django.contrib import admin
from .models import Chart


class ChartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'crypto_charts'
    )

admin.site.register(Chart, ChartAdmin)