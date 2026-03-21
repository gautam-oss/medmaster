from django.contrib import admin
from .models import InsurancePrediction


@admin.register(InsurancePrediction)
class InsurancePredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'bmi', 'smoker', 'predicted_cost', 'created_at')
    list_filter = ('smoker', 'region', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
