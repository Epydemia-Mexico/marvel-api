from django.contrib import admin
from django.urls import path

from dashboard.views import HomeView, ComicsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('comics', ComicsView.as_view(), name='comics'),
]
