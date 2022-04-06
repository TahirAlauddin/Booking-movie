from django.db import models
from django.contrib.auth.models import User


class Cinema(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=30,default='cinema_manager')
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    owner = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
    class Meta:
        managed = True

class Movie(models.Model):
    name = models.CharField(max_length=50)
    trailer = models.CharField(max_length=300, default="null")
    rdate = models.CharField(max_length=20, default="null")
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    poster = models.ImageField(upload_to='movies/poster', default="movies/poster/not.jpg")
    genre = models.CharField(max_length=50,default="Action | Comedy | Romance")
    duration = models.CharField(max_length=10, default="2hr 45min")

    def __str__(self):
        return self.name


class Shows(models.Model):
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='cinema_show')
    movie = models.ForeignKey('Movie',on_delete=models.CASCADE, related_name='show')
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=15, default="")
    price = models.IntegerField()

    def __str__(self):
        return self.cinema.name +" | "+ self.movie.name +" | "+ self.time


class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shows = models.ForeignKey(Shows, on_delete=models.CASCADE)
    useat = models.CharField(max_length=100)
    
    @property
    def useat_as_list(self):
        return self.useat.split(',')
    def __str__(self):
        return self.user.username +" | "+ self.shows.movie.name +" | "+ self.useat

