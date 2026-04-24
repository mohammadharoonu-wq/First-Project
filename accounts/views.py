from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParent, IsStudent, IsTeacher


# 🔐 Signup API
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User created"})
        return Response(serializer.errors)


# 🔐 Login API
class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": "Invalid credentials"})


# 👨‍🏫 Teacher Dashboard
class TeacherDashboard(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        return Response({"msg": "Teacher Dashboard"})


# 👨‍🎓 Student + Parent Dashboard
class StudentParentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsParent | IsTeacher]

    def get(self, request):
        return Response({"msg": "Student/Parent Dashboard"})