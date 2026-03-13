from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.db.models import F
from .forms import UserForm
from .decorators import permission_required

# ------------------- ROLES -------------------

@permission_required("auth.view_group")
def role_list(request):
    roles = Group.objects.all().order_by("name")
    return render(request, "core/roles/role_list.html", {"roles": roles})


@permission_required("auth.add_group")
def add_role(request):
    permissions = Permission.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        perm_ids = request.POST.getlist("permissions")

        role = Group.objects.create(name=name)
        role.permissions.set(perm_ids)

        messages.success(request, "Role created successfully!")
        return redirect("core:role_list")

    return render(request, "core/roles/role_form.html", {"permissions": permissions})


@permission_required("auth.change_group")
def edit_role(request, pk):
    role = get_object_or_404(Group, pk=pk)
    permissions = Permission.objects.all()

    if request.method == "POST":
        role.name = request.POST.get("name")
        perm_ids = request.POST.getlist("permissions")

        role.save()
        role.permissions.set(perm_ids)

        messages.success(request, "Role updated successfully!")
        return redirect("core:role_list")

    return render(request, "core/roles/role_form.html", {
        "role": role,
        "permissions": permissions
    })


@permission_required("auth.delete_group")
def delete_role(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role.delete()
    messages.success(request, "Role deleted successfully!")
    return redirect("core:role_list")

# ------------------- USERS -------------------

@permission_required("core.view_userprofile")
def user_list(request):
    users = User.objects.all().order_by("-id")
    return render(request, "core/user_list.html", {"users": users})


@permission_required("core.add_userprofile")
def add_user(request):
    groups = Group.objects.all()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()

            role_id = request.POST.get("role")
            if role_id:
                group = Group.objects.get(id=role_id)
                user.groups.add(group)

            messages.success(request, "User added successfully!")
            return redirect("core:user_list")
        else:
            messages.error(request, "Failed to add user.")
    else:
        form = UserForm()

    return render(request, "core/user_form.html", {"form": form, "groups": groups})


@permission_required("core.change_userprofile")
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    groups = Group.objects.all()

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            role_id = request.POST.get("role")
            if role_id:
                group = Group.objects.get(id=role_id)
                user.groups.clear()
                user.groups.add(group)

            messages.success(request, "User updated successfully!")
            return redirect("core:user_list")
        else:
            messages.error(request, "Failed to update user.")
    else:
        form = UserForm(instance=user)

    return render(request, "core/user_form.html", {
        "form": form,
        "groups": groups,
        "user": user
    })


@permission_required("core.delete_userprofile")
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("core:user_list")


@permission_required("core.change_userprofile")
def user_toggle_status(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, "Status changed successfully.")
    return redirect('core:user_list')


# ------------------- BULK ACTIONS -------------------

@permission_required("core.change_userprofile")
def user_bulk_action(request):
    if request.method == "POST":
        action = request.POST.get("action")
        selected_ids = request.POST.getlist("selected_user")
        users = User.objects.filter(id__in=selected_ids)

        if action == "publish":
            users.update(is_active=~F("is_active"))
            messages.success(request, "Status changed successfully.")
        elif action == "delete":
            for user in users:
                user.delete()
            messages.success(request, "Selected users deleted successfully.")

    return redirect('core:user_list')


# ------------------- LOGOUT -------------------

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'core:login'