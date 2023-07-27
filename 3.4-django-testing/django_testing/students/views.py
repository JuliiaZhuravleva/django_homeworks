from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_testing import settings
from students.filters import CourseFilter
from students.models import Course, Student
from students.serializers import CourseSerializer, StudentSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

    @action(detail=True, methods=['post', 'delete'])
    def student(self, request, pk=None):
        course = self.get_object()

        student_id = request.data.get('student_id')

        if student_id is None:
            return Response({'error': 'Необходимо указать student_id'}, status=400)

        student = Student.objects.filter(pk=student_id).first()
        if not student:
            return Response({"detail": "Студента с таким id не существует."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            max_students = settings.MAX_STUDENTS_PER_COURSE
            if course.students.count() >= max_students:
                return Response({'error': f'Максимальное количество студентов на курсе {max_students}'}, status=400)
            # Добавить студента на курс
            course.students.add(student)
            return Response({"detail": "Студент добавлен на курс."}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            # Удалить из избранного
            course.students.remove(student)
            return Response({"detail": "Объявление удалено из избранного."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Недопустимый HTTP-метод."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StudentsViewSet(ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
