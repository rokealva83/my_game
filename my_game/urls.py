from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'my_game.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^index/', 'my_game.views.home'),
                       url(r'^$', 'my_game.views.home', name='home'),
                       url(r'^registration.html', 'my_game.views.registr'),
                       url(r'regisration', 'my_game.views.registration', name='registration'),
                       url(r'admin/gener/', 'my_game.views.gener'),
                       url(r'admin/gener1', 'my_game.views.generation', name='gen1'),
                       url(r'civilization.html', 'my_game.views.auth', name='auth'),
                       url(r'civilization', 'my_game.views.civilization', name='civilization'),
                       url(r'warehouse', 'my_game.views.warehouse', name='warehouse'),
                       url(r'scientic', 'my_game.views.scientic', name='scientic'),
                       url(r'scient', 'my_game.views.scientic_up', name='scient'),
                       )
