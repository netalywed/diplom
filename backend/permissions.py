from rest_framework.permissions import BasePermission


class IsOwnerOrReader(BasePermission):
    def has_object_permission(self, request, view, obj):  # вшитый метод, проверяем права клиента на конкретный объект
        if request.method == 'GET':
            return True
        return request.user == obj.user


class IsSeller(BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user == obj.user
