from django.contrib import admin
from .models import Ambiente, Sensor, Historico
# Register your models here.

@admin.register(Ambiente)
class AmbienteAdmin(admin.ModelAdmin):
    list_display = ['sig', 'descricao', 'responsavel']
    search_fields = ['sig', 'descricao']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'mac_address', 'status', 'unidade_med']
    list_filter = ['status', 'unidade_med']
    search_fields = ['sensor', 'mac_address']

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'ambiente', 'valor', 'timestamp']
    list_filter = ['sensor', 'ambiente', 'timestamp']
    search_fields = ['sensor__sensor', 'ambiente__sig']