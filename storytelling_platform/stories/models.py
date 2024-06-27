

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_stories')  # Unique related_name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')  # Use the actual model name 'Story'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Chapter, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')  # Specify unique related_name
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_comments')  # Use a different related_name
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, related_name='chapter_comments')  # Use a different related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.chapter:
            return f'Comment by {self.author.username} on Chapter "{self.chapter.title}"'
        else:
            return f'Comment by {self.author.username} on Story "{self.story.title}"'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Unique related_name
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
