from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SUPERADMIN'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Machine(models.Model):
    machine_id = models.CharField(max_length=50, unique=True)
    machine_name = models.CharField(max_length=100)
    tool_capacity = models.IntegerField()
    tool_offset = models.FloatField()
    feedrate = models.FloatField()
    tool_in_use = models.IntegerField()

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return f'{self.machine_name} - {self.machine_id}'

class Axis(models.Model):
    AXIS_CHOICES = (
        ('X', 'X'),
        ('Y', 'Y'),
        ('Z', 'Z'),
    )

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='axes')
    axis_name = models.CharField(max_length=1, choices=AXIS_CHOICES)
    max_acceleration = models.FloatField()
    max_velocity = models.FloatField()
    actual_position = models.FloatField()
    target_position = models.FloatField()
    distance_to_go = models.FloatField()
    homed = models.BooleanField(default=False)
    acceleration = models.FloatField()
    velocity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Axis"
        verbose_name_plural = "Axes"

    def __str__(self):
        return f'{self.axis_name} Axis for {self.machine.machine_name}'

    def save(self, *args, **kwargs):
        self.distance_to_go = self.target_position - self.actual_position
        super(Axis, self).save(*args, **kwargs)

class Field(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE)
    field_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
       unique_together = (('machine', 'axis', 'timestamp'),)

    def __str__(self):
        return f'Field for {self.axis.axis_name} on {self.machine.machine_name} at {self.timestamp}'
