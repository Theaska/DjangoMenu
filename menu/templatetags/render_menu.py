from django.template import Library, loader
from menu.models import Menu


register = Library()

@register.simple_tag(takes_context=True)
def render_menu(context, menu_name, template_name='menu/menu.html'):
    try:
        menu = Menu.objects.filter(title__iexact=menu_name).prefetch_related('menu_items', 'menu_items__children').first()
    except Menu.DoesNotExist:
        return ''

    return loader.render_to_string(template_name=template_name, context={
        'menu_items': menu.menu_items.all() 
        }, request=context.get('request'))


