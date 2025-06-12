
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from apps.user.api.serializers import UserLoginSerializer, UserProfileResponseSerializer, UserProfileSeralizer, UserRegistrationSerializer
from apps.user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    response_serializer_class = UserProfileResponseSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            **self.response_serializer_class(
                    instance=user,
                    context={'request': request}
                ).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
        
        
class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    response_serializer_class = UserProfileResponseSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': self.response_serializer_class(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
   
        
class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSeralizer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'