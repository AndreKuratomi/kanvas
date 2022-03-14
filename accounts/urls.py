from django.urls import path
from .views import PersonalizedUserView

urlpatterns = [
    path('accounts/', PersonalizedUserView.as_view())
]
