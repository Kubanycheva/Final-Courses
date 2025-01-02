from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Teacher(UserProfile):
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    expertise = models.CharField(max_length=255, verbose_name="Основная область знаний преподавателя")
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name="Опыт работы в годах")
    social_links = models.URLField(blank=True, verbose_name="Ссылки на соцсети")
    date_registered = models.DateField(auto_now=True)

    def __str__(self):
        return self.username


class Student(UserProfile):
    student_images = models.ImageField(upload_to='student_images/', null=True, blank=True)
    bio_student = models.TextField(null=True, blank=True)
    grade_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'beginnet'),
            ('intermediate', 'intermediate'),
            ('advanced', 'advanced')
        ],
        default='beginner',
    )
    GRADE_LEVEL = (
        ('Beginner', 'beginner'),
        ('Intermediate', 'intermediate'),
        ('Advanced', 'advanced'),
    )
    grade_level = models.CharField(max_length=50, choices=GRADE_LEVEL)
    date_registered = models.DateField(auto_now=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Skills(models.Model):
    skills = models.CharField(max_length=155, null=True, blank=True, verbose_name='Навыки')

    def __str__(self):
        return self.skills


class Course(models.Model):
    course_name = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skills, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses_student')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses_teacher')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    LEVEL_CHOICES = (
        ('Начальный', 'начальный'),
        ('Средний', 'средний'),
        ('Продвинутый', 'продвинутый'),
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    course_images = models.ImageField(upload_to='course_images/', null=True, blank=True )
    DURATION_CHOICES = (
        ('Менее 2 часов', 'Менее 2 часов'),
        ('1–4 недели', '1–4 недели'),
        ('1–3 месяца', '1–3 месяца'),
        ('3–6 месяцев', '3–6 месяцев'),

    )
    duration = models.CharField(max_length=40, choices=DURATION_CHOICES)

    def __str__(self):
        return self.course_name


    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.stars for i in ratings) / ratings.count(), 1)
        return 0

    def get_total_people(self):
        ratings = self.reviews.all()
        if ratings.exists():
            if ratings.count() > 10000:
                return '10000+'
            return ratings.count()
        return 0


class CourseLanguages(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_languages')
    language = models.CharField(max_length=35)
    video_filed = models.FileField(upload_to='course_languages_video/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    course = models.ForeignKey(Course, related_name='course_languages', on_delete=models.CASCADE)

    def __str__(self):
        return self.language


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lesson')
    lesson_name = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(blank=True, null=True)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.lesson_name


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=255)
    teacher = models.ManyToManyField(Teacher, related_name='assignment')
    students = models.ManyToManyField(Student)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.assignment_name


class AssignmentSubmission(models.Model):
    students = models.ManyToManyField(UserProfile, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 101)], null=True, blank=True,
                                             verbose_name='Оценка на задачи')

    def __str__(self):
        return f'{self.submission_file}'


class Exam(models.Model):
    exam_name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='exam')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    passing_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 101)], null=True,
                                                     blank=True,
                                                     verbose_name='Оценка на экзамен')
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.exam_name


class Question(models.Model):
    text = models.CharField(max_length=255)  # Текст вопроса
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Choice(models.Model):  # Ответ
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)  # Связь с вопросом
    text = models.CharField(max_length=255)  # Текст варианта ответа
    is_correct = models.BooleanField(default=False)  # Флаг правильного ответа

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Выбранный пользователем ответ
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # Результат проверки (правильно/неправильно)

    def __str__(self):
        return f"{self.student} - {self.question.text}: {self.choice.text} ({'Correct' if self.is_correct else 'Wrong'})"


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)  # Для текстовых ответов
    selected_options = models.ManyToManyField(UserAnswer)  # Для выборочных вопросов


class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificate_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_course')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.URLField(null=True, blank=True)
    certificate_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.certificate_url


class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True,
                                             verbose_name='Рейтинг')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stars} - {self.student.username}'


class Cart(models.Model):
    student = models.OneToOneField(Student, related_name='cart', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def get_total_price(self):
        return self.course.price

    def __str__(self):
        return f'{self.course} - {self.quantity}'


class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.country_name}'


