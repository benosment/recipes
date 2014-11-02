from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'recipes.views.home', name='home'),
                       url(r'^users/new$', 'recipes.views.add_user', name='add_user'),
                       url(r'^users/(\d+)/$', 'recipes.views.user', name='user'),
                       url(r'^users/(\d+)/recipe/new$', 'recipes.views.add_recipe', name='add_recipe'),
                       )
