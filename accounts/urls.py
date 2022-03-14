from django.urls import path
from .views import PersonalizedUserView, LoginUserView

urlpatterns = [
    path('accounts/', PersonalizedUserView.as_view()),
    path('login/', LoginUserView.as_view())
]
