from django.shortcuts import render, redirect
from .models import Destination
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Sign Up
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('destination-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST request OR a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

# home view
class Home(LoginView):
  template_name = 'home.html'

class DestinationList(LoginRequiredMixin, ListView):
  model = Destination

  def get_queryset(self):
    return Destination.objects.filter(user=self.request.user)

class DestinationDetail(LoginRequiredMixin, DetailView):
  model = Destination

class DestinationCreate(LoginRequiredMixin, CreateView):
  model = Destination
  fields = ['name', 'type', 'country', 'city', 'date', 'comment', 'rating', 'image_url']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class DestinationUpdate(LoginRequiredMixin, UpdateView):
  model = Destination
  fields = ['country', 'city', 'date', 'comment', 'rating', 'image_url']

class DestinationDelete(LoginRequiredMixin, DeleteView):
  model = Destination
  success_url = '/destinations/'