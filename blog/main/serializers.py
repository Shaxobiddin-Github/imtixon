from rest_framework import serializers
from .models import Category, Course, Section, Lesson, Enrollment, Comment, Rating
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    """
    Kategoriya modelini serializer.
    Kategoriyalarning barcha maydonlarini seriyalash imkonini beradi.
    """
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    """
    Kurs modelini serializer.
    Kurslarning barcha maydonlarini seriyalash imkonini beradi.
    """
    class Meta:
        model = Course
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    """
    Bo'lim modelini serializer.
    Bo'limlarning barcha maydonlarini seriyalash imkonini beradi.
    """
    class Meta:
        model = Section
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    """
    Dars modelini serializer.
    Darslarning barcha maydonlarini seriyalash imkonini beradi.
    """
    class Meta:
        model = Lesson
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Ro'yxatdan o'tish modelini serializer.
    Foydalanuvchi haqida ma'lumotlarni o'qish mumkin, lekin yozish mumkin emas.
    """
    user = serializers.ReadOnlyField(source='user.username')
   
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'enrolled_at', 'course']

class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi modelini serializer.
    Foydalanuvchilarni yaratish va ma'lumotlarni olish imkonini beradi.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Foydalanuvchini yaratish.
        Parolni shifrlash va foydalanuvchini saqlash.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CommentSerializer(serializers.ModelSerializer):
    """
    Izoh modelini serializer.
    Foydalanuvchilarning izohlarini seriyalash imkonini beradi.
    """
    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = Comment
        fields = ['lesson', 'user', 'comment', 'created_at']
        read_only_fields = ['user']

class RatingSerializer(serializers.ModelSerializer):
    """
    Baho modelini serializer.
    Foydalanuvchilarning darslarga bergan baholarini seriyalash imkonini beradi.
    """
    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = Rating
        fields = ['lesson', 'rating', 'user']
        read_only_fields = ['user']
