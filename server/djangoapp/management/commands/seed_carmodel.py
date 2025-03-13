from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel

class Command(BaseCommand):
    help = 'Seeds the CarModel table with initial data'

    def handle(self, *args, **kwargs):
        # Fetch car makes
        car_make_1 = CarMake.objects.get(name='Toyota')
        car_make_2 = CarMake.objects.get(name='Ford')
        car_make_3 = CarMake.objects.get(name='Chevrolet')

        # Create car models associated with car makes
        CarModel.objects.create(car_make=car_make_1, name='Corolla', year='2020-01-01')
        CarModel.objects.create(car_make=car_make_1, name='Camry', year='2021-01-01')
        CarModel.objects.create(car_make=car_make_2, name='Focus', year='2020-01-01')
        CarModel.objects.create(car_make=car_make_2, name='Mustang', year='2021-01-01')
        CarModel.objects.create(car_make=car_make_3, name='Impala', year='2020-01-01')
        CarModel.objects.create(car_make=car_make_3, name='Malibu', year='2021-01-01')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the CarModel table'))
