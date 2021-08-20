from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img style="width:150px; height:auto;" src="{}" />'.format(obj.image.url))    
    image_tag.short_description = 'image'


    list_display = ['name','slug', 'image_tag']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img style="width:150px; height:auto;" src="{}" />'.format(obj.image.url))    
    image_tag.short_description = 'image'


    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated', 'image_tag']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(Product, ProductAdmin) 


