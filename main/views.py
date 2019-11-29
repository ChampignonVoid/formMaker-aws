from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from formMaker.settings import DEFAULT_PROTOCOL_DISPLAY
from main.models import Form


def form(request, uuid):
    form = Form.objects.filter(uuid=uuid).first()
    if form is None:
        raise Http404("No form were found.")
    return render(request, 'main/form.html', {
        'form': form
    })


def form_token(request):
    if request.method == 'POST':
        token = request.POST['token']
        try:
            form = Form.objects.filter(uuid=token).first()
        except ValidationError:
            return render(request, 'main/form_token.html', {
                'message': 'The token is not a valid token'
            })
        if form is None:
            return render(request, 'main/form_token.html', {
                'message': 'There\'s no form with this token.'
            })
        return redirect(to=reverse_lazy('form', kwargs={'uuid': token}), permanent=False)
    return render(request, 'main/form_token.html')


@login_required
def my_forms(request):
    return render(request, 'main/my_forms.html')


@login_required
def form_create(request):
    return render(request, 'main/form_create.html')


@login_required
def form_summary(request, uuid):
    user_form = get_object_or_404(Form, uuid=uuid)
    if user_form.creator != request.user:
        raise PermissionDenied
    return render(request, 'main/form_summary.html', {
        'form': user_form,
        'protocol': DEFAULT_PROTOCOL_DISPLAY
    })
