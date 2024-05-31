from .detection import predict_skin_disease, predict_skin_type, predict_skin_burn
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from core.utils import get_object_or_none
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *


class RegistrationView(APIView):
    def post(self, request):
        user = get_object_or_none(User, username=request.data.get('email'))
        if user:
            return Response({"error": "user already exists!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            my_user = User.objects.create_user(
                username=request.data.get('email'),
                password=request.data.get('password'),
                first_name=request.data.get('name'),
            )
            
            patient = Patient.objects.create(
                phone=request.data.get('phone'),
                birthday=request.data.get('birthday'),
                image=request.FILES.get('image'),
                gender=request.data.get('gender'),
                user=my_user,
            )
            
            token = Token.objects.get(user=my_user)
            
            data = {
                "token": str(token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_none(User, username=request.data.get('email'))
            if not user:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_403_FORBIDDEN)
            
            if user.check_password(request.data.get('password')):
                token = Token.objects.get(user=user)
            
                data = {
                    "token": str(token),
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@parser_classes((MultiPartParser, ))
class ProfileView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        serializer = ProfileSerializer(request.user.patient_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            request.user.first_name = request.data.get('name')
            request.user.patient_user.phone = request.data.get('phone')
            
            if request.data.get('birthday'):
                request.user.patient_user.birthday = request.data.get('birthday')
            
            if request.data.get('gender'):
                request.user.patient_user.gender = request.data.get('gender')
            
            if request.FILES.get('image'):
                request.user.patient_user.image = request.FILES.get('image')
            
            request.user.save()
            request.user.patient_user.save()
            
            serializer = ProfileSerializer(request.user.patient_user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetUserPasswordView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def put(self, request):
        serializer = ResetUserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.check_password(request.data.get("old_password")):
                request.user.set_password(request.data.get('new_password'))
                request.user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@parser_classes((MultiPartParser, ))
class SkinRecognitionView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        skin_recognition_results = SkinRecognitionResult.objects.filter(patient=request.user.patient_user)
        serializer = SkinRecognitionResultSerializer(skin_recognition_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # create skin recognition object in the db
        skin_recognition_result = SkinRecognitionResult.objects.create(
            image=request.FILES.get('image'),
            patient=request.user.patient_user,
        )

        # Perform image detection
        prediction = predict_skin_type(skin_recognition_result.image.path)

        # Save detection results to db 
        skin_recognition_result.detection = prediction
        skin_recognition_result.save()
        
        # Serialize detection result
        serializer = SkinRecognitionResultSerializer(skin_recognition_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@parser_classes((MultiPartParser, ))
class SkinDiseaseView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        skin_disease_results = SkinDiseaseResult.objects.filter(patient=request.user.patient_user)
        serializer = SkinDiseaseResultSerializer(skin_disease_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # create skin recognition object in the db
        skin_disease_result = SkinDiseaseResult.objects.create(
            image=request.FILES.get('image'),
            patient=request.user.patient_user,
        )

        # Perform image detection
        prediction = predict_skin_disease(skin_disease_result.image.path)

        # Save detection results to db 
        skin_disease_result.detection = prediction
        skin_disease_result.save()
        
        # Serialize detection result
        serializer = SkinDiseaseResultSerializer(skin_disease_result, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@parser_classes((MultiPartParser, ))
class SkinBurnDegree(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # create skin recognition object in the db
        skin_burn_result = SkinBurnDegreeResult.objects.create(
            image=request.FILES.get('image'),
            patient=request.user.patient_user,
        )

        # Perform image detection
        prediction = predict_skin_burn(skin_burn_result.image.path)

        # Save detection results to db 
        skin_burn_result.detection = prediction
        skin_burn_result.save()
        
        # Serialize detection result
        serializer = SkinBurnDegreeResultSerializer(skin_burn_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@parser_classes((MultiPartParser, ))
class DiseasesHistoryView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        skin_recognition_results = SkinRecognitionResult.objects.filter(patient=request.user.patient_user)
        skin_recognition_serializer = SkinRecognitionResultSerializer(skin_recognition_results, many=True)
        
        skin_disease_results = SkinDiseaseResult.objects.filter(patient=request.user.patient_user)
        skin_disease_serializer = SkinDiseaseResultSerializer(skin_disease_results, many=True)
        
        data = {
            "skin_recognition_results": skin_recognition_serializer.data,
            "skin_disease_results": skin_recognition_serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED)



# class registerAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = User.objects.create_user(
#                 username=request.data.get('username'),
#                 password=request.data.get('password'),
#             )

#             token = Token.objects.get(user=user)

#             data = {
#                 "token": str(token),
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     def get(self, request):
#         user = get_object_or_404(User, username=request.query_params.get('username'))
#         if user.check_password(request.query_params.get('password')):
#             token = Token.objects.get(user=user)
#             data = {
#                 "token": str(token),
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             data = {
#                 "error": "the user password is incorrect!",
#             }
#             return Response(data, status=status.HTTP_401_UNAUTHORIZED)

