from django.urls import path
from . import views

app_name = 'url'
urlpatterns = [
    path('', views.ShortUrlView.as_view(),name='short-url'),
    path('stats-export/<key>', views.StatsUrlExportView.as_view(),name='url-stats-export'),
    path('url/<key>', views.RedirectUrlView.as_view(),name='redirect-url'),
    path('url-check-password/<key>', views.RedirectPasswordCheckView.as_view(),name='redirect-url-password-check'),
    path('stats', views.StatsUrlView.as_view(),name='url-stats')
]
