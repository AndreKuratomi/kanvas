from rest_framework.urls import path

from courses.views import CoursesView, CourseByIdView

urlpatterns = [
    path('courses/', CoursesView.as_view()),
    path('courses/<course_id>/', CourseByIdView.as_view()),
    path('courses/<course_id>/registrations/instructor', CourseByIdView.as_view())
]
