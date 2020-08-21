from rest_framework import routers

from apps.delta.viewsets import PropostaViewSet

router = routers.DefaultRouter()
router.register(r'proposta', PropostaViewSet)
urlpatterns = router.urls