
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Category, Course, Section, Lesson, Enrollment, Comment, Rating
from .permissions import IsStaffOrReadOnly
from .serializers import (CategorySerializer, CourseSerializer, 
                          SectionSerializer, LessonSerializer,
                         EnrollmentSerializer,UserSerializer,
                         CommentSerializer, RatingSerializer,
                         )




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'created_at']
    filterset_fields = ['category']

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'course']
    filterset_fields = ['course']

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title','section']
    filterset_fields = ['section']

    

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['user', 'course']

    def perform_create(self, serializer):   
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['lesson__title']
    ordering_fields = ['lesson', 'user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Faqat autentifikatsiya qilingan foydalanuvchilar

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Avtomatik foydalanuvchini saqlash





# ------------------------------AUTHINTICATION ------------------------------

class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)




# ----------------------------------SEND_EMAIL --------------------------------





from django.shortcuts import get_object_or_404
from .models import Course, Enrollment


def send_update_email(user_email, update_message):
    subject = 'Platforma yangilanishlari'
    message = f'Yangilanish haqida ma\'lumot:\n\n{update_message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)

def update_course(course):
    # Kurs yangilanishi bilan bog'liq amallar
    update_message = f'Kurs "{course.title}" yangilandi.'
    
    # Barcha foydalanuvchilar uchun email yuborish
    for enrollment in course.enrollment_set.all():
        send_update_email(enrollment.user.email, update_message)

# Kurs yangilanishi uchun view misoli
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Yangilanishlar vaqti
        update_course(course)  # Yangilanishlar bilan bog'liq email yuborish
        # Kursni saqlash va boshqa amallar