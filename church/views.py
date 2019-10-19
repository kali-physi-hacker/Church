from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import UserProfile


@login_required
def index(request):
    template = "index.html"
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = None
    context = {"home_active": "active", "profile": profile}
    return render(request, template, context)


"""@login_required
def search(request):
    template = "index.html"
    """