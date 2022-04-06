from django.shortcuts import render
from accounts.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib.messages import SUCCESS 

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request,"index.html", context)

def movies(request, id):
    movies = Movie.objects.get(id=id)
    cinema = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()  # get all cinema
    show = Shows.objects.filter(movie=id)
    print(movies)
    print(cinema)
    context = {
        'movies':movies,
        'show':show,
        'cinemas':cinema,
    }
    return render(request, "movies.html", context )

def seat(request, id):
    show = Shows.objects.get(shows=id)
    seat = Bookings.objects.filter(shows=id)
    return render(request,"seat.html", {'show':show, 'seat':seat})    

class Booked(View):
    def post(self, request):
        user = request.user
        seat = ','.join(request.POST.getlist('check'))
        show = request.POST['show']
        book = Bookings(useat=seat, shows_id=show, user=user)
        book.save()
        return render(request,"booked.html", {'book':book})  

    def get(self, request):
        return HttpResponse("Page Not available for get request!")  
        

def ticket(request, id):
    ticket = Bookings.objects.get(id=id)
    return render(request,"ticket.html", {'ticket':ticket})

def dummy(request):
    messages.add_message(request, level=SUCCESS, message="here we are")
    return render(request, 'dummy.html')