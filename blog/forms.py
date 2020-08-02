from django import forms
from .models import Post,Comments


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'This is my blog title'}),
            'content': forms.TextInput(attrs={'placeholder': 'This is my blog content'})
        }

class CreateComment(forms.ModelForm):
    comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add your comments here','cols': 45, 'rows': 5}), label='')
    class Meta:
        model=Comments 
        fields=['comments']
