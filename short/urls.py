from django.urls import path
from . import views

app_name = 'url'
urlpatterns = [
    path('', views.ShortUrlView.as_view(),name='short-url'),
    path('url/<key>', views.RedirectUrlView.as_view(),name='redirect-url'),
    path('stats', views.StatsUrlView.as_view(),name='url-stats')
]
