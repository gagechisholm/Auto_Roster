from django.db import models
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return f'{self.rank} {self.last_name} {self.first_name}'
    
class Shift(models.Model):
    date = models.DateField()
    assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'Duty on {self.date}'
    
class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['employee', 'date']
        
    def __str__(self):
        return f'{self.employee} - {"Available" if self.is_available else "Unavailable"} on {self.date}'
    
class DutyRoster(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ['employee', 'date']
        
    def __str__(self):
        return f'{self.employee} - Duty on {self.date}'