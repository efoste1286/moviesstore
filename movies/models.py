from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def hearts_count(self):
        return self.hearts.count()

    def user_has_hearted(self, user):
        if not user.is_authenticated:
            return False
        return self.hearts.filter(user=user).exists()

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Heart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="movie_hearts"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="hearts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user} ♥ {self.movie}"

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # convenience
    def yes_count(self):
        return self.petitionvote_set.count()

    def __str__(self):
        return self.title


class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("petition", "user") 