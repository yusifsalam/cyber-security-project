from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Q
from .models import File, Message


@login_required
def deleteView(request):
    f = File.objects.get(pk=request.POST.get('id'))
    if (f.owner == request.user):
        f.delete()
    return redirect('/')


@login_required
def downloadView(request, fileid):
    f = File.objects.get(pk=fileid)
    if (f.owner != request.user):
        return redirect('/')
    filename = f.data.name.split('/')[-1]
    response = HttpResponse(f.data, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def addView(request):
    data = request.FILES.get('file')
    f = File(owner=request.user, data=data)
    f.save()
    return redirect('/')


@login_required
def addMessage(request):
    target = User.objects.get(username=request.POST.get('to'))
    Message.objects.create(source=request.user, target=target,
                           content=request.POST.get('content'))
    return redirect('/')


@login_required
def homePageView(request):
    files = File.objects.filter(owner=request.user)
    uploads = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]
    messages = Message.objects.filter(
        Q(source=request.user) | Q(target=request.user))
    users = User.objects.exclude(pk=request.user.id)
    return render(request, 'pages/index.html', {'uploads': uploads, 'msgs': messages, 'users': users})


class RegisterView(View):
    def get(self, request):
        return render(request, 'pages/register.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'pages/register.html', {'form': form})
