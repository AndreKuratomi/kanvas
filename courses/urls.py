from rest_framework.urls import path

from courses.views import CoursesView, CourseByIdView, RegisterInstructorToCourseView, EnrollStudentToCourseView

urlpatterns = [
    path('courses/', CoursesView.as_view()),
    path('courses/<course_id>/', CourseByIdView.as_view()),
    path('courses/<course_id>/registrations/instructor', RegisterInstructorToCourseView.as_view()),
    path('courses/<course_id>/registrations/students', EnrollStudentToCourseView.as_view())
]
