from django.contrib import admin
from .models import Category, Product
from .models import Product, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'size', 'color', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'size', 'color']
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)