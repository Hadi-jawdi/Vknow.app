from django.shortcuts import render,get_object_or_404
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ShareResource,ResourceComment

@login_required
def share_resource(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        file = request.FILES.get("file")

        ShareResource.objects.create(
            user=request.user,
            title=title,
            description=description,
            link=link,
            file=file,
        )
        return redirect("resources_app:resources")

    return render(request, "resources_app/pages/share_resource.html")


def resource_list(request):
    resources = ShareResource.objects.all().order_by('-created_at')
    return render(request, "resources_app/pages/resources.html", {"resources": resources})


@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(ShareResource, pk=pk)
    comments = resource.comments.all().order_by('-created_at')

    if request.method == "POST":
        content = request.POST.get("content")
        if content.strip():
            ResourceComment.objects.create(resource=resource, user=request.user, content=content)
        return redirect("resources_app:resource_detail", pk=pk)

    context = {
        "resource": resource,
        "comments": comments,
    }
    return render(request, "resources_app/pages/resource_detail.html", context)