from django.db import models
from django.contrib.auth.models import User
import string
import random


class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class PromoCode(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='promo_codes')
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        while True:
            code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8))
            if not PromoCode.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f"{self.code} - {self.partner.company_name}"
