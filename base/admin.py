from django.contrib import admin
from .forms import *
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    form = ProductForm
    list_display = ('name', 'team', 'racing_series')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'racing_series')


class RacingSeriesAdmin(admin.ModelAdmin):
    list_display = 'name'


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Team, TeamAdmin)
admin.site.register(Category)
admin.site.register(RacingSeries)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
