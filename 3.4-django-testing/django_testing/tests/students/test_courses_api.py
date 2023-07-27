import pytest
import string
import random

from django_testing import settings
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course = course_factory(_quantity=1)[0]
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_courses(api_client, course_factory):
    courses = course_factory(_quantity=15)
    response = api_client.get('/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_get_course_by_id(api_client, course_factory):
    courses = course_factory(_quantity=15)
    for course in courses:
        url = reverse('courses-list')
        response = api_client.get(url, {'id': course.id})
        assert response.status_code == 200
        data = response.json()[0]
        assert data['name'] == course.name


@pytest.mark.django_db
def test_get_course_by_name(api_client, course_factory):
    courses = course_factory(_quantity=15)
    for course in courses:
        url = reverse('courses-list')
        response = api_client.get(url, {'name': course.name})
        assert response.status_code == 200
        data = response.json()[0]
        assert data['id'] == course.id


@pytest.mark.django_db
def test_create_course(api_client):
    course_name = ''.join(random.choices(string.ascii_letters, k=10))
    url = reverse('courses-list')
    response = api_client.post(url, {'name': course_name})
    assert response.status_code == 201
    course_id = response.json()['id']
    course = Course.objects.filter(id=course_id)[0]
    assert course.name == course_name


@pytest.mark.django_db
def test_update_course(api_client):
    course_name = ''.join(random.choices(string.ascii_letters, k=10))
    course = Course.objects.create(name=course_name)
    new_course_name = ''.join(random.choices(string.ascii_letters, k=10))
    url = reverse('courses-detail', args=[course.id])
    response = api_client.patch(url, {'name': new_course_name})
    course.refresh_from_db()
    assert response.status_code == 200
    assert course.name == new_course_name
    assert course.name != course_name


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory(_quantity=1)[0]
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    with pytest.raises(Course.DoesNotExist):
        course.refresh_from_db()


@pytest.mark.django_db
@pytest.mark.parametrize('students_count, expected_status', [
    (3, 400),
    (2, 201),
])
def test_add_student_to_course(api_client, student_factory, students_count, expected_status):
    settings.MAX_STUDENTS_PER_COURSE = 3
    course = Course.objects.create(name="Sample Course")
    students = student_factory(_quantity=students_count+1)
    for i in range(students_count):
        course.students.add(students[i])
    url = reverse('courses-student', args=[course.id])
    response = api_client.post(url, {'student_id': students[students_count].id})
    assert response.status_code == expected_status
    if expected_status == 201:
        course.refresh_from_db()
        assert course.students.count() == 3


