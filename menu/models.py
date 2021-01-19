from django.db import models
from django.urls import exceptions
from django.db.models import Max
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _


class Menu(models.Model):
    title = models.CharField(
        _('title of menu'), 
        max_length=128,
        unique=True
    )

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')


class MenuItem(models.Model):
    parent = models.ForeignKey(
        'self', 
        verbose_name=_('parent menu item'), 
        blank=True, 
        null=True, 
        related_name='children',
        on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu, 
        verbose_name=_('menu'), 
        related_name='menu_items', 
        on_delete=models.CASCADE
    )
    name = models.CharField(
        _('name of menu item'), 
        max_length=128
    )
    raw_url = models.CharField(
        _('url of menu item'), 
        help_text=_('can be url or named django app url'), 
        max_length=300
    )

    sort_order = models.PositiveIntegerField(_('order'), null=True, blank=True)

    class Meta:
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')
        ordering = ('sort_order', )
        
    @property
    def url(self):
        try:
            return resolve_url(self.raw_url)
        except exceptions.NoReverseMatch:
            return self.raw_url

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            max_sort_order = self._meta.model.objects.filter(menu=self.menu).aggregate(max_order=Max('sort_order'))['max_order']
            self.sort_order = max_sort_order + 1 if max_sort_order is not None else 0
        super().save(*args, **kwargs)