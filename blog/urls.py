from django.urls import path
from blog.views import (home, posts, follows, CreateTicket, DeleteTicket, UpdateTicket,
                        CreateReview, DeleteReview, UpdateReview, CreateReviewAndTicket, Follow,
                        DeleteUserFollows)


urlpatterns = [
    path('flux/', home, name='home'),
    path('vos-posts/', posts, name='posts'),
    path('abonnements/', Follow.as_view(), name='follow'),
    path('create-ticket/', CreateTicket.as_view(), name='create_ticket'),
    path('delete-ticket/<int:pk>/', DeleteTicket.as_view(), name='delete_ticket'),
    path('update-ticket/<int:pk>/', UpdateTicket.as_view(), name='update_ticket'),
    path('create-review/<int:pk>/', CreateReview.as_view(), name='create_review'),
    path('delete-review/<int:pk>/', DeleteReview.as_view(), name='delete_review'),
    path('update-review/<int:pk>/', UpdateReview.as_view(), name='update_review'),
    path('create-review/', CreateReviewAndTicket.as_view(), name='create_review_and_ticket'),
    path('unfollow/<int:pk>/', DeleteUserFollows.as_view(), name='delete_user_follows'),
]
