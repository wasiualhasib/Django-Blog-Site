from time import timezone
from .models import Post,Comments
from .forms import CreateComment
from django.shortcuts import render, get_object_or_404,redirect,redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.views.generic import \
    (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.urls import resolve
from .forms import CreateBlogForm
from .models import Post


# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# def my_post(request):
#     my_id=request.user.id
#     context = {
#         'posts': Post.objects.filter(my_id).all()
#     }
#     return render(request, 'blog/home_mypost.html', context)
#
class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home_mypost.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.request.user.id).order_by('-date_posted')

class DraftPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/draft_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(post_published=False).filter(author_id=self.request.user.id).all()

def PublishPost(request,pk,url_name):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    post.save()
    current_url = url_name
    print(url_name)
    return redirect(current_url)


def UnPublishPost(request,pk,url_name):
    post=get_object_or_404(Post,pk=pk)
    post.unPublish()
    post.save()
    current_url = url_name
    print(url_name)
    return redirect(current_url)


    

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(post_published=True).all()

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        comment=CreateComment()
        context['form'] = comment
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateBlogForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['title', 'content']  # model_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def add_comments_to_post(request,pk):
    
    post=get_object_or_404(Post,pk=pk)
    form=CreateComment()
    
    if request.method=='POST':
        form=CreateComment(request.POST)
        
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect('post-detail',pk=post.pk) 
    else:
        return redirect('post-detail',pk=post.pk)
    
def remove_comments(request,pk):
    post_comment=get_object_or_404(Comments,pk=pk)
    post_comment.delete()
    post_id=post_comment.post.pk
    return redirect('post-detail',pk=post_id)
    
def publish_comments(request,pk):
    post_comment=get_object_or_404(Comments,pk=pk)
    post_comment.approve()
    post_comment.save()
    return redirect('post-detail',pk=post_comment.post.pk)

class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comments
    form=CreateComment()
    template_name = 'blog/update_comments.html'
    fields = ['comments',]  # model_form.html
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #we can pass context and also we can pass form_valid() function
    
    