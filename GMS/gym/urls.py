from django.urls import include, path
from rest_framework import routers
from . import views
# роутим Api
router = routers.DefaultRouter()
router.register(r'plans', views.PlanViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]