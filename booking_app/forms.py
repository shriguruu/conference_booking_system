# booking_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking, Feedback, Conference, Speaker

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=45, required=True)
    last_name = forms.CharField(max_length=45, required=True)
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['conference']
        widgets = {
            'conference': forms.HiddenInput(),
        }

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = Feedback
        fields = ['comments', 'rating']

class ConferenceSearchForm(forms.Form):
    topic = forms.CharField(required=False)
    category = forms.CharField(required=False)
    speaker = forms.ModelChoiceField(queryset=Speaker.objects.all(), required=False)