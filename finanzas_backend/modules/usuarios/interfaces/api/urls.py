from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from modules.usuarios.interfaces.api.views import LoginView, RegistroView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="usuarios-registro"),
    path("login/", LoginView.as_view(), name="usuarios-login"),
    # Cuando el access token expira (ver SIMPLE_JWT.ACCESS_TOKEN_LIFETIME),
    # el front manda el refresh acá y recibe un access nuevo sin pedir
    # contraseña de nuevo.
    path("token/refresh/", TokenRefreshView.as_view(), name="usuarios-token-refresh"),
]
