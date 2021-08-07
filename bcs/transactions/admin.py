from django.contrib import admin

from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'description')