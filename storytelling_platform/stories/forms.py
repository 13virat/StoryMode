from django import forms
from .models import Story, Chapter, Comment

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        