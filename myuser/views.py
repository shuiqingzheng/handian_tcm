from .serializers import MyUserSerializer, PasswordSerializer
from .models import MyUser
from rest_framework import generics
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope


class RegisterView(generics.CreateAPIView):
    """
    : 注册
    """
    permission_classes = []
    serializer_class = MyUserSerializer


class PasswordView(generics.GenericAPIView):
    """
    : 修改密码(已知旧密码)
    """
    permission_classes = [TokenHasScope, ]
    required_scopes = ['user:password']
    serializer_class = PasswordSerializer
    queryset = MyUser.objects.all()

    def post(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
