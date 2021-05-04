from django.shortcuts import render, get_object_or_404
from .models import Album, Artist, Contact, Booking
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from .forms import ContactForm, ParagraphErrorList


# Create your views here.
def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]  # 12 premier résulta
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Album.objects.filter(available=True)  # 12 premier résulta
    paginator = Paginator(albums_list, 9)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)

    context = {
        'albums': albums,
        'paginate': True,
    }
    return render(request, 'store/listing.html', context)


# @transaction.atomic()
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    artists_name = " ".join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form
            email = form.cleaned_data['email']
            # email = request.POST.get('email')
            # name = request.POST.get('name')
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        print('-----------------------------')
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                        print('-----------------------------')
                    else:
                        contact = contact.first()

                    album = get_object_or_404(Album, pk=album_id)
                    Booking.objects.create(
                        contact=contact,
                        album=album
                    )
                    album.available = False
                    album.save()
                    context = {
                        'album_title': album.title
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête. "
    else:

        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)


def search(request):
    query = request.GET.get('query')
    print(query)
    if not query:
        albums = Album.objects.all()
        # message = "Aucun artiste n'est demandé"
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():  # vérifier si la query est vide ou pas
            albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultat pour la requête %s" % query
    context = {
        'albums': albums,
        'title': title,
    }

    return render(request, 'store/search.html', context)
