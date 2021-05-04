from django.db import models


# Create your models here.

class Artist(models.Model):
    name = models.CharField('Nom ', max_length=200, unique=True)

    class Meta:
        verbose_name = "artist"

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField('Nom ', max_length=200)
    name = models.CharField('Email ', max_length=200)

    class Meta:
        verbose_name = "prospect"

    def __str__(self):
        return self.name


class Album(models.Model):
    reference = models.IntegerField('Réference', null=True)
    created_at = models.DateField('Date de création', auto_now_add=True)
    available = models.BooleanField('Disponible', default=True)
    title = models.CharField('Titre', max_length=200)
    picture = models.URLField("Url de l'image", )
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    class Meta:
        verbose_name = 'Disque'

    def __str__(self):
        return self.title


class Booking(models.Model):
    created_at = models.DateField("Date d'envoi", auto_now_add=True)
    contacted = models.BooleanField("Demande traitée", default=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    album = models.OneToOneField(Album, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "réservation"

    def __str__(self):
        return self.contact.name

# ARTISTS = {
#  'francis-cabre': {'name': 'Francis Cabrel'},
# 'lej': {'name': 'Elija'},
# 'rosana': {'name': 'Rosana'},
# 'mario-dolores-pradera': {'name': 'Maria Dolores Pradera'},

# }

# ALBUMS = [
#   {'name': 'Sarbacane', 'artists': [ARTISTS['francis-cabre']]},
#  {'name': 'La Dalle', 'artists': [ARTISTS['lej']]},
# {'name': 'Luna Nueva', 'artists': [ARTISTS['rosana'], ARTISTS['mario-dolores-pradera']]},

# ]
