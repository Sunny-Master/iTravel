from django.shortcuts import render, redirect
from .models import Destination
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

# Constant variables
s3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'sunny-master-travellist'

# Edit photo
def edit_image(request, destination_id):
  # image-file will be the "name" attribute on the <input type="file">
  image_file = request.FILES.get('image-file', None)
  destination = Destination.objects.get(id=destination_id)
  if image_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using image_file.name[image_file.name.rfind('.'):]
    key = uuid.uuid4().hex + image_file.name[image_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(image_file, BUCKET, key)
      #buuild the full url string
      url = f"{s3_BASE_URL}{BUCKET}/{key}"
      if destination.image_url.split('/')[2] == 's3.us-east-2.amazonaws.com':
        old_key = destination.image_url.split('/')[-1]
        s3.delete_object(Bucket=BUCKET, Key=old_key)
      destination.image_url = url
      destination.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect(f"/destinations/{destination_id}")

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
  fields = ['country', 'city', 'date', 'comment', 'rating']

class DestinationDelete(LoginRequiredMixin, DeleteView):
  model = Destination
  success_url = '/destinations/'