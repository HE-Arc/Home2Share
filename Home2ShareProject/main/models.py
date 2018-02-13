from django.db import models

# Create your models here.
class House(models.Model):
    name=models.CharField(max_length=200)

    COUNTRIES = (
        ('CH', 'Switzerland'),
        ('FR', 'France'),
        ('BE', 'Belgium'),
    )
    country = models.CharField(max_length=2, choices=COUNTRIES)
    city=models.CharField(max_length=200)
    street_name=models.CharField(max_length=200)
    street_number=models.PositiveSmallIntegerField()
    description=models.TextField(max_length=500)
    room_quantity=models.PositiveSmallIntegerField()
    person_quantity=models.PositiveSmallIntegerField()
    price=models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='house_images', default='default.jpg')

    def __str__(self):
        return self.name
