from django.contrib import admin
from django.urls import path, include
import authentication.views
import blog.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('flux/', include(("blog.urls", "blog"))),
    path('', include(("authentication.urls", "auth"))),
    path('logout/', authentication.views.logout_user, name='logout'),
]
