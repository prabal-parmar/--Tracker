from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    expense_id=models.UUIDField(primary_key=True, default=uuid.uuid4())
    expense=models.PositiveIntegerField(max_length=8)
    reason=models.CharField(max_length=100)
    date=models.DateField()

    def __str__(self):
        return self.reason