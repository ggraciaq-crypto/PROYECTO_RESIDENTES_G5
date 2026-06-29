from django.db import models

class Residente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Vivienda(models.Model):
    numero = models.CharField(max_length=10)
    bloque = models.CharField(max_length=10)
    estado = models.CharField(max_length=20)
    residente = models.ForeignKey(
        Residente,
        on_delete=models.CASCADE,
        related_name="viviendas"
    )

    def __str__(self):
        return f"Vivienda {self.numero} - Bloque {self.bloque}"
    
class Visita(models.Model):

    ESTADOS = [
        ("En curso", "En curso"),
        ("Finalizada", "Finalizada"),
        ("Cancelada", "Cancelada"),
    ]

    nombre_visitante = models.CharField(max_length=100)
    documento = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)

    placa = models.CharField(max_length=10, blank=True, null=True)

    motivo = models.CharField(max_length=150)
    observaciones = models.TextField(blank=True, null=True)

    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(blank=True, null=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default="En curso")

    vivienda = models.ForeignKey(
        Vivienda,
        on_delete=models.CASCADE,
        related_name="visitas"
    )

    def __str__(self):
        return f"{self.nombre_visitante} - {self.vivienda.numero}"