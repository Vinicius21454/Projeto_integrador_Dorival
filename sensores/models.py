from django.db import models

class Ambiente(models.Model):
    descricao = models.CharField(max_length=100)
    sig = models.CharField(max_length=10, unique=True)
    ni = models.CharField(max_length=40)
    responsavel = models.CharField(max_length=50)
    def __str__(self):
        return self.sig
    
class Sensor(models.Model):
    sensor = models.CharField(max_length=40)  
    mac_address = models.CharField(max_length=50)  
    unidade_med = models.CharField(max_length=100) 
    latitude = models.FloatField()  
    longitude = models.FloatField() 
    status = models.BooleanField(default=True) 
    


class Historico(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    valor = models.FloatField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)