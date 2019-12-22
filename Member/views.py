from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Member, Ministry, Shepherd
from users.models import UserProfile
from .forms import MemberForm, MinistryForm, ShepherdForm


@login_required
def table_members(request):
    template = "members/table.html"
    members = Member.objects.active()
    profile = UserProfile.objects.get(user=request.user)
    context = {"members": members, "members_active_list": "active", "profile": profile}
    return render(request, template, context)


@login_required
def thumbnail_members(request):
    template = "members/thumbnail.html"
    members = Member.objects.active()
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"members": members, "members_active_list": "active", "ministries": ministries, "shepherds": shepherds, "profile": profile}
    return render(request, template, context)


@login_required
def list_members(request):
    template = "members/list.html"
    members = Member.objects.active()
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {
        "profile": profile,
        "members": members, "shepherds": shepherds, "ministries": ministries, "total": len(members),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        "total_delete": len(members),
        "status": "all"
    }
    return render(request, template, context)


@login_required
def list_deleted_members(request):
    template = "members/list.html"
    members = Member.objects.deleted()
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {
        "profile": profile,
        "members": members, "shepherds": shepherds, "ministries": ministries, "total": len(members),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        "total_delete": len(members),
        "status": "all",
        "active": "active"
    }
    return render(request, template, context)


@login_required
def detail_member(request, pk):
    template = "members/detail.html"
    member = get_object_or_404(Member, pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    context = {"member": member, "profile": profile}
    return render(request, template, context)


@login_required
def edit_member(request, pk):
    template = "members/edit.html"
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm()
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"member": member, "form": form, "shepherds": shepherds, "ministries": ministries, "profile": profile}
    return render(request, template, context)


@login_required
def update_member(request, pk):
    if request.method == "POST":
        member = get_object_or_404(Member, pk=pk)
        form = MemberForm(request.POST, request.FILES, instance=member)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.success(request, "Member Information Updated Successfully")
            return redirect("detail_member", pk=pk)
        else:
            messages.error(request, "Member Information Not Updated")
            return redirect("edit_member", pk=pk)


@login_required
def delete_member(request, pk):
    # TODO: Make this functionality available only to admins
    member = get_object_or_404(Member, pk=pk)
    member.active = False
    member.save()
    messages.success(request, "Member Deleted Successfully")
    return redirect("list_members")


@login_required
def restore_member(request, pk):
    # TODO: Make this functionality available only to admins
    member = get_object_or_404(Member, pk=pk)
    member.active = True
    member.save()
    messages.success(request, "Member Restored Successfully")
    return redirect("list_members")


@login_required
def search_members(request):
    template = "members/list.html"
    q = request.GET.get('q')
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"ministries": ministries, "shepherds": shepherds, "profile": profile}
    if q != '':
        qs = Member.objects.active().filter(
            Q(name__icontains=q) | Q(shepherd__name__icontains=q) | Q(ministry__name__icontains=q)|
            Q(location__icontains=q) | Q(fathers_name__contains=q) | Q(mothers_name__contains=q)
        )
        context["members"] = qs
        context['total'] = len(qs)
        return render(request, template, context)
    else:
        members = Member.objects.active()
        context['members'] = members
        context['total'] = len(members)
        return render(request, template, context)


@login_required
def get_members_by_statuses(request, status):
    template = "members/list.html"
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    members = None
    if status == "tithe":
        members = Member.objects.pays_tithe()
    elif status == "new_believers":
        members = Member.objects.new_believer_school()
    elif status == "working":
        members = Member.objects.working()
    elif status == "schooling":
        members = Member.objects.schooling()

    context = {
        "profile": profile,
        "members": members,
        "shepherds": shepherds,
        "ministries": ministries,
        "total": len(Member.objects.active()),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        "total_delete": len(Member.objects.deleted()),
        status: status,
    }
    return render(request, template, context)


@login_required
def get_members_by_shepherds(request, shepherd):
    template = "members/list.html"
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    members = Member.objects.active().filter(shepherd__name__icontains=shepherd)
    profile = UserProfile.objects.get(user=request.user)
    context = {
        "profile": profile,
        "members": members,
        "shepherds": shepherds,
        "ministries": ministries,
        "total": len(Member.objects.active()),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        "total_delete": len(Member.objects.deleted()),
        "shepherd_name": shepherd
    }

    return render(request, template, context)


