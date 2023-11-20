from django.shortcuts import render, get_object_or_404, redirect
from musicPlatform.models import Music, Review
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import googlemaps
# Create your views here.
class MusicListView(ListView):
    def get_queryset(self):
        return Music.objects.all()


# def index(request):
#    dbData = Music.objects.all()
#   context = {'musics': dbData}
#   return render(request, 'musicPlatform/music_list.html', context)
class MusicDetailView(DetailView):
    model = Music

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = context['music'].review_set.all().order_by('-create_at')
        return context


# def show(request, id):
#    musicList = get_object_or_404(Music, pk=id)
#   reviews = Review.objects.filter(music_id=id).order_by('-create_at')
#  context = {'music': musicList, 'reviews': reviews}
# return render(request, 'musicPlatform/music_detail.html', context)
def review(request, id):
    if request.user.is_authenticated:
        body = request.POST['review']
        newReview = Review(body=body, music_id=id, user=request.user)
        if len(request.FILES) != 0:
            image = request.FILES['image']
            fs = FileSystemStorage()
            name = fs.save(image.name, image)
            newReview.image = fs.url(name)

        newReview.save()

    return redirect(f"/musicPlatform/{id}")


class MusicSearchView(ListView):
    model = Music

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Music.objects.filter(title__icontains=query).order_by('-create_at')

class MusicSearchVoiceView(ListView):
    model = Music

    @csrf_exempt
    def audio_data(request):
        if request.method == 'POST':

            # Authenticating API
            gmaps = googlemaps.Client(key='YOUR_API_KEY')

            # Calling google geocode API with query as a Address
            geocode_result = gmaps.geocode(request.POST['send'])

            # geocode_result will return a JSON, contents can be extracted
            # for example
            x = geocode_result[0]['geometry']['location']['lat']  # get latitute for the query
            y = geocode_result[0]['geometry']['location']['lng']  # get longitude for the query

        else:
            message = "Please check the POST call"
        return HttpResponse(message)