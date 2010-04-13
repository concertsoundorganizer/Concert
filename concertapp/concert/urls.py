from django.conf.urls.defaults import *

urlpatterns = patterns('concertapp.concert.views',
    url(r'^login$', 'dumb_login', name='login'),
    url(r'^logout$', 'dumb_logout', name='logout'),
    url(r'^register$', 'dumb_registration', name='registration'),
    url(r'^$', 'posts', name='posts'),
    # Users
    (r'^users/', include('concertapp.concert.users.urls')),
    # Audio
    (r'^audio/', include('concertapp.concert.audio.urls')),
    # Groups
    (r'^groups/', include('concertapp.concert.groups.urls')),
    # Blog content
    url(r'^add/$','create_post', name='create_post'),
    url(r'^ajaxy_add/$','create_ajaxy_post', name='create_ajaxy_post'),
)
