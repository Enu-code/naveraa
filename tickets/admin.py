from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'category', 'priority', 'status', 'source', 'created_at')
    list_filter = ('status', 'priority', 'category', 'source')
    search_fields = ('description', 'reporter_name', 'reporter_phone')
    readonly_fields = ('created_at',)