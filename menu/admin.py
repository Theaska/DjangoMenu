from django.contrib import admin
from django.urls import resolve
from django import forms
from .models import Menu, MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if getattr(self.instance, 'menu', None):
    #         self.fields['parent'].queryset = MenuItem.objects.filter(
    #             menu=self.instance.menu,
    #         ).exclude(pk=self.instance.pk)


class MenuItemsInline(admin.StackedInline):
    model = MenuItem
    min_num = 1
    extra = 0
    form = MenuItemForm

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        resolved = resolve(request.path_info)
        menu = None
        if resolved.kwargs.get('object_id'):
            menu = self.parent_model.objects.get(pk=resolved.kwargs.get('object_id'))
        print(super().get_queryset(request).filter(menu=menu))
        return super().get_queryset(request).filter(menu=menu)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemsInline, )
    list_display = ('__str__', )



