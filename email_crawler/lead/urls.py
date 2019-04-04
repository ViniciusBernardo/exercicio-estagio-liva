from rest_framework import routers
from .views import LeadViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register('lead-viewset', LeadViewSet)

urlpatterns = ROUTER.urls