class Order(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='client')
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Оплачено', 'Оплачено'),
        ('Не Оплачено', 'Не Оплачено'),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Ожидает оброботки')
    name_on_the_map = models.CharField(max_length=35, verbose_name='Имя на карте')
    card_number = models.DecimalField(max_digits=16, decimal_places=0)
    expiration_date = models.DateField()
    cvv = models.DecimalField(max_digits=3, decimal_places=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    creates_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.status}'


# class Favorite(models.Model):
#     user = models.ForeignKey(Course, on_delete=models.CASCADE)
#     created_date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user} - {self.created_date}'
#
#
# class FavoriteLesson(models.Model):
#     cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.lesson} - {self.cart}'
#



#
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# class UserProfile(AbstractUser):
#     pass
#
#     def __str__(self):
#         return self.username
#
#
# class Teacher(UserProfile):
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     expertise = models.CharField(max_length=255, help_text="Основная область знаний преподавателя")
#     years_of_experience = models.PositiveIntegerField(default=0, help_text="Опыт работы в годах")
#     social_links = models.URLField(blank=True, help_text="Ссылки на соцсети (например, LinkedIn)")
#     date_registered = models.DateField(auto_now=True)
#     def __str__(self):
#         return self.username
#
#
# class Student(UserProfile):
#     student_images = models.ImageField(upload_to='student_images/', null=True, blank=True)
#     bio_student = models.TextField(blank=True, null=True)
#     grade_level = models.CharField(
#         max_length=50,
#         choices=[
#             ('beginner', 'Начальный'),
#             ('intermediate', 'Средний'),
#             ('advanced', 'Продвинутый')
#         ],
#         default='beginner',
#         help_text="Уровень подготовки студента"
#     )
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_registered = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.username
#
#
# class Category(models.Model):
#     category_name = models.CharField(max_length=255)
#
#
#     def __str__(self):
#         return self.category_name
#
#
# class Skills(models.Model):
#     skills = models.CharField(max_length=155, null=True, blank=True, verbose_name='Навыки')
#
#
#     def __str__(self):
#         return f'{self.skills}'
#
# class Course(models.Model):
#     LEVEL_CHOICES = (
#         ('beginner', 'beginner'),
#         ('intermediate', 'intermediate'),
#         ('advanced', 'advanced'),
#     )
#     course_name = models.CharField(max_length=255)
#     skills = models.ManyToManyField(Skills, related_name='courses')
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
#     level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     students = models.ManyToManyField(Student, related_name='courses_student',null=True,blank=True)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses_teacher')
#     created_at = models.DateField(auto_now=True)
#     updated_at = models.DateField(auto_now=True)
#     course_images = models.ImageField(upload_to='course_images/')
#     DURATION_CHOICES = (
#         ('Менее 2 часов', 'Менее 2 часов'),
#         ('1–4 недели', '1–4 недели'),
#         ('1–3 месяца', '1–3 месяца'),
#         ('3–6 месяцев', '3–6 месяцев'),
#
#     )
#     duration = models.CharField(max_length=40, choices=DURATION_CHOICES)
#
#     def __str__(self):
#         return self.course_name
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['category']),
#             models.Index(fields=['teacher']),
#             models.Index(fields=['level']),
#         ]
#
#     def get_avg_rating(self):
#         ratings = self.reviews.all()
#         if ratings.exists():
#             return round(sum(i.stars for i in ratings) / ratings.count(), 1)
#         return 0
#
#     def get_total_people(self):
#         ratings = self.reviews.all()
#         if ratings.exists():
#             if ratings.count() > 10000:
#                 return '10000+'
#             return ratings.count()
#         return 0
#
#
# class CourseLanguages(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_languages')
#     language = models.CharField(max_length=35)
#     video_filed = models.FileField(upload_to='Course_Languages_video/', null=True, blank=True)
#     video_url = models.URLField(null=True, blank=True)
#     course = models.ForeignKey(Course, related_name='course_languages', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.language
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['language']),
#         ]
#
#
# class Lesson(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lesson')
#     lesson_name = models.CharField(max_length=255)
#     video_url = models.URLField(blank=True, null=True)
#     video_file = models.FileField(blank=True, null=True)
#     content = models.TextField()
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
#
#     def __str__(self):
#         return self.lesson_name
#
#
# class Assignment(models.Model):
#     teacher = models.ManyToManyField(Teacher, related_name='assignment')
#     assignment_name = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateTimeField()
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
#     students = models.ManyToManyField(Student)
#
#     def __str__(self):
#         return self.assignment_name
#
#
# class AssignmentSubmission(models.Model):
#     students = models.ManyToManyField(UserProfile, related_name='submissions')
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
#     submission_file = models.FileField(upload_to='submissions/', blank=True, null=True)
#     grade = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 101)], null=True, blank=True,
#                                              verbose_name='Оценка на задачи')
#
#     submitted_at = models.DateTimeField(auto_now_add=True)
#
#
# class Exam(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='exam')
#     exam_name = models.CharField(max_length=255)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
#     passing_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 101)], null=True,
#                                                      blank=True,
#                                                      verbose_name='Оценка на экзамен')
#     duration = models.PositiveSmallIntegerField()
#
#     def __str__(self):
#         return self.exam_name
#
#
# QUESTION_CHOICES = (
#     ('question_A', 'question_A'),
#     ('question_B', 'question_B'),
#     ('question_C', 'question_C'),
#     ('question_D', 'question_D')
# )
#
#
# class Question(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='question')
#     question_name = models.CharField(max_length=155)
#
#     # question_a = models.CharField(max_length=155)
#     # question_b = models.CharField(max_length=155)
#     # question_c = models.CharField(max_length=155)
#     # question_choices_teacher = models.CharField(max_length=10, choices=QUESTION_CHOICES)
#     # question_choices_student = models.CharField(max_length=10, choices=QUESTION_CHOICES)
#     #
#
#     def __str__(self):
#         return self.question_name
#
#
# class Option(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='option')
#     student = models.ManyToManyField(Student, related_name='option')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='option_question')
#     option_choices = models.CharField(max_length=10, choices=QUESTION_CHOICES)
#     option = models.CharField(max_length=100)
#     option_boolean = models.BooleanField(null=True, blank=True)
#     # question_choices_teacher = models.CharField(max_length=10, choices=QUESTION_CHOICES)
#     question_choices_student = models.CharField(max_length=10, choices=QUESTION_CHOICES)
#
#
# class Certificate(models.Model):
#     student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificate_student')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_course')
#     issued_at = models.DateTimeField(auto_now_add=True)
#     certificate_url = models.URLField(null=True, blank=True)
#     certificate_file = models.FileField(null=True, blank=True)
#
#
# class Review(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
#     stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True,
#                                              verbose_name='Рейтинг')
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.stars} - {self.student.username}'
#
#
# class Cart(models.Model):
#     student = models.OneToOneField(Student, related_name='cart', on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user}'
#
#     def get_total_price(self):
#         total_price = sum(item.get_total_price() for item in self.items.all())
#         return total_price
#
#
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
#
#     def get_total_price(self):
#         return self.course.price
#
#     def __str__(self):
#         return f'{self.course} - {self.quantity}'
#
#
# class Country(models.Model):
#     country_name = models.CharField(max_length=100)
#
#
#     def __str__(self):
#         return f'{self.country_name}'
#
# class Order(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='client')
#     cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
#     STATUS_CHOICES = (
#         ('Оплачено', 'Оплачено'),
#         ('Не Оплачено', 'Не Оплачено'),
#
#     )
#     status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Ожидает оброботки')
#     name_on_the_map = models.CharField(max_length=35, verbose_name='Имя на карте')
#     card_number = models.DecimalField(max_digits=16, decimal_places=0)
#     expiration_date = models.DateField()
#     cvv = models.DecimalField(max_digits=3, decimal_places=0)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     creates_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.student} - {self.status}'
