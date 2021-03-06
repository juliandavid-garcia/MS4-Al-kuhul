from django.db import models
from profiles.models import UserProfile

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=900, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    date_added = models.DateTimeField(auto_now_add=True)