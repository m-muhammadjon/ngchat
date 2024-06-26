from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User

from .serializers import UserListSerializer


class UserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


__all__ = ["UserListAPIView"]
