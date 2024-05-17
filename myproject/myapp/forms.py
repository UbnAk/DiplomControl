from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from .models import PostReaction

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

class PostReactionForm(forms.ModelForm):
    reaction_type = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = PostReaction
        fields = ('reaction', 'reaction_type')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
       
        
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None