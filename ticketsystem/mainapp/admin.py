from django.contrib import admin

from mainapp.models import News, Tickets
from mainapp.models import UserProfile

admin.site.register(News)
admin.site.register(Tickets)
admin.site.register(UserProfile)

