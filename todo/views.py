# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from todo.models import Todo
from todo.forms import UserCreationForm, LoginForm, TodoForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    print"register"
    if request.user.is_authenticated():
        return HttpResponseRedirect("/todo/profile/")
    print request.user
    if request.method == 'POST':
        print 'inside Post'
        form = UserCreationForm(request.POST)
        print form.errors
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.set_password(str(form.cleaned_data['password']))
            new_user.save()
            
            return HttpResponseRedirect("/todo/profile/")
        else:
        	return render_to_response('register.html',locals(),context_instance=RequestContext(request))
    else:
    	form = UserCreationForm()
        print request.user
    	return render_to_response('register.html',locals(),context_instance=RequestContext(request))

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/todo/list/")
    if request.method == 'POST':
        print 'hi'
        form = LoginForm(request.POST)
        print form
        if form.is_valid():
            print form.errors
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/todo/list/")
            else:
                return HttpResponseRedirect("/todo/login/")
        else:

            return render_to_response('login.html',locals(),context_instance=RequestContext(request))
    else:
        form = LoginForm(request.POST)
        return render_to_response('login.html',locals(),context_instance=RequestContext(request))

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/todo/login/")

def todo_list(request):
	todos = Todo.objects.all()
	return render_to_response('todo.html',locals(),context_instance=RequestContext(request))

@login_required
def add_todo(request):
    if request.method == 'POST':
        print 'inside'
        form = TodoForm(request.POST)
        print form.errors
        if form.is_valid():
            print "insideform"
            todo = Todo(name=form.cleaned_data['name'],
						description = form.cleaned_data['description'],
						user = request.user,
						priority = form.cleaned_data['priority'],
                        state = form.cleaned_data['state'],
						task_date = form.cleaned_data['task_date']
						)
            todo.save()
            return HttpResponseRedirect("/todo/list/")
    else:
        form = TodoForm()
    return render_to_response('add_todo.html',locals(),context_instance=RequestContext(request))

@login_required
def view_edit(request,todo_id):
	todo = Todo.objects.get(id = todo_id)
	if request.method == 'POST':
		form = TodoForm(request.POST)
		if form.is_valid():
			todo.name = form.cleaned_data['name']
			todo.description = form.cleaned_data['description']
			todo.user = request.user
			todo.priority = form.cleaned_data['priority']
			todo.task_date = form.cleaned_data['task_date']
			todo.save()
			return HttpResponseRedirect("/todo/list/")
	else:
		form = TodoForm()
		form.fields['name'].initial = todo.name
		form.fields['description'] = todo.description
		form.fields['priority'] = todo.priority
		form.fields['task_date'] = todo.task_date
	return render_to_response('view_todo.html',locals(),context_instance=RequestContext(request))
