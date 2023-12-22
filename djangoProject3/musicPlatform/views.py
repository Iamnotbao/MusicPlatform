from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from musicPlatform.models import Music, Review
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import re

from django.http import HttpResponse, JsonResponse
import googlemaps

import openai

from .models import Chat

from django.utils import timezone

openai_api_key = 'your api key'
openai.api_key = openai_api_key


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                return redirect('register')
            except:
                error_message = 'Error creating account'
                return render(request, 'registration/register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'registration/register.html', {'error_message': error_message})
    return render(request, 'registration/register.html')


class MusicListView(ListView):
    def get_queryset(self):
        return Music.objects.all()

    def ask_openai(self, message):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are an helpful assistant."},
                {"role": "user", "content": message},
            ]
        )

        answer = response.choices[0].message.content.strip()
        return answer

    def post(self, request):
        message = request.POST.get('message')
        response = self.ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})

    def get(self, request):
        chats = Chat.objects.filter(user=request.user.id)
        musics = Music.objects.all()
        return render(request, 'musicPlatform/music_list.html', {'chats': chats, 'music_list': musics})


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
        query = re.sub('[.]', '', query)
        if Music.objects.filter(title__icontains=query).order_by('-create_at'):
            self.request.session['search_by_title'] = query
            print(self.request.session['search_by_title'])
        elif not Music.objects.filter(title__icontains=query).order_by('-create_at'):
            self.request.session['search_by_title'] = 'none'

        return Music.objects.filter(title__icontains=query).order_by('-create_at')
