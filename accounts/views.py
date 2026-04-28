from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParent, IsStudent, IsTeacher
from rest_framework import status

# 🔐 Signup API
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 🚪 Logout API
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Token is already blacklisted or invalid"}, status=status.HTTP_400_BAD_REQUEST)


# 👨‍🏫 Teacher Dashboard
class TeacherDashboard(APIView):
    
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        return Response({
            "msg": "Welcome to Teacher Dashboard",
            "user": request.user.username
        })


# 👨‍🎓 Student + Parent Dashboard
class StudentParentDashboard(APIView):
    
    permission_classes = [IsAuthenticated, IsStudent | IsParent | IsTeacher]

    def get(self, request):
        return Response({
            "msg": "Student/Parent Dashboard",
            "accessed_by": request.user.username,
            "your_role": request.user.role
        })