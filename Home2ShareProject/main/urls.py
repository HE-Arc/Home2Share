from django.urls import path
from . import views

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name = 'index'),
    path('houses', views.HouseListView.as_view(), name='house-list'),
    path('house/<pk>/', views.HouseDetailView.as_view(), name='house-detail'),
]

# For media working in localhost

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
