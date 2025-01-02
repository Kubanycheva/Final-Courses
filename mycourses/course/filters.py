from django_filters.rest_framework import FilterSet
from .models import Course


class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'category': ['exact'],
            'level': ['exact'],
            'teacher': ['exact'],
            'duration': ['exact'],
            'skills': ['exact'],
            'course_languages': ['exact'],
        }