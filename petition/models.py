from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="voters")
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name