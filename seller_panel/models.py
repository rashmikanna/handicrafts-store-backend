#models for seller account

from django.db import models
from django.contrib.auth.models import User

class SellerProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name       = models.CharField(max_length=100)
    craft_category  = models.CharField(max_length=100)
    district        = models.CharField(max_length=50)
    village         = models.CharField(max_length=100)
    govt_id_type    = models.CharField(max_length=50)   # e.g. Aadhar, Voter ID
    govt_id_number  = models.CharField(max_length=50)
    id_document     = models.FileField(upload_to='seller_ids/')
    bank_account_no = models.CharField(max_length=50)
    bank_ifsc       = models.CharField(max_length=20)
    approved        = models.BooleanField(default=False)
    applied_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.shop_name})"

