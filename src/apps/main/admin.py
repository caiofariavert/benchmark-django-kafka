from django.contrib import admin

from apps.main.models import BenchmarkTest


@admin.register(BenchmarkTest)
class BenchmarkTestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_type",
        "full_init_consumer_at",
        "full_ended_consumer_at",
        "time_processing",
        "is_finished"
    )
    search_fields = ("test_type",)
    list_filter = ("test_type", "is_finished")
    ordering = ("-created_at",)
