from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # Define fields explicitly to match your desired template placeholders
    author_name = forms.CharField(
        max_length=80, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Display Name',
            'title': 'Name displayed with your comment',
            'class': 'w-full p-2 border border-gray-300 rounded-lg text-gray-800'
        })
    )
    author_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email (for Gravatar)',
            'title': 'Email used for avatar/identity only',
            'class': 'w-full p-2 border border-gray-300 rounded-lg text-gray-800'
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Join the discussion...',
            'rows': 4,
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-gray-800 resize-y'
        })
    )

    class Meta:
        model = Comment
        fields = ('author_name', 'author_email', 'body')