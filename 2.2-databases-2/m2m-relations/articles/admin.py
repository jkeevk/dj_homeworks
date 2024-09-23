from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):

        counter = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                counter += 1
            if counter > 1:
                raise ValidationError('Основным может быть только один раздел')
            if counter == 0:
                raise ValidationError('Укажите основной раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [ScopeInline]