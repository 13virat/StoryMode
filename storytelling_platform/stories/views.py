
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Story, Chapter, Comment  # Make sure Story is imported here
from .forms import StoryForm, ChapterForm, CommentForm



def story_list(request):
    stories = Story.objects.all()
    return render(request, 'stories/story_list.html', {'stories': stories})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'stories/story_detail.html', {'story': story})

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('story_detail', pk=story.pk)
    else:
        form = StoryForm()
    return render(request, 'stories/story_form.html', {'form': form})

@login_required
def story_edit(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('story_detail', pk=story.pk)
    else:
        form = StoryForm(instance=story)
    return render(request, 'stories/story_form.html', {'form': form})

@login_required
def chapter_create(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.save()
            return redirect('story_detail', pk=story_id)
    else:
        form = ChapterForm()
    return render(request, 'stories/chapter_form.html', {'form': form, 'story': story})

@login_required
def comment_create(request, story_id, chapter_id=None):
    story = get_object_or_404(Story, pk=story_id)
    chapter = None
    if chapter_id:
        chapter = get_object_or_404(Chapter, pk=chapter_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.story = story
            if chapter:
                comment.chapter = chapter
            comment.save()
            return redirect('story_detail', pk=story_id)
    else:
        form = CommentForm()
    return render(request, 'stories/comment_form.html', {'form': form, 'story': story, 'chapter': chapter})
