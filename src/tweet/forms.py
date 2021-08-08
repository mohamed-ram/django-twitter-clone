from ckeditor.fields import RichTextField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': "Create New Tweet..",
    }))
    
    class Meta:
        model = Tweet
        fields = ['content']


class RetweetForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': "Retweet..",
        'class': 'retweet-input'
    }))
    
    class Meta:
        model = Tweet
        fields = ['content']

