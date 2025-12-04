from django.contrib import admin

# Register your models here.
from .models import CarouselSlide

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active') 
    search_fields = ('title', 'description')
    ordering = ('order',)