@login_required
def filter_members(request):
    template = "members/thumbnail.html"
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    initial_members = Member.objects.active()
    statuses = []
    for i in request.GET:
        if request.GET.get(i) == 'on':
            statuses.append(i)
    for i in statuses:
        if i == 'pays_tithe':
            initial_members = initial_members.filter(pays_tithe=True)
        elif i == 'working':
            initial_members = initial_members.filter(working=True)
        elif i == 'schooling':
            initial_members = initial_members.filter(schooling=True)
        elif i == "new_believer_school":
            initial_members = initial_members.filter(new_believer_school=True)
    # import pdb; pdb.set_trace()

    ministry = request.GET.get('ministry')
    profile = UserProfile.objects.get(user=request.user)

    context = {
        "profile": profile,
        "members": initial_members,
        "shepherds": shepherds,
        "ministries": ministries,
        "total": len(Member.objects.active()),
        "total_tithe": len(Member.objects.pays_tithe()),
        "total_new_believers": len(Member.objects.new_believer_school()),
        "total_schooling": len(Member.objects.schooling()),
        "total_working": len(Member.objects.working()),
        ministry: ministry
    }
    if ministry is not None:
        initial_members = initial_members.filter(ministry__name__icontains=ministry)
        context['members'] = initial_members
        context['id_ministry'] = ministry

    shepherd = request.GET.get('shepherd')
    if shepherd is not None:
        initial_members = initial_members.filter(shepherd__name__icontains=shepherd)
        # import pdb; pdb.set_trace()
        context['members'] = initial_members

    for i in statuses:
        context[i] = 'checked'

    return render(request, template, context)


@login_required
def add_member(request):
    # TODO: Make This functionality available only to admins
    template = "members/add.html"
    form = MemberForm()
    shepherds = Shepherd.objects.all()
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"form": form, "shepherds": shepherds, "ministries": ministries, "members_active_add": "active", "profile": profile}
    return render(request, template, context)


@login_required
def create_member(request):
    # TODO: Make this functionality available only to admins
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            member = form.save(commit=False)
            member.active = True
            member.save()
            messages.success(request, "Church Member Added Successfully")
            return redirect("list_members")
        else:
            messages.error(request, "Church Member Creation Failed")
            return redirect('add_member')


@login_required
def list_ministries(request):
    template = "ministries/list.html"
    ministries = Ministry.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"ministries": ministries, "ministries_active_list": "active", "profile": profile}
    return render(request, template, context)


@login_required
def add_ministries(request):
    # TODO: Make this functionality available only to admins
    template = "ministries/add.html"
    form = MinistryForm()
    profile = UserProfile.objects.get(user=request.user)
    context = {"form": form, "ministries_active_add": "active", "profile": profile}
    return render(request, template, context)


@login_required
def create_ministry(request):
    # TODO: Make this functionality available only to admins
    if request.method == "POST":
        form = MinistryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ministry Created Successfully")
            return redirect('list_ministries')
        else:
            messages.error(request, "Ministry Creation Failed")
            return redirect('add_ministry')


@login_required
def list_shepherds(request):
    template = "shepherds/list.html"
    shepherds = Shepherd.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {"shepherds": shepherds, "shepherds_active_list": "active", "profile": profile}
    return render(request, template, context)


@login_required
def add_shepherd(request):
    # TODO: Make this functionality available only to admins
    template = "shepherds/add.html"
    form = ShepherdForm()
    profile = UserProfile.objects.get(user=request.user)
    context = {"form": form, "shepherds_active_add": "active", "profile": profile}
    return render(request, template, context)


@login_required
def create_shepherd(request):
    # TODO: Make this functionality available only to admins
    if request.method == "POST":
        form = ShepherdForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Shepherd Created Successfully")
            return redirect('list_shepherds')
        else:
            messages.error(request, "Shepherd Creation Failed")
            return redirect('add_shepherd')


