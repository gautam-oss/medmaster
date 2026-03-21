from django import forms
from .models import InsurancePrediction


class InsurancePredictionForm(forms.ModelForm):
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female')]
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = InsurancePrediction
        fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '100', 'placeholder': 'Enter age'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '10', 'max': '60', 'placeholder': 'e.g. 25.5'}),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'placeholder': 'Number of children'}),
            'smoker': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'bmi': 'BMI = weight(kg) / height(m)²',
            'age': 'Must be 18 or older',
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 18:
            raise forms.ValidationError('Age must be at least 18 years.')
        if age and age > 100:
            raise forms.ValidationError('Please enter a valid age.')
        return age

    def clean_bmi(self):
        bmi = self.cleaned_data.get('bmi')
        if bmi and (bmi < 10 or bmi > 60):
            raise forms.ValidationError('Please enter a valid BMI between 10 and 60.')
        return bmi
