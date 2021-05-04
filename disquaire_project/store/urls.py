from django.urls import path, re_path
from .views import listing, detail, search

app_name = 'store'
urlpatterns = [
    # path('', views.index)

    path('', listing, name='listing'),
    re_path(r'^(?P<album_id>[0-9]+)/$', detail, name='detail'),
    re_path(r'^search/$', search, name='search'),

]
