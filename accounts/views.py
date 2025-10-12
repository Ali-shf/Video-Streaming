from datetime import timedelta
from django.utils import timezone
from rest_framework import status, generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from accounts.models import User
from accounts.serializers import (
    RegistrationModelSerializer,
    UserSerializer,
    UserProfileSerializer,
    UpdateUserSerializer,
)

# --------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegistrationModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        self.response = Response(
            {
                "message": "User registered successfully.",
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

        # Set cookies
        self.response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(minutes=30),
            samesite="Lax",
        )
        self.response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(days=7),
            samesite="Lax",
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return getattr(self, "response", response)


# --------------------------------------------------------------------
# Login
# --------------------------------------------------------------------
class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "message": "Login successful.",
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(minutes=30),
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(days=7),
            samesite="Lax",
        )

        return response


# --------------------------------------------------------------------
# Refresh Token
# --------------------------------------------------------------------
class RefreshTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({"message": "Access token refreshed."})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(minutes=30),
            samesite="Lax",
        )
        return response


# --------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------
class LogoutUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        response = Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


# --------------------------------------------------------------------
# Profile Views
# --------------------------------------------------------------------
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# --------------------------------------------------------------------
# Admin Views
# --------------------------------------------------------------------
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_object(self):
        user_id = self.request.query_params.get("user_id")
        if not user_id:
            raise serializers.ValidationError({"error": "user_id query parameter is required."})
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found."})


class UpdateUserView(generics.GenericAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "user_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User updated successfully.", "user": UserProfileSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class DeleteUserView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "user_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        username = user.username
        user.delete()

        return Response(
            {"message": f"User '{username}' deleted and tokens invalidated."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ChangeUserRoleView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateUserSerializer

    def patch(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "user_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        is_admin = request.data.get("is_admin")
        if is_admin is None:
            return Response({"error": "is_admin field is required."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_staff = bool(is_admin)
        user.save()

        return Response(
            {"message": "User role updated successfully.", "user": UserProfileSerializer(user).data},
            status=status.HTTP_200_OK,
        )
