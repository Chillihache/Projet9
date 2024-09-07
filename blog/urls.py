from django.urls import path
from blog.views import home, posts, CreateTicket, delete_ticket


urlpatterns = [
    path('flux/', home, name='home'),
    path('vos-posts/', posts, name='posts'),
    path('create-ticket/', CreateTicket.as_view(), name='create_ticket'),
    path('delete-ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket')
]
