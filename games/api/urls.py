from django.urls import path

from games.api.views import ApiGameListView

app_name = 'games'

urlpatterns = [
    path('all-games/', ApiGameListView.as_view(), name='all games')
]