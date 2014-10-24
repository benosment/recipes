from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'recipes.views.home', name='home'),
                       url(r'^users/ben/$', 'recipes.views.user', name='user'),
                       url(r'^users/ben/add_recipe$', 'recipes.views.add', name='add'),
                       )
