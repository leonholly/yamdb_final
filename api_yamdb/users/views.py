from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminOnly
from .serializers import (SignUpSerializer, TokenCreateSerializer,
                          UserPatchSerializer, UserSerializer)


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    При запросе администратора:
    - возвращает список пользователей
    - возвращает данные пользователя по username
    - создаёт, изменяет, удаляет объект пользователя
    При запросе аутентифицированного пользователя:
    - возвращает данные пользователя
    - изменяет объект пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminOnly,)

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserPatchSerializer(request.user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignUpViewSet(CreateViewSet):
    """
    При запросе анонима:
    - создаёт объект пользователя, отправляет код на почту.
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save()
        email = self.request.data.get('email')
        user = User.objects.get(username=self.request.data.get('username'))
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Get your confirmation code',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=None,
            recipient_list=[email],
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,  # Переопределяю create т.к.
            headers=headers             # по стандарту возвращается код 201,
        )                               # а документация требует код 200


@api_view(http_method_names=['POST'],)
@permission_classes([AllowAny],)
def get_token(request):
    serializer = TokenCreateSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = data.get('confirmation_code')
        code_valid = default_token_generator.check_token(
            user,
            confirmation_code
        )

        if code_valid:
            refresh = RefreshToken.for_user(
                User.objects.get(username=data.get('username'))
            )
            resp = dict()
            resp['token'] = str(refresh.access_token)

            return Response(resp, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
