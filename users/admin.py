from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):

#     """ Custom User Admin """

#     list_display = ("username", "gender", "language", "currency", "superhost")
#     list_filter = ("superhost", "currency", "language")


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Field",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )
