from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import (TemplateView, ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# waits until you've actually deleted a post to give you back the success url
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
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
        # can be used to create a wishlist/favorite item list
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
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


############################
############################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    # the pk used is the primary key provided as a parameter
    # it links the comment to the post
    post = get_object_or_404(Post, pk=pk)

    # someone actually filled in the form and hit enter
    if request.method == "POST":
        # this form will be injected into the HTML through the context dictionary
        form = CommentForm(request.POST)
        if form.is_valid():
            # have at least some sort of form in memory
            comment = form.save(commit=False)
            # connect that particular comment's post attribute to the post object
            comment.post = post
            # now save it
            comment.save()
            return redirect('post_detail', pk=post.pk)

    # if someone has not filled out the comment form
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    # grab the comment in this case
    comment = get_object_or_404(Comment, pk=pk)
    # set the property to true while it was false by default in the models
    comment.approve()
    # what happens once you approve a comment?
    # to go to the post of that comment, you need post.pk
    # asking what's the pk of the post that this comment was linked to
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # by the time you get to redirect, it's not gonna remember what the pk was
    # so necessary to store it before hand
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', post_pk)
