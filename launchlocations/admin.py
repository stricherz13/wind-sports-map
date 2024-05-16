from django.contrib import admin
from .models import LaunchLocation, Weather, Direction


class LaunchLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "get_user_full_name", "updated_at")

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user_full_name.short_description = (
        "User Name"  # Sets column name in admin interface
    )


admin.site.register(LaunchLocation, LaunchLocationAdmin)
admin.site.register(Weather)
admin.site.register(Direction)
