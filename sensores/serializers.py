from rest_framework import serializers # type: ignore
from .models import Ambiente, Sensor, Historico

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'

