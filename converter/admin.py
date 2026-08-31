from django.contrib import admin

from .models import (
    Profile,
    Conversion,
    Favourite,
    Feedback,
    
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
    )


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "from_currency",
        "to_currency",
        "amount",
        "converted_amount",
        "conversion_date",
    )

    list_filter = (
        "from_currency",
        "to_currency",
    )


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "from_currency",
        "to_currency",
        "added_date",
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "comment",
        "submitted_date",
    )

    list_filter = (
        "submitted_date",
    )

    search_fields = (
        "user__username",
        "comment",
    )


