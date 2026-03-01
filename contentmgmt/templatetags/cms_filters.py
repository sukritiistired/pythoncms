from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    if not file_url:
        return False
    return file_url.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))