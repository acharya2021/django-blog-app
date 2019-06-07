from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        # connect the model we are using
        model = Post
        # connect the fields the user can edit in this form
        fields = ('author', 'title', 'text')

        # this is so that you can grab a particular field and style it with CSS
        widgets = {
            # the class name comes from the medium.com library
            # TextInput is a type of widget
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            # postcontent and textinputclass are our own classes
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
