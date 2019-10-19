from django.contrib import admin

from .models import Member, Ministry, Shepherd, TestDb

admin.site.register(Member)
admin.site.register(Ministry)
admin.site.register(Shepherd)
