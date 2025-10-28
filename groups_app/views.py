
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudyGroup, GroupMember, GroupMessage

@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        group = StudyGroup.objects.create(name=name, creator=request.user)
        GroupMember.objects.create(user=request.user, group=group)
        return redirect("groups_app:group_detail", group_id=group.id)
    return render(request, "groups_app/create_group.html")

@login_required
def join_group(request):
    error = None
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            group = StudyGroup.objects.get(code=code)
            GroupMember.objects.get_or_create(user=request.user, group=group)
            return redirect("groups_app:group_detail", group_id=group.id)
        except StudyGroup.DoesNotExist:
            error = "کد نامعتبر است"
    return render(request, "groups_app/join_group.html", {"error": error})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if not GroupMember.objects.filter(user=request.user, group=group).exists():
        return redirect("groups_app:join_group")

    if request.method == "POST":
        content = request.POST.get("content")
        file = request.FILES.get("file")
        if content or file:
            GroupMessage.objects.create(user=request.user, group=group, content=content, file=file)

    messages = group.messages.all().order_by("created_at")
    return render(request, "groups_app/group_detail.html", {"group": group, "messages": messages})
