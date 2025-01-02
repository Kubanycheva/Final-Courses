from django.urls import path
from .views import *

urlpatterns = [
    # FOR STUDENT
    path('register-student/', RegisterStudentView.as_view(), name='register-student_list'),
    path('login-student/', CustomStudentLoginView.as_view(), name='login-student_list'),
    path('logout-student/', LogoutStudentView.as_view(), name='logout-student_list'),

    path('student/', StudentListAPIView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentRetrieveUpdateAPIView.as_view(), name='student-detail'),

    path('courses/', CourseStudentListAPIView.as_view(), name='courses-list'),
    path('courses/<int:pk>/', CourseStudentRetrieveAPIView.as_view(), name='courses-detail'),

    path('assignment/', AssignmentListAPIView.as_view(), name='assignment-list'),
    path('assignment/<int:pk>/', AssignmentRetrieveAPIView.as_view(), name='assignment-detail'),
    path('submission/', AssignmentSubmissionListCreateAPIView.as_view(), name='submission-list'),

    path('exam/', ExamListAPIView.as_view(), name='exam-list'),
    path('exam/<int:pk>/', ExamRetrieveAPIView.as_view(), name='exam-detail'),

    path('exam/', ExamListAPIView.as_view(), name='exam-list'),
    path('exam/<int:pk>/', ExamRetrieveAPIView.as_view(), name='exam-detail'),

    path('question/', QuestionListCreateAPIView.as_view(), name='question-list'),

    path('cart/', CartRetrieveAPIView.as_view(), name='cart_detail'),

    path('cart_items/', CartItemListCreateAPIView.as_view(), name='cart_item_list'),
    path('cart_items/<int:pk>/', CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cart_item_detail'),

    path('order/', OrderListCreateAPIView.as_view(), name='order-list'),

    path('review/',ReviewCreateAPIView.as_view(),name='review_create'),

    path('review/<int:pk>/',ReviewDeleteAPIView.as_view(),name = 'review_delete'),


    # FOR TEACHER
    path('register-teacher/', RegisterTeacherView.as_view(), name='register-teacher-list'),
    path('login-teacher/', CustomTeachersLoginView.as_view(), name='login-teacher-list'),
    path('logout-teacher/', LogoutTeacherView.as_view(), name='logout-teacher-list'),


    path('teacher/',TeacherListAPIView.as_view(),name = 'teacher_list'),
    path('teacher/<int:pk>/',TeacherRetrieveUpdateAPIView.as_view(),name = 'teacher_detail'),

    path('lesson/',CourseLanguagesViewSet.as_view(),name = 'course_teacher'),
    path('lesson/<int:pk>/',CourseLanguagesDetailAPIView.as_view(),name = 'course_detail'),

    path('courses_for_teacher/',CourseTeacherListAPIView.as_view(),name = 'course_for_teacher'),
    path('courses_for_teacher/<int:pk>/',CourseTeacherRetrieveAPIView.as_view(),name ='course_detail_for_detail'),

    path('questions/',QuestionTeacherListCreateAPIView.as_view(),name = 'questions_teacher'),

    path('exam/',ExamTeacherListCreateAPIView.as_view(),name = 'exam_list'),

    path('exam/<int:pk>/',ExamTeacherRetrieveUpdateDestroyAPIView.as_view(),name = 'exam_detail')


]