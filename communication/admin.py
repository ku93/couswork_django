from django.contrib import admin

from communication.models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "links",
    )
    search_fields = ("topic",)
