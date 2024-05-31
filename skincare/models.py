from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models


class Patient(models.Model):
    GenderTypes = (
        ('M', "Male"),
        ("F", "Female"),
    )
    
    phone = models.CharField(max_length=20)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="patient_images/", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderTypes, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_user")

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.user.username



class SkinRecognitionResult(models.Model):
    image = models.ImageField(upload_to='skin_recognition/')
    detection = models.CharField(max_length=100, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_skin_recognitions")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Skin Recognition Result"
        verbose_name_plural = "Skin Recognition Results"

    def __str__(self):
        return self.image.name


class SkinDiseaseResult(models.Model):
    image = models.ImageField(upload_to='skin_Disease/')
    detection = models.CharField(max_length=100, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_skin_diseases")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Skin Disease Result"
        verbose_name_plural = "Skin Disease Results"

    def __str__(self):
        return self.image.name


class SkinBurnDegreeResult(models.Model):
    image = models.ImageField(upload_to='skin_burn_degree/')
    detection = models.CharField(max_length=100, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_skin_burns")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Skin Burn Degree Result"
        verbose_name_plural = "Skin Burn Degree Results"

    def __str__(self):
        return self.image.name


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created=False, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)

