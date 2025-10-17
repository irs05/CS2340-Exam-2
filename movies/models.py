from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model): # controls model properties
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    amount_left = models.PositiveIntegerField(default=1) #new
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0) # new
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=0) # new
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

# --- Trending by Region ---
class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class MovieRegionStat(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='region_stats')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='movie_stats')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('movie', 'region')
        indexes = [
            models.Index(fields=['movie', 'region']),
        ]

    def __str__(self):
        return f"{self.movie.name} @ {self.region.name}: {self.views}"
