from django.db import models
from users.models import User


class InsurancePrediction(models.Model):
    SMOKER_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    REGION_CHOICES = [
        ('northeast', 'Northeast'),
        ('northwest', 'Northwest'),
        ('southeast', 'Southeast'),
        ('southwest', 'Southwest'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_predictions')
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField(verbose_name="BMI")
    children = models.IntegerField(default=0)
    smoker = models.CharField(max_length=3, choices=SMOKER_CHOICES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)
    predicted_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - ${self.predicted_cost} on {self.created_at.date()}"
