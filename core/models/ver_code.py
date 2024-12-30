from django.utils import timezone
from django.db import models
from random import randint
from django.conf import settings
from hashlib import sha256

class VerificationCode(models.Model):
    code = models.CharField(max_length=64)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return f"/verify_email/"

    def is_expired(self):
        current_time = timezone.now() - self.created_at 

        if current_time > timezone.timedelta(minutes=settings.EMAIL_VALIDATION_TIME_INTERVAL):
            return True

        return False

    def save(self, *args, **kwargs):
        self.code = sha256((self.email+str(self.created_at)).encode("utf-8")).hexdigest()
        return super(VerificationCode, self).save(*args, **kwargs)
