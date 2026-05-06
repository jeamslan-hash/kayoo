from django.contrib import admin
from .models import Category, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "transaction_type",
        "status",
        "price",
        "currency",
        "city",
        "is_featured",
        "created_at",
    )
    list_filter = (
        "category",
        "transaction_type",
        "status",
        "city",
        "is_featured",
    )
    search_fields = (
        "title",
        "city",
        "address",
        "short_description",
        "full_description",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PropertyImageInline]