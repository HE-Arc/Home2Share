from django.urls import path , include

import main.views as views

# Used for the local image hack
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name = 'index'),
    path('', include('django.contrib.auth.urls')),
    path('user/<slug>/', views.ProfileView.as_view(), name='profile'),
    path('user/<slug>/houses', views.UserHouseListView.as_view(), name='user-house-list'),
    path('user/<slug>/update', views.UpdateUserView.as_view(), name='user-update'),
    path('user/<slug>/house/new', views.HouseCreateView.as_view(), name='house-new'),
    path('register/',views.UserCreateView.as_view(),name='register'),
    path('houses', views.HouseListView.as_view(), name='house-list'),
    path('house/<slug>/', views.HouseDetailView.as_view(), name='house-detail'),
    path('house/<slug>/update', views.HouseUpdateView.as_view(), name='house-update'),
    path('house/<slug>/delete', views.HouseDeleteView.as_view(), name='house-delete'),
    path('account_activation_sent/',views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
]

# For media working in localhost
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
