from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
# This mixin should be at the leftmost position in the inheritance list.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
# Create your views here.

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self) -> str:
        return reverse_lazy('tasks')
    

# To create register
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# To see the list of tasks user have
class TaskList(LoginRequiredMixin, ListView):
    # The Below two statements can be used to redirect all requests by non-authenticated users to login.
    # login_url = "login"
    # redirect_field_name = "redirect_to"

    # OR

    # In this Particular Application I have USED LOGIN_URL="login" in the settings.py to achieve similar functionality.

    # By default the ListView Looks for a template with the prefix of the model name (task) and the suffix of _list.html 
    model=Task
    # Override the default queryset name of “object_list” by setting the “context_object_name” attribute. 
    context_object_name='tasks'
    # By default the ListView Looks for a template with the prefix of the model name (task) and the suffix of _list.html if not otherwise set (task_list.html).
    # This can be overridden by setting the “template_name” attribute.
    # template_name = 'base/Tasks.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        # Backend for search field
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        context['search_input']=search_input
        return context


# To see the detailed view of the particular task
class TaskDetail(LoginRequiredMixin, DetailView):
    # By default the DetailView Looks for a template with the prefix of the model name (task) and the suffix of _detail.html  
    model=Task
    # Override the default model name of “object” by setting the “context_object_name” attribute.
    context_object_name='task'
    # By default the DetailView looks for a template with the prefix of the model name (task) and the suffix of _detail.html if not otherwise set (task_detail.html).
    template_name = 'base/Task.html'

# To create a new task
class TaskCreate(LoginRequiredMixin, CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self, form) :
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

# To update an existing task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

# To delete a task
class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

