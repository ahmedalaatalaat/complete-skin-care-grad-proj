from django.urls import path
from . import views

app_name = "skincare"

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="register"),
    path('skin_recognition/', views.SkinRecognitionView.as_view(), name='skin_recognition'),
    path('skin_disease/', views.SkinDiseaseView.as_view(), name='skin_disease'),
    # path('skin_burn_degree/', views.SkinBurnDegree.as_view(), name='skin_burn_degree'),
]
