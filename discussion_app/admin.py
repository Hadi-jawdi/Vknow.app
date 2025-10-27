from django.contrib import admin



from .models import DiscussionPost
from .models import DiscussionReply


admin.site.register(DiscussionPost)
admin.site.register(DiscussionReply)


