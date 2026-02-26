from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Category(models.Model):
    c_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.c_name} '


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME='income',
        EXPENSE='Expense'
    t_name=models.CharField(max_length=100)
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    type=models.CharField(choices=Type.choices,default=Type.EXPENSE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(default=datetime.now)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.t_name} - {self.amount} - {self.type}  - {self.category}  -{self.date}"




    
