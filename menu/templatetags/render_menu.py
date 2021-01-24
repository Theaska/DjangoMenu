from django.template import Library, loader
from menu.models import MenuItem
from menu.base import MenuBase


register = Library()

@register.simple_tag(takes_context=True)
def render_menu(context, menu_name, template_name='menu/menu.html'):
    menu = MenuBase(menu_name)
    menu.make_menu(request=context.get('request'))
    return loader.render_to_string(template_name=template_name, context={
        'menu_items': menu, 
    }, request=context.get('request'))


