# booking_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.BigIntegerField(null=True, blank=True)
    role = models.CharField(max_length=45, default='attendee')  # 'attendee', 'admin', 'organizer'

class Speaker(models.Model):
    speaker_id = models.CharField(max_length=45, primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    expertise = models.CharField(max_length=45)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SpeakerPhone(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name='phones')
    phone = models.BigIntegerField()
    
    def __str__(self):
        return f"{self.speaker} - {self.phone}"

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    time_start = models.TimeField()
    time_end = models.TimeField() 
    capacity = models.IntegerField()
    speakers = models.ManyToManyField(Speaker, through='ConferenceHasSpeaker')
    
    def __str__(self):
        return self.topic

class ConferenceCategory(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=45)
    
    def __str__(self):
        return f"{self.conference.topic} - {self.category}"

class ConferenceHasSpeaker(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('conference', 'speaker')
    
    def __str__(self):
        return f"{self.conference.topic} - {self.speaker}"

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='bookings')
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=45, default='pending')  # 'pending', 'confirmed', 'cancelled'
    
    class Meta:
        unique_together = ('user', 'conference')
    
    def __str__(self):
        return f"{self.user.username} - {self.conference.topic}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.CharField(max_length=45)
    rating = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'conference')
    
    def __str__(self):
        return f"{self.user.username} - {self.conference.topic} - {self.rating}"