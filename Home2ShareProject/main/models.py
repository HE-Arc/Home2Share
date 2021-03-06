from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    user = models.ForeignKey(User, related_name='houses', on_delete=models.CASCADE)
    evaluations = models.ManyToManyField(User, through='Evaluation', related_name='evaluations_houses')
    comments = models.ManyToManyField(User, through='Comment', related_name='comments_houses')
    pub_date = models.DateTimeField('Added on', auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Voir commentaire : https://github.com/HE-Arc/Home2Share/commit/2640e440612c46b9a03ff92a1c7e0426e9af822f#comments
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug_name = slugify(self.name)

        super(House, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    stars = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Comment(models.Model):
    body = models.TextField('Message', max_length=255)
    last_modif_date = models.DateTimeField('last modification', auto_now=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
