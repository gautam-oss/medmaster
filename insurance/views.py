from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models as db_models
from .forms import InsurancePredictionForm
from .models import InsurancePrediction
from .ml_model import predictor


def predict_insurance(request):
    if request.method == 'POST':
        form = InsurancePredictionForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            bmi = form.cleaned_data['bmi']
            children = form.cleaned_data['children']
            smoker = form.cleaned_data['smoker']
            region = form.cleaned_data['region']

            try:
                predicted_cost = predictor.predict(age, sex, bmi, children, smoker, region)

                if request.user.is_authenticated:
                    prediction = form.save(commit=False)
                    prediction.user = request.user
                    prediction.predicted_cost = predicted_cost
                    prediction.save()
                    return redirect('insurance:result', prediction_id=prediction.id)
                else:
                    request.session['guest_prediction'] = {
                        'age': age, 'sex': sex, 'bmi': float(bmi),
                        'children': children, 'smoker': smoker,
                        'region': region, 'predicted_cost': float(predicted_cost),
                    }
                    return redirect('insurance:guest_result')

            except Exception as e:
                messages.error(request, f'Error making prediction: {str(e)}')
    else:
        form = InsurancePredictionForm()

    return render(request, 'insurance/predict.html', {'form': form})


def prediction_result(request, prediction_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view saved predictions.')
        return redirect('users:login')

    prediction = get_object_or_404(InsurancePrediction, id=prediction_id, user=request.user)
    feature_importance = predictor.get_feature_importance()
    risk_factors = _get_risk_factors(prediction.smoker, prediction.bmi, prediction.age)

    return render(request, 'insurance/result.html', {
        'prediction': prediction,
        'feature_importance': feature_importance,
        'risk_factors': risk_factors,
    })


def guest_result(request):
    guest_prediction = request.session.get('guest_prediction')
    if not guest_prediction:
        messages.error(request, 'No prediction data found. Please make a prediction first.')
        return redirect('insurance:predict')

    feature_importance = predictor.get_feature_importance()
    risk_factors = _get_risk_factors(
        guest_prediction['smoker'], guest_prediction['bmi'], guest_prediction['age']
    )

    return render(request, 'insurance/result.html', {
        'prediction': guest_prediction,
        'feature_importance': feature_importance,
        'risk_factors': risk_factors,
        'is_guest': True,
    })


@login_required
def prediction_history(request):
    predictions = InsurancePrediction.objects.filter(user=request.user)
    avg_cost = min_cost = max_cost = None
    if predictions.exists():
        avg_cost = predictions.aggregate(db_models.Avg('predicted_cost'))['predicted_cost__avg']
        min_cost = predictions.aggregate(db_models.Min('predicted_cost'))['predicted_cost__min']
        max_cost = predictions.aggregate(db_models.Max('predicted_cost'))['predicted_cost__max']

    return render(request, 'insurance/history.html', {
        'predictions': predictions,
        'avg_cost': avg_cost,
        'min_cost': min_cost,
        'max_cost': max_cost,
    })


def about_model(request):
    return render(request, 'insurance/about.html', {
        'feature_importance': predictor.get_feature_importance(),
    })


def _get_risk_factors(smoker, bmi, age):
    risk_factors = []
    if smoker == 'yes':
        risk_factors.append({'factor': 'Smoking', 'impact': 'Very High', 'recommendation': 'Quitting smoking can significantly reduce insurance costs'})
    bmi = float(bmi)
    if bmi > 30:
        risk_factors.append({'factor': 'High BMI', 'impact': 'High', 'recommendation': 'Maintaining a healthy weight can lower costs'})
    elif bmi > 25:
        risk_factors.append({'factor': 'Overweight BMI', 'impact': 'Moderate', 'recommendation': 'Consider weight management for better rates'})
    if int(age) > 50:
        risk_factors.append({'factor': 'Age', 'impact': 'Moderate', 'recommendation': 'Regular health checkups are important'})
    return risk_factors
