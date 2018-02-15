from django.urls import path , include
from . import views

# Used for the local image hack
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name = 'index'),
    path('', include('django.contrib.auth.urls')),
    path('user/<slug>/', views.ProfileView.as_view(), name='profile'),
    path('user/<slug>/update', views.UpdateUserView.as_view(), name='user-update'),
    path('register/',views.UserCreateView.as_view(),name='register'),
    path('houses', views.HouseListView.as_view(), name='house-list'),
    path('house/<slug>/', views.HouseDetailView.as_view(), name='house-detail'),
    path('house/new', views.HouseCreateView.as_view(), name='house-new'),
    path('house/<slug>/update', views.HouseUpdateView.as_view(), name='house-update'),
    path('house/<slug>/delete', views.HouseDeleteView.as_view(), name='house-delete'),

]

# For media working in localhost
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
