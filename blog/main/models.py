from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Kategoriya modeli, kurslar kategoriyasini ifodalaydi.

    Atributlar:
        name (str): Kategoriyaning nomi.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Kurs modeli, kursni ifodalaydi.

    Atributlar:
        title (str): Kursning sarlavhasi.
        description (str): Kurs haqida batafsil tavsif.
        category (ForeignKey): Bu kurs tegishli bo'lgan kategoriya.
        instructor (ForeignKey): Kursning o'qituvchisi (User).
        created_at (DateTimeField): Kurs yaratilgan vaqt.
        updated_at (DateTimeField): Kurs oxirgi marta yangilangan vaqt.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    """
    Bo'lim modeli, kurs bo'limini ifodalaydi.

    Atributlar:
        course (ForeignKey): Bu bo'lim tegishli bo'lgan kurs.
        title (str): Bo'limning sarlavhasi.
        order (int): Kursdagi bo'limning tartibi.
    """
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Dars modeli, bo'lim ichidagi darsni ifodalaydi.

    Atributlar:
        section (ForeignKey): Bu dars tegishli bo'lgan bo'lim.
        title (str): Darsning sarlavhasi.
        content (str): Dars mazmuni.
        order (int): Bo'limdagi darsning tartibi.
        video (FileField): Darsga tegishli bo'lgan video fayl (ixtiyoriy).
    """
    section = models.ForeignKey(Section, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Izoh modeli, darsga yozilgan izohni ifodalaydi.

    Atributlar:
        lesson (ForeignKey): Bu izoh tegishli bo'lgan dars.
        user (ForeignKey): Izohni yozgan foydalanuvchi.
        comment (str): Izoh mazmuni.
        created_at (DateTimeField): Izoh yozilgan vaqt.
    """
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Rating(models.Model):
    """
    Baholash modeli, darsga foydalanuvchining bahosini ifodalaydi.

    Atributlar:
        lesson (ForeignKey): Baholangan dars.
        user (ForeignKey): Bahoni bergan foydalanuvchi.
        rating (str): Berilgan baho (yoqdi yoki yoqmadi).
        created_at (DateTimeField): Baho berilgan vaqt.
    """
    lesson = models.ForeignKey(Lesson, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=[('liked', 'Yoqdi'), ('disliked', 'Yoqmadi')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.lesson.title} darsini {self.rating} deb baholadi."


class Enrollment(models.Model):
    """
    Ro'yxatdan o'tish modeli, foydalanuvchining kursga ro'yxatdan o'tishini ifodalaydi.

    Atributlar:
        user (ForeignKey): Ro'yxatdan o'tgan foydalanuvchi.
        course (ForeignKey): Foydalanuvchi ro'yxatdan o'tgan kurs.
        enrolled_at (DateTimeField): Foydalanuvchi ro'yxatdan o'tgan vaqt.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} kursiga ro'yxatdan o'tgan."
