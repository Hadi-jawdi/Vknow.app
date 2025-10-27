from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import DiscussionPost, DiscussionReply
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def discussion_list(request):
    posts = DiscussionPost.objects.all().order_by('-created_at')
    return render(request, "discussion_app/pages/discussion_list.html", {"posts": posts})

@login_required
def discussion_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        DiscussionPost.objects.create(user=request.user, title=title, content=content)
        return redirect("discussion_app:list")
    return render(request, "discussion_app/pages/discussion_post.html")

@login_required
def discussion_reply(request, post_id, parent_id=None):
    post = get_object_or_404(DiscussionPost, id=post_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(DiscussionReply, id=parent_id)
    if request.method == "POST":
        content = request.POST.get("content")
        DiscussionReply.objects.create(user=request.user, post=post, content=content, parent=parent)
        return redirect("discussion_app:list")
    return render(request, "discussion_app/pages/discussion_reply.html", {"post": post, "parent": parent})
