from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    text        = models.TextField()
    date_time   = models.DateTimeField('Post date', auto_now_add=True)
    num_likes   = models.IntegerField()
    author      = models.ForeignKey(User, on_delete=models.CASCADE)


class Post_Likes(models.Model):
    post_id     = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_liked  = models.ForeignKey(User, on_delete=models.CASCADE)

class User_Following(models.Model):
    user_id             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user_id   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

    def __str__(self):
        f"{self.user_id} follows {self.following_user_id}"