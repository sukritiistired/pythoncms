from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import BlogForm
from django.db.models import F
from django.contrib import messages
from django.urls import reverse
from contentmgmt.models import MediaFile, Folder

# --------------------------
# Blog Views (existing)
# --------------------------
def check_slug(request):
    slug = request.GET.get("slug")
    blog_id = request.GET.get("id")
    qs = Blog.objects.filter(slug=slug)
    if blog_id:
        qs = qs.exclude(id=blog_id)
    return JsonResponse({"exists": qs.exists()})

def blog_list(request):
    homepage_param = request.GET.get('homepage')
    if homepage_param is not None:
        request.session['homepage_filter'] = homepage_param
        return redirect('blog_list')

    current_filter = request.session.get('homepage_filter', '0')
    blog = Blog.objects.filter(homepage=current_filter).order_by('position')

    return render(request, 'blog/list.html', {
        'list': blog,
        'current_filter': current_filter
    })

def create_blog(request):
    session_filter = request.session.get('homepage_filter', '0')
    homepage = session_filter == '1'
    homepage_param = '1' if homepage else '0'

    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.homepage = homepage
            blog.save()
            action = request.POST.get("action")

            if action == "save":
                messages.success(request, "Blog saved! You can add a new one.")
                return redirect(f"{reverse('create_blog')}?homepage={homepage_param}")
            elif action == "save_more":
                messages.success(request, "Blog saved! You can continue editing.")
                return redirect('blog_edit', id=blog.id)
            elif action == "save_quit":
                messages.success(request, "Blog saved!")
                return redirect(f"{reverse('blog_list')}?homepage={homepage_param}")
    else:
        form = BlogForm()

    return render(request, 'blog/form.html', {
        'form': form,
        'homepage': homepage,
    })
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    session_filter = request.session.get('homepage_filter', '0')
    homepage = session_filter == '1'
    homepage_param = '1' if homepage else '0'

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.homepage = homepage
            blog.save()
            action = request.POST.get("action")

            if action == "save_more":
                messages.success(request, "Changes saved.")
                return redirect('blog_edit', id=blog.id)
            elif action == "save_quit":
                messages.success(request, "Changes saved.")
                return redirect(f"{reverse('blog_list')}?homepage={homepage_param}")
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blog/form.html', {
        'form': form,
        'homepage': homepage,
        'blog': blog,
    })
def sort(request, module):
    data = json.loads(request.body)
    order = data.get('order', [])

    for index, item_id in enumerate(order):
        Blog.objects.filter(id=item_id).update(position=index)

    return JsonResponse({'status': 'ok'})


def blog_delete(request, id):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        blog = get_object_or_404(Blog, id=id)

        # Soft delete
        if hasattr(blog, "is_deleted"):
            blog.is_deleted = True
            blog.save()
        else:
            blog.delete()

        return JsonResponse({
            "success": True,
            "message": "Blog deleted successfully."
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request."
    }, status=400)


def blog_toggle_status(request, id):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=id)
        blog.active = not blog.active
        blog.save()

        return JsonResponse({
            "success": True,
            "active": blog.active,
        })

    return JsonResponse({"success": False}, status=400)


def blog_bulk_action(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        action = request.POST.get("action")
        selected_ids = request.POST.getlist("selected_blogs[]")

        if not selected_ids:
            return JsonResponse({
                "success": False,
                "message": "No blogs selected."
            }, status=400)

        blogs = Blog.objects.filter(id__in=selected_ids)

        if action == "publish":
            for blog in blogs:
                blog.active = not blog.active
                blog.save()

            return JsonResponse({
                "success": True,
                "message": "Status updated for selected blogs."
            })

        elif action == "delete":
            blogs.delete()

            return JsonResponse({
                "success": True,
                "message": "Selected blogs deleted successfully."
            })

        return JsonResponse({
            "success": False,
            "message": "Unsupported bulk action."
        }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Invalid request."
    }, status=400)
# --------------------------
# CMS Media Views for Featured Image Modal
# --------------------------
def cms_media_list(request, folder_id=None):
    folder = Folder.objects.filter(id=folder_id).first() if folder_id else None

    folders = Folder.objects.filter(parent=folder, is_active=True)
    files = MediaFile.objects.filter(folder=folder, is_active=True)

    # breadcrumb
    folder_path = []
    current = folder
    while current:
        folder_path.insert(0, current)
        current = current.parent

    return render(request, "contentmgmt/cms_media_list.html", {
        "folders": folders,
        "files": files,
        "folder_path": folder_path,
        "current_folder": folder
    })

@require_POST
def upload_media_file(request):
    folder_id = request.POST.get('folder')
    folder = Folder.objects.filter(id=folder_id).first() if folder_id else None

    if not request.FILES.getlist('file'):
        return JsonResponse({'success': False, 'errors': 'No files uploaded'})

    uploaded_files = []
    for f in request.FILES.getlist('file'):
        media = MediaFile.objects.create(
            file=f,
            folder=folder,
            name=f.name
        )
        uploaded_files.append({
            'id': media.id,
            'name': media.name,
            'url': media.file.url
        })

    return JsonResponse({'success': True, 'files': uploaded_files})


@require_POST
def create_folder(request):
    name = request.POST.get('name')
    parent_id = request.POST.get('parent')
    parent = Folder.objects.filter(id=parent_id).first() if parent_id else None

    if not name:
        return JsonResponse({'success': False, 'errors': 'Folder name required'})

    folder = Folder.objects.create(name=name, parent=parent)
    return JsonResponse({
        'success': True,
        'folder': {'id': folder.id, 'name': folder.name}
    })