from django.shortcuts import render
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'menu_name': 'test 1',
        })
        return context

