from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # SAFE METHODS : GET, HEAD, OPTIONS
            return True 
        return (request.user and request.user.is_authenticated)

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')