from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Faqat is_staff foydalanuvchilarga yozish uchun ruxsat berish,
    boshqa foydalanuvchilarga faqat o'qish (GET) uchun ruxsat berish.
    """

    def has_permission(self, request, view):
        # Agar foydalanuvchi is_staff bo'lsa, barcha amallarga ruxsat ber
        if request.user and request.user.is_staff:
            return True
        
        # Aks holda, faqat GET so'rovlariga ruxsat ber
        return request.method in permissions.SAFE_METHODS  # 'GET', 'HEAD', 'OPTIONS'
