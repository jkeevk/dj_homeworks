from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "description",
        "status",
        "creator",
        "created_at",
        "updated_at",
    ]

    list_filter = ["status", "creator", "created_at"]

    search_fields = ["title", "description", "creator__username"]

    ordering = ["-created_at"]

    list_per_page = 20

    fields = ["title", "description", "status", "creator", "created_at", "updated_at"]

    readonly_fields = ["created_at", "updated_at"]