from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^([a-z]+)/$', 'recipes.views.user', name='user'),
                       url(r'^([a-z]+)/add_recipe$', 'recipes.views.add_recipe', name='add_recipe'),
                       url(r'^([a-z]+)/export$', 'recipes.views.export', name='export'),
                       url(r'^([a-z]+)/recipe/([a-z\-]+)$', 'recipes.views.view_recipe', name='view_recipe'),
                       url(r'^([a-z]+)/recipe/([a-z\-]+)/edit$', 'recipes.views.edit_recipe', name='edit_recipe'),
                       )
