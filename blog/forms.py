from django import forms
from .models import Blog
from contentmgmt.models import MediaFile

class BlogForm(forms.ModelForm):
    featured_image = forms.ModelChoiceField(
        queryset=MediaFile.objects.all(),
        required=False,
        widget=forms.HiddenInput()  # CMS modal will populate this
    )

    class Meta:
        model = Blog
        fields = [
            'title', 'subtitle', 'slug', 'content', 'featured_image',
            'homepage', 'active', 'meta_title', 'meta_keywords', 'meta_description'
        ]
        widgets = {
            'homepage': forms.HiddenInput(),
            'slug': forms.TextInput(attrs={'id': 'id_slug'}),
            'content': forms.Textarea(attrs={'id': 'id_content'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['slug'].widget.attrs['data-blog-id'] = self.instance.pk