from functools import partial

from django.contrib import admin
from django.urls import resolve, exceptions
from django.shortcuts import resolve_url
from django import forms
from .models import Menu, MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)
            

class MenuItemsInline(admin.StackedInline):
    model = MenuItem
    min_num = 1
    extra = 0
    form = MenuItemForm

    def wrap_callback(self, request, obj=None, **kwargs):
        """ Для того, чтобы в поле parent показывались только элементы меню, у которых меню = текущему объекту меню """
        obj = obj
        request = request
        def callback(field, **kwargs):
            nf = field.formfield(**kwargs)
            if field.name == 'parent':
                nf.queryset = MenuItem.objects.filter(menu=obj)
            return nf
        return callback

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update({
            'formfield_callback': self.wrap_callback(request=request, obj=obj)
        })
        return super().get_formset(request, obj, **kwargs)



@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemsInline, )
    list_display = ('__str__', )



