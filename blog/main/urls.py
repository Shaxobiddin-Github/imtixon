from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LessonViewSet, CourseViewSet, CategoryViewSet,
                    RegisterView,EnrollmentViewSet,LogoutView,
                    SectionViewSet, CommentViewSet, RatingViewSet
                    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'


router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'register', RegisterView, basename='register')
# router.register(r'logout', LogoutView, basename='logout')


urlpatterns = [
    path('', include(router.urls)),  
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)