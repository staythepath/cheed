from django.urls import path
from . import views

urlpatterns = [
    path('actor/', views.actor, name='actor'),
    path('inbox/', views.inbox, name='inbox'),
    path('outbox/', views.outbox, name='outbox'),
    path('followers/', views.followers, name='followers'),
    path('following/', views.following, name='following'),
    path('.well-known/webfinger', views.webfinger, name='webfinger'),  # Include the webfinger route here
]
