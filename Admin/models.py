from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts' ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    caption = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.caption

class Like(models.Model):
    liked_by = models.ForeignKey(User, related_name='liked_by', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='liked_post', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment_user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_post', on_delete=models.CASCADE)
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_flagged = models.BooleanField(default=False)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)
