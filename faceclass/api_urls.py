from django.urls import path
from faceclass.api.views import get_csrf_token

urlpatterns = [
    path('csrf/cookie/', get_csrf_token, name='get-csrf-token'),
]