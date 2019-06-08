from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# waits until you've actually deleted a post to give you back the success url
from django.urls import reverse_lazy
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


# the actual homepage is going to be a list of all the posts
class PostListView(ListView):
    # this is all you have to do and you will be provided with a list of all entries/records in this model
    # The ListView does all this for you
    model = Post

    # similar to a SQL query on your model
    # grab all the objects on the post model and filter out based on the field you want and the lookup type
    # give me stuff that's been published
    def get_queryset(self):
        # lte means less than or equal to
        # the dash - orders them in a descending order, so that the most recent comes up front
        # SELECT * FROM posts WHERE pub_date <= now;
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# click on an actual post, go to the detail of that post
class PostDetailView(DetailView):
    model = Post


# we want an authenticated user to be able to create a post
# instead of a decorator for a function based view, use mixins for a CBV

# inherit methods from both the LoginRequiredMixin and CreateView classes
class CreatePostView(LoginRequiredMixin, CreateView):
    # in case a person is not logged in, where should they go
    login_url = '/login/'
    # redirect them to the DetailView
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # in case a person is not logged in, where should they go
    login_url = '/login/'
    # redirect them to the DetailView
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    # connect it to the model we are deleting from
    model = Post
    # where should you go when you actually delete it
    # we don't want this url to activate until you've deleted the post
    # so use reverse lazy to wait until a post is deleted
    # then go back to the homepage
    success_url = reverse_lazy('post_list')


# create a view that lists all my unpublished drafts
# looks a lot like the PostListView but lists only those posts
# which don't have a published date
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        # make sure it doesn't have a published date
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
