from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("post/", views.post, name="post"),
    path("user/<int:uid>/", views.user, name="user"),
    path("setuserdata/", views.setuserdata, name="setuserdata"),
    path('login/', LoginView.as_view(template_name='pages/login.html'), name='login'),
	path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
