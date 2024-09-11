from django.urls import path
from blog.views import home, posts, CreateTicket, DeleteTicket


urlpatterns = [
    path('flux/', home, name='home'),
    path('vos-posts/', posts, name='posts'),
    path('create-ticket/', CreateTicket.as_view(), name='create_ticket'),
    path('delete-ticket/<int:pk>/', DeleteTicket.as_view(), name='delete_ticket')
]
