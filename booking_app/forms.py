# booking_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking, Feedback, Conference, Speaker, Payment

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

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('credit_card', 'Credit Card'),
                ('debit_card', 'Debit Card'),
                ('paypal', 'PayPal'),
            ]),
        }
    
    # Credit card fields (for demo purposes)
    card_number = forms.CharField(max_length=16, required=False)
    card_holder = forms.CharField(max_length=100, required=False)
    expiry_date = forms.CharField(max_length=5, required=False, help_text="Format: MM/YY")
    cvv = forms.CharField(max_length=4, required=False)

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