# ================================================================================= #
#                                   Api View Functions                              #
# ================================================================================= #
def api_get_members(request, user_id):
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
        except:
            user = None

        if user is not None:
            members = Member.objects.active()
            shepherds = Shepherd.objects.all()
            ministry = Ministry.objects.all()

            data = {
                "STATUS": "OK",
                "members": members,
                "shepherds": shepherds,
                "ministry": ministry
            }

        else:
            data = {"STATUS": "INVALID", "ERROR_TYPE": "AUTHENTICATION PROBLEM", "STATUS_CODE": -1}
    else:
        data = {"STATUS": "INVALID", "ERROR_TYPE": "USER NOT LOGGED IN", "STATUS_CODE": 0}

    return JsonResponse(data, content_type="Application/json", safe=False)


def api_create_member(request, user_id):
    data = {}
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
        except:
            user = None
        if user is not None:
            if request.method == "POST":
                form = MemberForm(request.POST, request.FILES or None)
                if form.is_valid():
                    member = form.save(commit=False)
                    member.save()
                    data = {"STATUS": "OK", "MEMBER_ID": member.pk}
                    return JsonResponse(data, content_type="Application/json", safe=False)
                else:
                    data = {"STATUS": "INVALID"}
        else:
            data = {"STATUS": "INVALID", "ERROR_TYPE": "AUTHENTICATION PROBLEM", "STATUS_CODE": -1}
    else:
        data = {"STATUS": "INVALID", "ERROR_TYPE": "USER NOT LOGGED IN", "STATUS_CODE": 0}

    return JsonResponse(data, content_type="Application/json", safe=False)


def api_get_shepherds(request):
    shepherds = Shepherd.objects.all()
    data = {"shepherds": shepherds}
    return JsonResponse(data, content_type="Application/json", safe=False)


def api_create_shepherd(request):
    if request.method == "POST":
        form = ShepherdForm(request.POST, request.FILES or None)
        if form.is_valid():
            shepherd = form.save(commit=False)
            shepherd.save()
            data = {"STATUS": "OK", "SHEPHERD_ID": shepherd.pk}
            return JsonResponse(data, content_type="Application/json", safe=False)
        else:
            data = {"STATUS": "INVALID"}
            return JsonResponse(data, content_type="Application/json", safe=False)


def api_edit_shepherd(request, pk):
    if request.method == "POST":
        shepherd = get_object_or_404(Shepherd, pk=pk)
        form = ShepherdForm(request.POST or None, instance=shepherd)
        if form.is_valid():
            form.save()
            data = {"STATUS": "OK", "CODE": 0}
        else:
            data = {"STATUS": "INVALID", "CODE": -1}
        return JsonResponse(data, content_type="Application/json", safe=False)


def api_delete_shepherd(request, pk):
    if request.method == "POST":
        shepherd = get_object_or_404(Shepherd, pk=pk)
        form = ShepherdForm(request.POST or None, instance=shepherd)
        if form.is_valid():
            form.delete()
            data = {"STATUS": "OK", "CODE": 0}
        else:
            data = {"STATUS": "INVALID", "CODE": -1}
        return JsonResponse(data, content_type="Application/json", safe=False)


def api_get_ministry(request):
    ministries = Ministry.objects.all()
    data = {"ministries": ministries}
    return JsonResponse(data, content_type="Application/json", safe=False)


def api_edit_ministry(request, pk):
    if request.method == "POST":
        ministry = get_object_or_404(Ministry, pk=pk)
        form = MinistryForm(request.POST or None, instance=ministry)
        if form.is_valid():
            form.save()
            data = {"STATUS": "OK", "CODE": 0}
        else:
            data = {"STATUS": "INVALID"}
        return JsonResponse(data, content_type="Application/json", safe=Fale)


# def api_delete_ministry(request, pk):



def api_create_ministry(request):
    if request.method == "POST":
        form = MinistryForm(request.POST, request.FILES or None)
        if form.is_valid():
            ministry = form.save(commit=False)
            ministry.save()
            data = {"STATUS": "OK", "MINISTRY_ID": ministry.pk}
            return JsonResponse(data, content_type="Application/json", safe=False)
        else:
            data = {"STATUS": "INVALID"}
            return JsonResponse(data, content_type="Application/json", safe=False)


# def api_get_members_status(request, status)