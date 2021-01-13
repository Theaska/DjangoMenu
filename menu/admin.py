from django.contrib import admin
from django import forms
from .models import Menu, MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = MenuItem.objects.exclude(pk=self.instance.pk)


class MenuItemsInline(admin.StackedInline):
    model = MenuItem
    min_num = 1
    extra = 0
    form = MenuItemForm


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemsInline, )


