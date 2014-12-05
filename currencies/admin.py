from django.contrib import admin
from currencies.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "is_base", "code", "symbol", "factor", "rounding", "source", "rate_interval")
    list_filter = ("is_active", )
    search_fields = ("name", "code")

admin.site.register(Currency, CurrencyAdmin)
