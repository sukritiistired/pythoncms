from django.urls import path
from . import views

urlpatterns = [
    # Blog CRUD
    path('', views.blog_list, name='blog_list'),
    path('create/', views.create_blog, name='create_blog'),
    path('edit/<int:id>/', views.edit_blog, name='blog_edit'),
    path('delete/<int:id>/', views.blog_delete, name='blog_delete'),

    # Extra actions
    path('toggle-status/<int:id>/', views.blog_toggle_status, name='blog_toggle_status'),
    path('bulk-action/', views.blog_bulk_action, name='blog_bulk_action'),
    path('sort/<str:module>/', views.sort, name='sort'),  
    path('check-slug/', views.check_slug, name='check_slug'),

    # CMS modal for selecting images
    # Optional folder_id as URL parameter for navigable folders
    path('cms-media-list/', views.cms_media_list, name='cms_media_list'),
    path('cms-media-list/<int:folder_id>/', views.cms_media_list, name='cms_media_list_with_id'),
]