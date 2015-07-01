from django.template.response import TemplateResponse

from .forms import TargetForm


def demo_view(request):
    context = {'form': TargetForm()}
    return TemplateResponse(request, 'index.html', context)
