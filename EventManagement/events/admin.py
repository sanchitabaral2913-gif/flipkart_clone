from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'status', 'date', 'start_time']
    list_filter = ['status', 'date', 'created_by']

    # ❌ in fields ko change nahi kar sakta
    readonly_fields = [
        'title',
        'description',
        'date',
        'start_time',
        'created_by',
    ]

    # 👇 form me sirf status editable
    fields = (
        'title',
        'description',
        'date',
        'start_time',
        'created_by',
        'status',   # ✅ ONLY editable field
    )

    actions = ['mark_accepted', 'mark_rejected']

    def mark_accepted(self, request, queryset):
        queryset.update(status='Accepted')
    mark_accepted.short_description = "Accept selected events"

    def mark_rejected(self, request, queryset):
        queryset.update(status='Rejected')
    mark_rejected.short_description = "Reject selected events"
