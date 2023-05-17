from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView,LogicView,DashboardView,EventView,EditView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('logic', LogicView.as_view()),
    path('dashboard', DashboardView.as_view()),
    path('dashboard/<id>', EventView.as_view()),
    path('dashboard/<id>/edit', EditView.as_view()),
]

