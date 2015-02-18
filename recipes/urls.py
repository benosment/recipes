from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^new$', 'recipes.views.add_user', name='add_user'),
                       url(r'^(\d+)/$', 'recipes.views.user', name='user'),
                       url(r'(\d+)/add_recipe$', 'recipes.views.add_recipe', name='add_recipe'),
                       url(r'(\d+)/recipe/([a-z\-]+)$', 'recipes.views.view_recipe', name='view_recipe'),
                       url(r'(\d+)/recipe/([a-z\-]+)/edit$', 'recipes.views.edit_recipe', name='edit_recipe'),
                       )
