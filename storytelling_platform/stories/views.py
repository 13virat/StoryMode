
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Story, Chapter, Comment, UserProfile  # Make sure Story is imported here
from .forms import StoryForm, ChapterForm, CommentForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.cache import cache_page



@login_required
@cache_page(60 * 15)
def story_list(request):
    stories = Story.objects.select_related('author').all()
    paginator = Paginator(stories, 10)  # Show 10 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stories/story_list.html', {'page_obj': page_obj})

@cache_page(60 * 15)
def story_detail(request, pk):
    story = get_object_or_404(Story.objects.select_related('author'), pk=pk)
    chapters = Chapter.objects.filter(story=story).select_related('story')
    comments = Comment.objects.filter(story=story).select_related('author', 'chapter')
    context = {
        'story': story,
        'chapters': chapters,
        'comments': comments,
    }
    return render(request, 'stories/story_detail.html', context)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('story_list')  # Redirect to story list after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('story_list')  # Redirect to story list after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('story_list')  # Redirect to story list after logout

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

@login_required
def profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    return render(request, 'profile.html', {'profile': user_profile})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})
@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'stories/user_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'stories/edit_profile.html', {'form': form})

@login_required
def search(request):
    query = request.GET.get('q')
    stories = Story.objects.filter(title__icontains=query)
    chapters = Chapter.objects.filter(title__icontains=query)
    comments = Comment.objects.filter(content__icontains=query)
    return render(request, 'stories/search_results.html', {'stories': stories, 'chapters': chapters, 'comments': comments})

def story_search(request):
    query = request.GET.get('q')
    if query:
        results = Story.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        results = Story.objects.all()
    return render(request, 'stories/story_search.html', {'results': results, 'query': query})
@login_required
def user_dashboard(request):
    user_stories = Story.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(author=request.user)
    context = {
        'user_stories': user_stories,
        'user_comments': user_comments,
    }
    return render(request, 'stories/user_dashboard.html', context)