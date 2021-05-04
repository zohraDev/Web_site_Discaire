from django.contrib import admin

# Register your models here.
from .models import Booking, Contact, Album, Artist
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


# admin.site.register(Booking)

class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%_change" % (content_type), args=(obj.id))


class BookingInline(admin.TabularInline, AdminURLMixin):
    readonly_fields = ['created_at', 'album_link', 'contacted']
    model = Booking
    fieldsets = [
        (None, {'fields': ['album_link', 'contacted']})
    ]

    extra = 0
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def has_add_permission(self, request, obj):
        return False

    def album_link(self, booking):
        # path = "admin:store_album_change"
        # url = reverse(path, args=(booking.album.pk,))

        url = self.get_admin_url(booking.album)
        return mark_safe("<a href="'{}'">{}</a>".format(url, booking.album.title))


class AlbumArtisInline(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = 'Disque'
    verbose_name_plural = 'Disques'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtisInline, ]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ['created_at', 'contact', 'album_link']
    fields = ["created_at", "album_link", "contacted"]
    list_filter = ['created_at', 'contacted']

    def has_add_permission(self, request):
        return False

    def album_link(self, booking):
        # path = "admin:store_album_change"
        # url = reverse(path, args=(booking.album.pk,))

        url = self.get_admin_url(booking.album)
        return mark_safe("<a href="'{}'">{}</a>".format(url, booking.album.title))
