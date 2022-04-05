from django.shortcuts import render
from accounts.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request,"index.html", context)

def movies(request, id):
    movies = Movie.objects.get(movie=id)
    cinema = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()  # get all cinema
    show = Shows.objects.filter(movie=id)
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
