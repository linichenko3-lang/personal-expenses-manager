from rest_framework.permissions import BasePermission


class IsTransactionOwner(BasePermission):
    """
    Дозволяє доступ до транзакції лише її власнику.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user