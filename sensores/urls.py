from rest_framework.routers import DefaultRouter
from .views import AmbienteViewSet, SensorViewSet, HistoricoViewSet

router = DefaultRouter()
router.register(r'ambientes', AmbienteViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'historicos', HistoricoViewSet)

urlpatterns = router.urls
