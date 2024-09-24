from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name    
    
class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')
    temperature = models.FloatField(verbose_name='Температура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время измерения')
    image = models.ImageField(blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return str(self.temperature)