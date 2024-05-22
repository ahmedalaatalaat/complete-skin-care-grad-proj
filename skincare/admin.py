from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(SkinRecognitionResult)
admin.site.register(SkinBurnDegreeResult)
admin.site.register(SkinDiseaseResult)

