from django.db import models
from django.contrib.auth.models import User
import uuid 
from decimal import Decimal

class MonthWise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()  
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    per_day_salary = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    per_minute_salary = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    working_hours_per_day = models.PositiveIntegerField()

    def __str__(self):
        return self.month.strftime('%m-%Y')



class Expense(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False)
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    time_value_in_hours = models.CharField(max_length=200,blank=True, null=True)
    month_wise = models.ForeignKey(MonthWise, on_delete=models.CASCADE)

    def __str__(self):
        return f'Expense on {self.date}: {self.amount}'

    def save(self, *args, **kwargs):
        # Automatically calculate time_value before saving
        if not self.time_value:
            # Time spent on the expense = amount / perDaySalary (in minutes)
            time_in_minutes = Decimal(self.amount) / Decimal(self.month_wise.per_minute_salary)
            self.time_value = time_in_minutes  # This will store the time value in minutes.

            hour = time_in_minutes // 60  # Integer division (gives full hours)
            minutes = round(time_in_minutes % 60)  # Remainder is the minutes

            # Assign to the 'time_value_in_hours' attribute as a string
            self.time_value_in_hours = str(hour) + ' hrs ' + str(minutes) + ' mins.'
        super(Expense, self).save(*args, **kwargs)
