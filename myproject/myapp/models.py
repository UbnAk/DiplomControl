
from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=8, choices=(
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ))
    
    
# class Reaction(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reaction = models.CharField(max_length=10, choices=(
#         ('like', 'Like'),
#         ('dislike', 'Dislike'),
#     ))

