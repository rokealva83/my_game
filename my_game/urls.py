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
                       url(r'building', 'my_game.views.building', name='building'),
                       url(r'choice_build', 'my_game.views.choice_build', name="choice_build"),
                       url(r'working', 'my_game.views.working', name='working'),
                       url(r'factory', 'my_game.views.factory', name='factory'),
                       url(r'choice_element', 'my_game.views.choice_element', name='choice_element'),
                       url(r'production', 'my_game.views.production', name='production'),
                       url(r'designingships', 'my_game.views.designingships', name='designingships'),
                       #url(r'choice_module', 'my_game.views.choice_module', name='choice_module'),
)
