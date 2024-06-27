
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, Permission
from django.utils.text import slugify

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ('can_publish_story', 'Can publish story'),
            ('can_edit_story', 'Can edit own story'),
            ('can_delete_story', 'Can delete own story'),
        ]

    def __str__(self):
        return self.title

@receiver(post_save, sender=Story)
def send_story_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = f'New Story Created: {instance.title}'
        message = f'Hi {instance.author.username},\n\nYour new story "{instance.title}" has been successfully created on Storytelling Platform.\n\nRead it here: example.com/{instance.pk}/\n\nBest regards,\nStorytelling Platform Team'
        sender_email = 'your-email@example.com'
        recipient_list = [instance.author.email]
        send_mail(subject, message, sender_email, recipient_list, fail_silently=True)

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='story_comments')
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, null=True, blank=True, related_name='chapter_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.chapter:
            return f'Comment by {self.author.username} on Chapter "{self.chapter.title}"'
        else:
            return f'Comment by {self.author.username} on Story "{self.story.title}"'

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    subject = f'New Comment on {instance.story.title}'
    message = f'Hi {instance.story.author.username},\n\n{instance.author.username} commented on your story "{instance.story.title}".\n\nRead it here: example.com/{instance.story.pk}/\n\nBest regards,\nStorytelling Platform Team'
    sender_email = 'your-email@example.com'
    recipient_list = [instance.story.author.email]
    send_mail(subject, message, sender_email, recipient_list, fail_silently=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Unique related_name
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
