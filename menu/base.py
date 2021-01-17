from menu.models import Menu


class MenuItemBase:
    children = []
    def __init__(self, item, children=None):
        self.item = item
        if children:
            self.children.extend(children)
    
    def add_child(self, child):
        self.children.append(child)



class MenuBase:
    def __init__(self, menu):
        if not isinstance(menu, Menu):
            raise ValueError(f'Menu have to be {type(Menu)}')
        self.menu_obj = menu