from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^video_gallery/$', views.ListView.as_view(), name='list_all'),
    url(r'^video_gallery/(?P<pk>[-\w]+)/$', views.DetailView.as_view(), name='detail'),
]
