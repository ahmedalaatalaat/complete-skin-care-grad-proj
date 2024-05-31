from django.urls import path
from . import views

app_name = "skincare"

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="register"),
    path('skin_recognition/', views.SkinRecognitionView.as_view(), name='skin_recognition'),
    path('skin_disease/', views.SkinDiseaseView.as_view(), name='skin_disease'),
    path('diseases_history/', views.DiseasesHistoryView.as_view(), name='diseases_history'),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('reset_password/', views.ResetUserPasswordView.as_view(), name="reset_password"),
    # path('skin_burn_degree/', views.SkinBurnDegree.as_view(), name='skin_burn_degree'),
]
