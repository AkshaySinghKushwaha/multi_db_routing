from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$', views.user_dashboard, name='home'),
	url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'logout.html'}, name='logout'),
    url(r'^create-user/$', views.admin_dashboard, name='admin_dashboard'), 
    url(r'^product-details/$', views.product_details, name='product_details'), 
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]