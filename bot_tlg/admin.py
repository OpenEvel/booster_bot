from django.contrib import admin

from .forms import ProfileForm
from .models import Profile
from .models import Message
from .models import TlgBot

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=('id', 'profile', 'text', 'created_at')

@admin.register(TlgBot)
class BotTokenAdmin(admin.ModelAdmin):
    list_display=('username', 'state', 'external_id', 'token')