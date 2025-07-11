from django.db import models

class Loan(models.Model):
    borrower_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    ])

    def __str__(self):
        return f"{self.borrower_name} - {self.amount}"