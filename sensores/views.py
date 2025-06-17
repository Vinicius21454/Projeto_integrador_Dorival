from rest_framework import viewsets, permissions, generics, pagination, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
import pandas as pd
from sqlalchemy import create_engine

from .models import Ambiente, Sensor, Historico
from .serializers import AmbienteSerializer, SensorSerializer, HistoricoSerializer

# Configuração de paginação
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AmbienteViewSet(viewsets.ModelViewSet):
    # Define o conjunto de dados padrão (todos os ambientes)
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['sig']
    pagination_class = CustomPagination

    def get_queryset(self):
       queryset = super().get_queryset()
       sig = self.request.query_params.get('sig')

       if sig:
           queryset = queryset.filter(sig__icontains= sig)    
       return queryset  
    
    # GET /ambientes/
    def list(self, request, *args, **kwargs):
        try:
            ambientes = self.get_queryset()
            serializer = self.get_serializer(ambientes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET /ambientes/{id}/
    def retrieve(self, request, *args, **kwargs):
        try:
            ambiente = self.get_object()
            serializer = self.get_serializer(ambiente)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # POST /ambientes/
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():  # Validação dos dados
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT /ambientes/{id}/
    def update(self, request, *args, **kwargs):
        try:
            ambiente = self.get_object()
            serializer = self.get_serializer(ambiente, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH /ambientes/{id}/
    def partial_update(self, request, *args, **kwargs):
        try:
            ambiente = self.get_object()
            serializer = self.get_serializer(ambiente, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE /ambientes/{id}/
    def destroy(self, request, *args, **kwargs):
        try:
            ambiente = self.get_object()
            self.perform_destroy(ambiente)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'status', 'sensor']
    pagination_class = CustomPagination

    def get_queryset(self):
        sensor = self.request.query_params.get('sensor')
        queryset = super().get_queryset()
        if sensor:
            queryset = queryset.filter(sensor__icontains=sensor) 
        return queryset
        

     # GET /sensores/
    def list(self, request, *args, **kwargs):
        try:
            sensores = self.get_queryset()
            serializer = self.get_serializer(sensores, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET /sensores/{id}/
    def retrieve(self, request, *args, **kwargs):
        try:
            sensor = self.get_object()
            serializer = self.get_serializer(sensor)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # POST /sensores/
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT /sensores/{id}/
    def update(self, request, *args, **kwargs):
        try:
            sensor = self.get_object()
            serializer = self.get_serializer(sensor, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH /sensores/{id}/
    def partial_update(self, request, *args, **kwargs):
        try:
            sensor = self.get_object()
            serializer = self.get_serializer(sensor, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE /sensores/{id}/
    def destroy(self, request, *args, **kwargs):
        try:
            sensor = self.get_object()
            self.perform_destroy(sensor)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sensor', 'ambiente', 'timestamp']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Historico.objects.all()  # Primeiro definimos o queryset
        timestamp = self.request.query_params.get('timestamp')
    
        if timestamp:
            queryset = queryset.filter(timestamp__icontains=timestamp)

        return queryset

    
    # GET /historico/
    def list(self, request, *args, **kwargs):
        try:
            registros = self.get_queryset()
            serializer = self.get_serializer(registros, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET /historico/{id}/
    def retrieve(self, request, *args, **kwargs):
        try:
            registro = self.get_object()
            serializer = self.get_serializer(registro)
            return Response(serializer.data)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # POST /historico/
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT /historico/{id}/
    def update(self, request, *args, **kwargs):
        try:
            registro = self.get_object()
            serializer = self.get_serializer(registro, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH /historico/{id}/
    def partial_update(self, request, *args, **kwargs):
        try:
            registro = self.get_object()
            serializer = self.get_serializer(registro, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE /historico/{id}/
    def destroy(self, request, *args, **kwargs):
        try:
            registro = self.get_object()
            self.perform_destroy(registro)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





