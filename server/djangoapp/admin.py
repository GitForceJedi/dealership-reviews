from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel
# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ('name', 'car_make', 'car_type', 'year', 'color', 'doors', 'average_rating')
    # Add any other configuration options you need for CarModelAdmin
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ('name', 'company')
    inlines = [CarModelInline]
    # Add any other configuration options you need for CarMakeAdmin

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)