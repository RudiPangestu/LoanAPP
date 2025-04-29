from django.db import models
import uuid
from django.utils import timezone

class LoanApplication(models.Model):
    EDUCATION_CHOICES = (
        ('Graduate','Graduate'),
        ('Not Graduate', 'Not Graduate'),
    )
    
    EMPLOYMENT_CHOICES = (
        ('Yes','Yes'),
        ('No','No'),
    )
    
    application_id = models.CharField(max_length=20, unique=True, editable=False)
    no_of_dependents = models.IntegerField()
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    self_employed = models.CharField(max_length=5, choices=EMPLOYMENT_CHOICES)
    income_annum = models.DecimalField(max_digits=12, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_term = models.IntegerField(help_text="Term in years")
    cibil_score = models.IntegerField()
    residential_assets_value = models.DecimalField(max_digits=12, decimal_places=2)
    commercial_assets_value = models.DecimalField(max_digits=12, decimal_places=2)
    luxury_assets_value = models.DecimalField(max_digits=12, decimal_places=2)
    bank_asset_value = models.DecimalField(max_digits=12, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.application_id:
            # Generate application ID (SB + random numbers)
            self.application_id = f"SB{uuid.uuid4().hex[:6].upper()}"
    
            
        super().save(*args, **kwargs)
    

    def total_assets(self):
        return (
            self.residential_assets_value + 
            self.commercial_assets_value + 
            self.luxury_assets_value + 
            self.bank_asset_value
        )
    
    def __str__(self):
        return f"Loan Application {self.application_id}"