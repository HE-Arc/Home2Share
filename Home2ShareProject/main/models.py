from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class House(models.Model):
    name=models.CharField(max_length=200, unique=True)
    slug_name = models.SlugField(unique=True, editable=False)

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

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug_name = slugify(self.name)

        super(House, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
