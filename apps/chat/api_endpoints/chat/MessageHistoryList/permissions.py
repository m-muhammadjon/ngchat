from rest_framework.permissions import BasePermission


class IsConversationParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user in view.get_object().participants.all()
