from rest_framework import viewsets
from .serializers import LeadSerializer
from .models import Lead


class LeadViewSet(viewsets.ModelViewSet):

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
