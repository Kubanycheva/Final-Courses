from .models import Course, Skills, CourseLanguages, Category, Lesson, Assignment
from modeltranslation.translator import TranslationOptions, register


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Skills)
class CourseTranslationOptions(TranslationOptions):
    fields = ('skills',)


@register(CourseLanguages)
class CourseTranslationOptions(TranslationOptions):
    fields = ('language',)


@register(Category)
class CourseTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Lesson)
class CourseTranslationOptions(TranslationOptions):
    fields = ('lesson_name', 'content')


@register(Assignment)
class CourseTranslationOptions(TranslationOptions):
    fields = ('assignment_name', 'description')