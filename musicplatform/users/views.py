from django.contrib.auth import login
from django.forms.models import model_to_dict
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from users.models import User


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]

            if request.data["bio"]:
                bio = request.data["bio"]
                User.objects.create_user(username=username, password=password, bio=bio)
            else:
                User.objects.create_user(username=username, password=password)

        except Exception as e:
            return Response({"detail": repr(e)}, status=403)
        return Response({"success": username}, status=201)
