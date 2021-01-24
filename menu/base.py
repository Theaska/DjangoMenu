from __future__ import annotations
from typing import Optional, List

from django.urls.exceptions import NoReverseMatch
from django.db.models import F
from django.shortcuts import resolve_url

from menu.models import MenuItem
from menu.exceptions import MenuException


class MenuItemBase:
    def __init__(
        self, 
        item: List[dict], 
        children: Optional[List[MenuItemBase]] = None, 
        parent: Optional[MenuItemBase] = None,
        classes: Optional[str]  = '',
        level: Optional[int] = 1,
    ):
        """
            item        - элемент меню представленный в виде списка элементов словаря
            children    - дочерние элементы меню
            parent      - родительский элемент меню
            classes     - классы, которые будут отображены в темплейте у этого элемента меню
        """
        self.item = item
        self._children = []
        self._parent = parent
        self._active = False
        self._classes = classes
        self.level = level
        if children:
            self._children.extend(children) 

    def activate(self):
        self.recursive_activate()

    def recursive_activate(self):
        """ Рекурсивно делает элемент меню и его родительские элементы активными """
        self._active = True
        if self.parent:
            self.parent.activate()

    @property
    def classes(self):
        """ Классы, для стилей   
        Show - если нужно показывать элемент меню (если элемент активен, если родительский элемент активен или элемент является главным).
        Hidden - скрыть элемент меню. """
        classes = self._classes
        print(self.parent)
        print(getattr(self.parent, 'is_active', False), self)
        if self.is_active or getattr(self.parent, 'is_active', False) or self.level == 1:
            classes += ' show'
        else:
            classes += ' hidden'
        return classes
    
    @property
    def is_active(self):
        """ Активен ли элемент """
        return self._active

    @property
    def title(self):
        """ Название элемента меню """
        return self.item['name']

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def id(self):
        return self.item['pk']

    @property
    def url(self):
        try:
            return resolve_url(self.item.get('raw_url'))
        except NoReverseMatch:
            return self.item.get('raw_url').strip()
    
    def add_child(self, child):
        self._children.append(child)

    def add_children(self, children):
        self._children.extend(children)

    def add_recursive(self, menu_items, current_path=None):
        """ Рекурсивно добавляет элементы меню. 
            current_path  - текущий url, чтобы знать, какие элементы меню активировать
        """
        for item in menu_items:
            if item.get('parent') == self.id:
                item_menu = MenuItemBase(item, parent=self, level=self.level+1)
                item_menu.add_recursive(menu_items, current_path)
                if current_path and current_path == item_menu.url:
                    item_menu.activate()
                self.add_child(item_menu)

    def __repr__(self):
        return f'name: {self.item["name"]}, path: {self.url}, active: {self.is_active}'


class MenuBase:
    """
        Класс меню. 
        menu_items_model    - модель БД, из которой будут браться элементы меню
        menu_name_query     - по какому полю будут фильтроваться меню
        values              - какие поля получить из БД
    """
    menu_items_model = MenuItem
    menu_name_query = 'menu__title__iexact'
    values = ('name', 'parent', 'pk', 'raw_url')

    def __init__(self, menu_name: str):
        """
            menu_name - название меню в БД
        """
        self._roots = []
        self.menu_name = menu_name
        self.menu_items = self._get_menu_items()

    def _get_menu_items(self):
        return list(self.menu_items_model.objects.filter(**{
                self.menu_name_query: self.menu_name
            }).values(
                *self.values,
            ))

    def make_menu(self, request=None):
        """ Запускает построение меню. 
            request - HttpRequest для получения текущего урла
        """
        for root in self.roots:
            current_path = getattr(request, 'path', '')
            if root.url == current_path:
                root.activate()
            root.add_recursive(self.menu_items, current_path=current_path)

    @property
    def roots(self):
        """ Главные элементы меню.
        """
        if not self._roots:
            self._roots = list(
                MenuItemBase(item) 
                for item in self.menu_items if item['parent'] is None
            )
        return self._roots

    def __iter__(self):
        return iter(self.roots)
    

