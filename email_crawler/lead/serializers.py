from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Lead.objects.all(),
                fields=('email', 'property_code')
            )
        ]
