from django.urls import path

from . import views

app_name = 'crawler'
urlpatterns = [
    path('', views.crawler, name='crawler'),
    path('crawler', views.crawler, name='crawlers'),
    path('download', views.download, name='download')
]