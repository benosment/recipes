from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'recipes.views.home', name='home'),
                       url(r'^users/', include('recipes.urls')),
                       url(r'^about/', 'recipes.views.about', name='about'),
                       url(r'^contact/', 'recipes.views.contact', name='contact'),
                       )
