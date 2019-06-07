from django.db import models
from django.utils import timezone

# after someone creates a post, where should the website take them?
from django.urls import reverse


# Create your models here.

# each blog post is going to connect to a model or a database

# each model serves as a unique table storing information about data and behavior (method)
# that's why it is a python class
class Post(models.Model):
    # the superuser can author new posts. This is a single-user blog.
    # Only that user should be able to author new posts.
    author = models.ForeignKey('auth.User', on_delete='CASCADE')
    title = models.CharField(max_length=200)
    # don't put max-length because you don't know how long the text is going to be
    text = models.TextField()
    # this is how you add the date the post was created, at the current timezone
    create_date = models.DateTimeField(default=timezone.now())
    # blank because maybe you don't want to publish it yet
    # null because you don't have any pub date whatsoever
    published_date = models.DateTimeField(blank=True, null=True)

    # now create some methods on it

    # when you hit the publish button, call this method
    def publish(self):
        self.published_date = timezone.now()
        # save this information on the database
        self.save()

    # posts can have comments on them. They need to be approved by the superuser
    def approve_comments(self):
        # eventually I will have a list of comments somewhere
        # some of them are going to be approved, while others are not
        # grab those comments and filter them by saying this is a truly approved comment
        # then you can show only the approved comments beneath the post

        # since the comment class is connected to post via a foreign key, comment + s = comments
        return self.comments.filter(approved_comment=True)

    # once you've created an instance of this post, what should I do?
    def get_absolute_url(self):
        # go to that post_detail page
        # using the primary key of that post you just created

        # to inject something as a context dictionary
        # **kwargs gives you all keyword arguments as a dictionary, name value pair
        # so take key word arguments and treat them as a dictionary
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    # connect each comment to a blog application post
    # the related name will make sense with the views
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete='CASCADE')
    # the author of a comment is not the same as the author of a post
    author = models.CharField(max_length=200)
    text = models.TextField()
    # once you hit create comment, that DateTimeField should be put into place
    create_date = models.DateTimeField(default=timezone.now())
    # by default, it will not have been approved
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        # save this information on the database
        self.save()

    # once that person is done making a comment and pending approval,
    # that person should be redirected to a list of all posts
    def get_absolute_url(self):
        # the list view is the homepage for this website
        # a list of all the posts
        return reverse('post_list')

    def __str__(self):
        return self.text
