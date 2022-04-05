from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.messages import ERROR, SUCCESS
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from . models import *
from django.db.models import Sum
from django.views import View


class Login(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.add_message(request, level=ERROR, message='Username/Password is incorrect')
            return redirect('login')

    def get(self, request):
        return render(request,"login.html")


class Register(View):

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, level=ERROR, message='Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.add_message(request, level=ERROR, message='Email already exists')
            else:        
                user = User.objects.create_user(username = username, first_name= first_name, last_name= last_name, email=email,password=password1)
                user.save()
                messages.add_message(request, level=SUCCESS, message='User created')
                return redirect('login')
        else:
            messages.add_message(request, level=ERROR, message='Password doesn\'t match')
        return redirect('register')                 

    def get(self, request):
        return render(request,"register.html")


class RegisterCinema(View):

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        cinema_name = request.POST['cinema']
        phone = request.POST['phone']
        city = request.POST['city']
        address = request.POST['address']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, level=ERROR, message='Username already exists')
                
            elif User.objects.filter(email=email).exists():
                messages.add_message(request, level=ERROR, message='Email already exists')
                
            else:
                user = User.objects.create_user(username = username, first_name= first_name, last_name= last_name, email=email,password=password1)
                cin_user = Cinema(cinema_name = cinema_name, phoneno = phone, city = city, address = address, user = user)
                cin_user.save()
                messages.add_message(request, level=SUCCESS, message='User created')
                
                return redirect('login')
        else:
            messages.add_message(request, level=ERROR, message='Password doesn\'t match')
            
        return redirect('register_cinema')     
                    
    def get(self, request):
        return render(request,"register_cinema.html")

class Profile(View):

    def post(self, request):
        u = request.user
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        old = request.POST['old']
        new = request.POST['new']
        user = User.objects.get(pk = u.pk)        
            
        if User.objects.filter(username=username).exclude(pk=u.pk).exists():
            messages.add_message(request, level=ERROR, message='Username already exists')
        
        elif User.objects.filter(email=email).exclude(pk=u.pk).exists():
            messages.add_message(request, level=ERROR, message='Email already exists')
        
        elif user.check_password(old):
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(new)
            user.save()
            #update session
            update_session_auth_hash(request, user)

            messages.add_message(request, level=SUCCESS, message='Profile updated')
            
        else:
            messages.add_message(request, level=ERROR, message='Wrong Old Password')
            
        return redirect('profile')
    
    def get(self, request):
        user = request.user
        return render(request,"profile.html")

class AddShows(View):

    def post(self, request):
        user = request.user
        movie = request.POST['movie']
        time = request.POST['time']
        date = request.POST['date']
        price = request.POST['price']
        i = user.cinema.pk

        show = Shows(cinema_id = i, movie_id = movie, date = date, time = time, price = price)
        show.save()
        messages.add_message(request, level=SUCCESS, message='Show Added')
        
        return redirect('add_shows')

    def get(self, request):  
        user = request.user  
        movies = Movie.objects.all()
        shows = Shows.objects.filter(cinema=user.cinema)
        data = {
            'movies':movies,
            'shows':shows
        }
        return render(request,"add_shows.html", data)

def bookings(request):
    user = request.user
    book = Bookings.objects.filter(user=user.pk)
    return render(request,"bookings.html", {'book':book} )

def dashboard(request):
    user = request.user
    m = Shows.objects.filter(cinema=user.cinema).values('movie','movie__movie_name','movie__movie_poster').distinct()
    print(m)
    return render(request,"dashboard.html", {'list':m})

def earnings(request):
    user = request.user
    d = Bookings.objects.filter(shows__cinema=user.cinema)
    total = Bookings.objects.filter(shows__cinema=user.cinema).aggregate(Sum('shows__price'))
    return render(request,"earnings.html", {'s':d, 'total':total})


def logout(request):
    auth.logout(request)
    return redirect('/')
