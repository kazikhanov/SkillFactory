from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class ArticleForm(NewsForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = News.ARTICLE
        if commit:
            instance.save()
        return instance