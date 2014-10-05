from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'recipes.views.home', name='home'),
                       url(r'^recipe/add$', 'recipes.views.add', name='add'),
                       )
