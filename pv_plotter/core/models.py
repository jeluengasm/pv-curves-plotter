from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import User


class PVData(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.SET_NULL,
        null=True
    )

    module_type = models.CharField(
        verbose_name='tipo de módulo',
        max_length=50
    )

    reference = models.CharField(
        verbose_name='referencia',
        max_length=50,
        blank=True
    )

    comments = models.TextField(
        verbose_name='referencia',
        max_length=50,
        blank=True
    )

    temperature = models.FloatField(
        verbose_name='temperatura',
        null=True
    )

    measure_date = models.DateTimeField(
        verbose_name='fecha de medición',
        auto_now_add=True
    )

    created_date = models.DateTimeField(
        verbose_name='fecha de creación',
        auto_now_add=True
    )

    updated_date = models.DateTimeField(
        verbose_name='fecha de modificación',
        auto_now=True
    )

    current_data = ArrayField(
        models.SmallIntegerField(),
        default=list,
    )

    voltage_data = ArrayField(
        models.SmallIntegerField(),
        default=list,
    )

    power_data = ArrayField(
        models.SmallIntegerField(),
        default=list,
    )

    def __str__(self):
        return (f'Medición: {self.measure_date}',
                f'temperatura: {self.temperature}')

    class Meta:
        verbose_name = 'PV Data'
        verbose_name_plural = 'PV Data'
