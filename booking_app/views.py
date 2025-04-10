# booking_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import User, Conference, Booking, Feedback, Speaker
from .forms import UserRegistrationForm, BookingForm, FeedbackForm, ConferenceSearchForm

def home_view(request):
    conferences = Conference.objects.all().order_by('time_start')[:5]
    return render(request, 'booking_app/home.html', {'conferences': conferences})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'booking_app/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

def conferences_view(request):
    search_form = ConferenceSearchForm(request.GET)
    conferences = Conference.objects.all()
    
    if search_form.is_valid():
        topic = search_form.cleaned_data.get('topic')
        category = search_form.cleaned_data.get('category')
        speaker = search_form.cleaned_data.get('speaker')
        
        if topic:
            conferences = conferences.filter(topic__icontains=topic)
        if category:
            conferences = conferences.filter(categories__category__icontains=category)
        if speaker:
            conferences = conferences.filter(speakers=speaker)
    
    return render(request, 'booking_app/conferences.html', {
        'conferences': conferences,
        'search_form': search_form
    })

def conference_detail_view(request, slug):
    conference = get_object_or_404(Conference, slug=slug)
    speakers = conference.speakers.all()
    can_book = True
    
    # Calculate spots left
    bookings_count = Booking.objects.filter(conference=conference, status='confirmed').count()
    spots_left = conference.capacity - bookings_count
    
    if request.user.is_authenticated:
        # Check if the user has already booked this conference
        already_booked = Booking.objects.filter(user=request.user, conference=conference).exists()
        # Check if the conference is at capacity
        at_capacity = bookings_count >= conference.capacity
        
        can_book = not already_booked and not at_capacity
        
    return render(request, 'booking_app/conference_detail.html', {
        'conference': conference,
        'speakers': speakers,
        'can_book': can_book,
        'spots_left': spots_left
    })

@login_required
def booking_view(request, slug):
    conference = get_object_or_404(Conference, slug=slug)
    
    # Check if the user has already booked this conference
    already_booked = Booking.objects.filter(user=request.user, conference=conference).exists()
    if already_booked:
        messages.error(request, 'You have already booked this conference.')
        return redirect('conference_detail', slug=slug)
    
    # Check if the conference is at capacity
    bookings_count = Booking.objects.filter(conference=conference, status='confirmed').count()
    if bookings_count >= conference.capacity:
        messages.error(request, 'This conference is at full capacity.')
        return redirect('conference_detail', slug=slug)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.conference = conference
            booking.status = 'confirmed'
            try:
                booking.save()
                messages.success(request, 'Booking successful!')
                return redirect('my_bookings')
            except IntegrityError:
                messages.error(request, 'You have already booked this conference.')
                return redirect('conference_detail', slug=slug)
    else:
        form = BookingForm(initial={'conference': conference})
    
    return render(request, 'booking_app/booking_form.html', {
        'form': form,
        'conference': conference
    })

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-time')
    return render(request, 'booking_app/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')
    
    return render(request, 'booking_app/cancel_booking.html', {'booking': booking})

@login_required
def feedback_view(request, slug):
    conference = get_object_or_404(Conference, slug=slug)
    
    # Check if the user has booked this conference
    booking = get_object_or_404(Booking, user=request.user, conference=conference)
    
    # Check if the user has already given feedback
    try:
        feedback = Feedback.objects.get(user=request.user, conference=conference)
        messages.info(request, 'You have already provided feedback for this conference.')
        return redirect('my_bookings')
    except Feedback.DoesNotExist:
        # User hasn't given feedback yet
        pass
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.conference = conference
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('my_bookings')
    else:
        form = FeedbackForm()
    
    return render(request, 'booking_app/feedback_form.html', {
        'form': form,
        'conference': conference
    })