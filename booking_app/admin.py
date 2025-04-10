# booking_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Speaker, SpeakerPhone, Conference, ConferenceCategory
from .models import ConferenceHasSpeaker, Booking, Feedback

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'first_name', 'last_name', 'phone', 'role')}),
    )

class SpeakerPhoneInline(admin.TabularInline):
    model = SpeakerPhone
    extra = 1

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['speaker_id', 'first_name', 'last_name', 'expertise']
    search_fields = ['first_name', 'last_name', 'expertise']
    inlines = [SpeakerPhoneInline]

class ConferenceCategoryInline(admin.TabularInline):
    model = ConferenceCategory
    extra = 1

class ConferenceHasSpeakerInline(admin.TabularInline):
    model = ConferenceHasSpeaker
    extra = 1

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['conference_id', 'topic', 'date', 'time_start', 'time_end', 'capacity']
    search_fields = ['topic', 'description']
    list_filter = ['date', 'time_start']
    inlines = [ConferenceCategoryInline, ConferenceHasSpeakerInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'conference', 'time', 'status']
    list_filter = ['status', 'time']
    search_fields = ['user__username', 'conference__topic']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'conference', 'rating']
    list_filter = ['rating']
    search_fields = ['user__username', 'conference__topic', 'comments']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Feedback, FeedbackAdmin)