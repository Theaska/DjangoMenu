from django.urls.exceptions import NoReverseMatch
from django.db.models import F
from django.shortcuts import resolve_url

from menu.models import MenuItem
from menu.exceptions import MenuException


class MenuItemBase:

    def __init__(self, item, children=None):
        self.item = item
        self._children = []
        if children:
            self._check_children(children)
            self._children.extend(children) 

    def _check_children(self, children):
        if not all(isinstance(child, self.__class__) for child in children):
            raise MenuException(f'children items have to be {self._class}')
    
    @property
    def title(self):
        return self.item['name']
    
    def add_child(self, child):
        self._children.append(child)

    def add_recursive(self, menu_items):
        print('add_recursive', menu_items)
        _child = list((MenuItemBase(item) for item in menu_items if item['parent']==self.item['pk']))
        for child in _child:
            print(child)
            child.add_recursive(menu_items)
        self._children.extend(_child)

    @property
    def children(self):
        return self._children

    @property
    def url(self):
        try:
            return resolve_url(self.item.get('raw_url'))
        except NoReverseMatch:
            return self.item.get('raw_url')

    def __repr__(self):
        return f'{self.item["name"]} / {self.url}'


class MenuBase:
    menu_items_model = MenuItem
    menu_name_query = 'menu__title__iexact'
    values = ('name', 'parent', 'pk', 'raw_url')

    def __init__(self, menu_name):
        self._roots = []
        self.menu_name = menu_name
        self.menu_items = self._get_menu_items()

    def _get_menu_items(self):
        return list(self.menu_items_model.objects.filter(**{
                self.menu_name_query: self.menu_name
            }).values(
                *self.values,
            ))

    def make_menu(self):
        print(self.roots)
        for root in self.roots:
            print(root)
            root.add_recursive(self.menu_items)
        # return self

    @property
    def roots(self):
        if not self._roots:
            self._roots = list(MenuItemBase(item) for item in self.menu_items if item['parent'] is None)
        return self._roots

    def __iter__(self):
        print(self.roots)
        print(self._roots)
        return iter(self.roots)
    

