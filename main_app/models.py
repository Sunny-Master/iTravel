from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django_countries.fields import CountryField

D_TYPES = (
  ('O', 'Other'),
  ('C', 'City/Town/Neighborhood/Village'),
  ('B', 'Beach / Island'),
  ('W', 'Waterfall'),
  ('H', 'Hill / Mountain / Cliff'),
  ('P', 'Park / Forest / Cave'),
  ('E', 'Entertainment/Amusement Park'),
  ('Z', 'Zoo / Wildlife Attraction'),
  ('M', 'Museum / Art Gallery / Market / Festivals & Parades / Exhibition'),
  ('H', 'Historical/Heritage Attraction'),
  ('L', 'Landmark / Unique Built Attraction')
)

# Destination model
class Destination(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(
    max_length=1,
    choices=D_TYPES,
    default=D_TYPES[0][0]
  )
  country = CountryField()
  city = models.CharField('Location', max_length=100)
  date = models.DateField('Visit Date', default=date.today)
  comment = models.TextField(max_length=250)
  rating = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 11)])
  image_url = models.URLField(
    'Image URL',
    max_length=200,
    blank=True,
    null=True
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('destination-detail', kwargs={'pk': self.id})
  
  class Meta:
    ordering = ['-rating']