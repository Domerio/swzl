from django.contrib import admin
from .models import User, Category, LostAndFound, Attachment, Notification, Report, Bookmark

admin.site.register(User)
admin.site.register(Category)
admin.site.register(LostAndFound)
admin.site.register(Attachment)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Bookmark)