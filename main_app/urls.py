from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('destinations/', views.DestinationList.as_view(), name='destination-index'),
  path('destinations/<int:pk>/', views.DestinationDetail.as_view(), name='destination-detail'),
  path('destinations/create/', views.DestinationCreate.as_view(), name='destination-create'),
  path('destinations/<int:pk>/update/', views.DestinationUpdate.as_view(), name='destination-update'),
  path('destinations/<int:pk>/delete/', views.DestinationDelete.as_view(), name='destination-delete'),
  path('accounts/signup/', views.signup, name='signup'),
]