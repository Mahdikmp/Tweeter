from django import forms
from .models import Tweet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User




class TweetForm(forms.ModelForm):
    body = forms.CharField(max_length=250, required=True, label=False, widget=forms.widgets.Textarea(attrs={'placeholder': 'Enter your Tweet', 'class': 'form-control'}))

    class Meta:
        model = Tweet
        exclude = ('user', 'likes')

    



class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label='', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
        }



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

        widgets = {'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your biography'})}




class PassChangeForm(PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'




class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']


        widgets = {'profile_image': forms.FileInput(attrs={'class': 'form-control'})}



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Type your comment ...', 'rows': 2, 'required': 'required'})}
    



class TweetEditForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['body']

        widgets = {'body': forms.TextInput(attrs={'class': 'form-control'})}