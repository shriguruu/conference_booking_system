# booking_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)  # Making it nullable temporarily
    time_start = models.TimeField()
    time_end = models.TimeField() 
    capacity = models.IntegerField()
    speakers = models.ManyToManyField(Speaker, through='ConferenceHasSpeaker')
    
    def __str__(self):
        return self.topic

@receiver(pre_save, sender=Conference)
def create_conference_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.topic)
        slug = base_slug
        counter = 1
        while Conference.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug

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