from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Album, Song
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .form import UserRegister
from django.urls import reverse_lazy
from music.Coding import corona_api


def main_pg(request):
    return redirect('music:index')


def index(request):
    if request.method == 'POST':
        find_text = request.POST['search']
        if find_text:
            album_with_title = Album.objects.filter(album_title__startswith=find_text)
            album_with_artist = Album.objects.filter(artist__startswith=find_text)
            if album_with_title:
                return render(request, 'music/index.html', {'album': album_with_title[0]})
            elif album_with_artist:
                return render(request, 'music/index.html', {'album': album_with_artist[0]})
            else:
                msg1 = f'No results found for "{find_text}"'
                msg2 = 'please check your spelling or try with a different keyword'
                return render(request, 'music/index.html', {'msg1': msg1, 'msg2': msg2})
    all_albums = Album.objects.all()
    return render(request, 'music/Index.html', {
        'albums': all_albums,
        'india_confirmed': corona_api.india_confirmed,
        'india_active': corona_api.india_active,
        'india_deaths': corona_api.india_deaths,
        'india_recover': corona_api.india_recover,
        'maha_recovered': corona_api.maha_recovered,
        'maha_confirmed': corona_api.maha_confirmed,
        'mumbai_confirmed': corona_api.mumbai_confirmed,
        'india_per_active': corona_api.india_per_active,
        'india_per_recover': corona_api.india_per_recover,
        'india_per_deaths': corona_api.india_per_deaths,
        'maha_per_recover': corona_api.maha_per_recover,
        'mum_per_india': corona_api.mum_per_india,
        })


def details(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'music/Details.html', {'album': album})


# def album_search(request):
#     if request.method == 'POST':
#         find_text = request.POST['search']
#         album = Album.objects.filter(album_title__startswith=find_text)
#         if album:
#             return render(request, 'music/index.html', {'album': album})
#         else:
#             album = Album.objects.filter(artist__startswith=find_text)
#             if album:
#                 return render(request, 'music/index.html', {'album': album})
#     error_message = 'album not found'
#     return render(request, 'music/index_search.html', {'error_message': error_message})


def songs(request):
    if request.method == 'POST':
        find_text = request.POST['search']
        if find_text:
            song_with_title = Song.objects.filter(song_title__startswith=find_text)
            if song_with_title:
                return render(request, 'music/Songs.html', {'song': song_with_title[0]})
            else:
                msg1 = f'No results found for "{find_text}"'
                msg2 = 'please check your spelling or try with a different keyword'
                return render(request, 'music/Songs.html', {'msg1': msg1, 'msg2': msg2})
    songs = Song.objects.all()
    template = 'music/Songs.html'
    return render(request, template, {'all_songs': songs})


def song_page_fav(request, song_pk):
    song = get_object_or_404(Song, pk=song_pk)
    if song.is_favorite:
        song.is_favorite = False
    else:
        song.is_favorite = True
    song.save()
    return redirect('music:songs')


def song_page_del(request, song_pk):
    song = get_object_or_404(Song, pk=song_pk)
    song.delete()
    return redirect('music:songs')


def album_favorite(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if album.is_favorite:
        album.is_favorite = False
    else:
        album.is_favorite = True
    album.save()
    return redirect('music:index')


def song_favorite(request, pk, song_pk):
    album = get_object_or_404(Album, pk=pk)
    song = get_object_or_404(Song, pk=song_pk)
    if song.is_favorite:
        song.is_favorite = False
    else:
        song.is_favorite = True
    song.save()
    return redirect('music:details', album.id)


# def add_album(request):
#     if request.method == 'POST':
#         artist = request.POST['artst']
#
#     return render(request, 'music/AddAlbum.html', {})

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


def song_create(request):
    if request.method == 'GET':
        all_albums = Album.objects.all()
        if not all_albums:
            msg1 = f'Cannot add songs without any album'
            msg2 = 'please add at least one album to add any songs to it'
            return render(request, 'music/song_form.html', {'msg1': msg1, 'msg2': msg2})
        return render(request, 'music/song_form.html', {'all_albums': all_albums})
    if request.method == 'POST':
        song = Song()
        song.song_title = request.POST['song_title']
        song.audio_file = request.FILES['audio_file']
        album_id = request.POST['sel']
        album = get_object_or_404(Album, pk=album_id)
        song.album = album
        song.save()
    return redirect('music:songs')


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def song_delete(request, pk, song_pk):
    album = get_object_or_404(Album, pk=pk)
    song = get_object_or_404(Song, pk=song_pk)
    song.delete()
    return redirect('music:details', album.id)


# class SongCreate(CreateView):
#     model = Song
#
#     def dispatch(self, request, *args, **kwargs):
#         """
#         Overridden so we can make sure the `Ipsum` instance exists
#         before going any further.
#         """
#         self.album = get_object_or_404(Album, pk=kwargs['pk'])
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.album = self.album
#         return super().form_valid(form)

class UserFormView(View):
    form_class = UserRegister
    template_name = 'music/register_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


def add_song(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':

        song = Song()

        song.song_title = request.POST['song_title']
        song.audio_file = request.FILES['f-msc']
        song.album = album

        song.save()

    return redirect('music:details', album.id)




# class SongCreateView(View):
#     form_class = SongCreateForm
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             song = form.save(commit=False)
#
#             song_title =

































