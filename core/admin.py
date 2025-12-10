# core/admin.py
from django.contrib import admin
from .models import Donation, Request

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title','donor','status','created_at')
    list_filter = ('status',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title','requester','status','created_at')
    list_filter = ('status',)
