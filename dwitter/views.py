
from django.views.generic import TemplateView
from dwitter.main.dwits_socketio import DwitsNamespace

class HomePage(TemplateView):
    template_name = 'index.html'

