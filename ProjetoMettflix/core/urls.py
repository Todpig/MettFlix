from django.urls import path, include
from rest_framework import routers
from .views import *
from .viewsSet import *

# Crie um roteador para as visualizações do Django Rest Framework
router = routers.DefaultRouter()
router.register(r'filmes', FilmeViewSet)
router.register(r'series', SerieViewSet)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create-movie", CreateFilmeView.as_view(), name="create-movie"),
    path("like/<int:id>", put_like, name="like"),
    path("dislike/<int:id>", put_deslike, name="dislike"),
    path("download/<int:id>", put_download, name="download"),
    path("loginconta/", LoginView.as_view(), name="loginconta"),
    path("fazerlogin/", login_request, name="fazerlogin"),
    path("obra/<slug:slug>", ObraView.as_view(), name="obra"),
    path("cadastro/", RegisterView.as_view(), name="cadastro"),
    path("fazercasdastro/", register_request, name="fazercasdastro"),
    path('api/', include(router.urls)),
    # ...
]

# Adicione a URL padrão para redirecionamento após a criação bem-sucedida
router.register(r'filmes', FilmeViewSet, basename='filmes')
router.register(r'series', SerieViewSet, basename='series')

urlpatterns += router.urls
