from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for submitting comments. The form includes fields for the user's email,
    username, optional home page URL, the comment text, and a captcha verification
    field. The form is tied to the `Comment` model for saving data to the database.
    """

    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, max_length=150)
    home_page = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField(generator='comment.utils.generate_alphanumeric_captcha')

    class Meta:
        model = Comment
        fields = ['email', 'username', 'home_page', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and pre-fills email and username fields with
        the current user's data if the user is authenticated.
        """
        user = kwargs.get('user')
        if user and user.is_authenticated:
            kwargs['initial'] = {
                'email': user.email,
                'username': user.username
            }
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Saves the form instance and creates or updates the associated `User` object based on
        the provided email. If a user with the given email already exists, the username is
        updated to ensure its uniqueness by appending the user ID to it.

        The `Comment` instance is saved with a reference to the created or updated `User` object.
        The `comment.save()` method is called to persist the comment to the database if `commit` is True.
        """
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        user, created = User.objects.get_or_create(email=email, defaults={'username': username})
        if not created:
            username = f"{username}_{user.id}"
            user.username = username
            user.save()

        comment = super().save(commit=False)
        comment.user = user
        if commit:
            comment.save()
        return comment

