from django.views.generic import TemplateView

class HelloWorldView(TemplateView):
    template_name = "pages/hello_world.html"
