from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import LoanApplicationForm
from .models import LoanApplication
from django.contrib import messages
import joblib
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd

rf_pipeline = joblib.load('bank/ml_models/rf_pipeline.pkl')

def loan_application_view(request):
    prediction = None
    application_status = None

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("Form is valid. Received data:", data)

            input_features = {
                'no_of_dependents': [data['no_of_dependents']],
                'education': [data['education']],
                'self_employed': [data['self_employed']],
                'income_annum': [data['income_annum']],
                'loan_amount': [data['loan_amount']],
                'loan_term': [data['loan_term']],
                'cibil_score': [data['cibil_score']],
                'residential_assets_value': [data['residential_assets_value']],
                'commercial_assets_value': [data['commercial_assets_value']],
                'luxury_assets_value': [data['luxury_assets_value']],
                'bank_asset_value': [data['bank_asset_value']],
            }

            input_df = pd.DataFrame(input_features)

            prediction = rf_pipeline.predict(input_df)[0]


            if prediction == " Approved":
                application_status = 'approved'
            elif prediction == " Rejected":
                application_status = 'rejected'

        

    else:
        form = LoanApplicationForm()

    return render(request, 'bank/apply_loan.html', {
        'form': form,
        'prediction': application_status,
    })

def home(request):
    return render(request, 'bank/home.html')

def services(request):
    return render(request, 'bank/services.html')

def about(request):
    return render(request, 'bank/about.html')

def testimonials(request):
    return render(request, 'bank/testimonials.html')

def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect('application_result', application_id=application.application_id)
    else:
        form = LoanApplicationForm()

    return render(request, 'bank/apply_loan.html', {'form': form})

def application_result(request, application_id):
    application = get_object_or_404(LoanApplication, application_id=application_id)

    status = 'approved' if application.is_approved else 'rejected'

    context = {
        'application': application,
        'total_assets': application.total_assets(),
        'application_date': application.created_at.strftime('%B %d, %Y'),
        'status': status,
    }

    if status == 'approved':
        template = 'bank/application_approved.html'
    else:
        template = 'bank/application_rejected.html'

    return render(request, template, context)
