# booking_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from .models import User, Conference, Booking, Feedback, Speaker, Payment
from .forms import UserRegistrationForm, BookingForm, FeedbackForm, ConferenceSearchForm, PaymentForm
import uuid
from django.template.loader import render_to_string
from django.conf import settings
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from decimal import Decimal

def set_default_prices():
    """Set default prices for conferences that don't have a price set."""
    conferences = Conference.objects.filter(price=0)
    for conference in conferences:
        # Set a default price based on the conference topic length (just for demo purposes)
        default_price = Decimal('50.00') + (len(conference.topic) * Decimal('5.00'))
        conference.price = default_price
        conference.save()
        print(f"Set price for {conference.topic} to ${default_price}")

def home_view(request):
    # Set default prices for conferences that don't have a price set
    set_default_prices()
    
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
        booking_form = BookingForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if booking_form.is_valid() and payment_form.is_valid():
            # Create the booking
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.conference = conference
            booking.status = 'pending'  # Set to pending until payment is confirmed
            booking.payment_status = 'pending'
            
            try:
                booking.save()
                
                # Create the payment
                payment = Payment.objects.create(
                    booking=booking,
                    amount=conference.price,
                    payment_method=payment_form.cleaned_data['payment_method'],
                    transaction_id=str(uuid.uuid4()),  # Generate a unique transaction ID
                    status='pending'
                )
                
                # In a real application, you would integrate with a payment gateway here
                # For demo purposes, we'll simulate a successful payment
                
                # Simulate payment processing
                payment.status = 'completed'
                payment.save()
                
                # Update booking status
                booking.status = 'confirmed'
                booking.payment_status = 'completed'
                booking.save()
                
                messages.success(request, 'Booking and payment successful!')
                return redirect('receipt', booking_id=booking.booking_id)
                
            except IntegrityError:
                messages.error(request, 'You have already booked this conference.')
                return redirect('conference_detail', slug=slug)
    else:
        booking_form = BookingForm(initial={'conference': conference})
        payment_form = PaymentForm()
    
    return render(request, 'booking_app/booking_form.html', {
        'form': booking_form,
        'payment_form': payment_form,
        'conference': conference
    })

@login_required
def receipt_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    
    return render(request, 'booking_app/receipt.html', {
        'booking': booking,
        'payment': payment
    })

@login_required
def download_receipt_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10
    )
    
    normal_style = styles['Normal']
    
    # Add content
    elements.append(Paragraph("Payment Receipt", title_style))
    elements.append(Spacer(1, 12))
    
    # Conference Details
    elements.append(Paragraph("Conference Details", heading_style))
    conference_data = [
        ["Conference:", booking.conference.topic],
        ["Date:", booking.conference.date.strftime("%B %d, %Y") if booking.conference.date else "Not specified"],
        ["Time:", f"{booking.conference.time_start.strftime('%I:%M %p')} - {booking.conference.time_end.strftime('%I:%M %p')}"],
    ]
    
    conference_table = Table(conference_data, colWidths=[1.5*inch, 4*inch])
    conference_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(conference_table)
    elements.append(Spacer(1, 12))
    
    # Payment Information
    elements.append(Paragraph("Payment Information", heading_style))
    payment_data = [
        ["Receipt #:", payment.transaction_id],
        ["Date:", payment.payment_date.strftime("%B %d, %Y %H:%M")],
        ["Method:", payment.payment_method.title()],
        ["Status:", "Paid"],
    ]
    
    payment_table = Table(payment_data, colWidths=[1.5*inch, 4*inch])
    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 12))
    
    # Attendee Information
    elements.append(Paragraph("Attendee Information", heading_style))
    attendee_data = [
        ["Name:", f"{booking.user.first_name} {booking.user.last_name}"],
        ["Email:", booking.user.email],
    ]
    
    if booking.user.phone:
        attendee_data.append(["Phone:", str(booking.user.phone)])
    
    attendee_table = Table(attendee_data, colWidths=[1.5*inch, 4*inch])
    attendee_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(attendee_table)
    elements.append(Spacer(1, 12))
    
    # Amount Details
    elements.append(Paragraph("Amount Details", heading_style))
    amount_data = [
        ["Description", "Amount"],
        [f"Conference Registration - {booking.conference.topic}", f"${payment.amount}"],
        ["Total", f"${payment.amount}"],
    ]
    
    amount_table = Table(amount_data, colWidths=[4*inch, 1.5*inch])
    amount_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(amount_table)
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create the HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.booking_id}.pdf"'
    
    return response

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