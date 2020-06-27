from django.urls import path
from . import views

app_name = 'music'


urlpatterns = [
    path('', views.index, name='index'),
    # path('search<str:find_text>/', views.index, name='index'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/delete-album/', views.AlbumDelete.as_view(), name='album-delete'),
    path('<int:pk>/add-song/', views.add_song, name='add-song'),
    path('<int:pk>/delete-song/<int:song_pk>/', views.song_delete, name='song-delete'),
    path('<int:pk>/album-favorite/', views.album_favorite, name='album_favorite'),
    path('<int:pk>/song-favorite/<int:song_pk>/', views.song_favorite, name='song_favorite'),
    path('songs/', views.songs, name='songs'),
    path('songs/song-favorite/<int:song_pk>', views.song_page_fav, name='song_page_fav'),
    path('songs/song-delete/<int:song_pk>', views.song_page_del, name='song_page_del'),
    path('songs/add-song/', views.song_create, name='song-create'),
    path('add-album/', views.AlbumCreate.as_view(), name='add-album'),
    # path('register/', views.UserFormView.as_view(), name='register'),
]
