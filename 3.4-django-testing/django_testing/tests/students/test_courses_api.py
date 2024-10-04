from django.conf import settings
from django.core.exceptions import ValidationError
import pytest
from rest_framework.test import APIClient

from students.models import Student, Course
from model_bakery import baker


# Фикстура для api-client
@pytest.fixture
def client():
    return APIClient()


# Фикстура для для фабрики курсов
@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# Фикстура для для фабрики студентов
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# Проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_create_course_and_retrieve(client, course_factory):
    course_name = "Swift For Dummies"
    course = course_factory(name=course_name)

    url = f"/api/v1/courses/{course.id}/"
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == course.id
    assert data["name"] == course_name


# Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_list_courses(client, course_factory):

    courses = course_factory(_quantity=10)
    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

    returned_course_ids = [course["id"] for course in data]
    for course in courses:
        assert course.id in returned_course_ids


# Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_by_id(client, course_factory):

    courses = course_factory(_quantity=10)
    filter_id = courses[0].id

    response = client.get("/api/v1/courses/", {"id": filter_id})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == filter_id


# Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_by_name(client, course_factory):

    courses = course_factory(_quantity=10)
    filter_name = courses[0].name
    response = client.get("/api/v1/courses/", {"name": filter_name})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == filter_name


# Тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    course_name = "CSS. Макетирование сайтов"

    response = client.post("/api/v1/courses/", {"name": course_name})
    assert response.status_code == 201

    response = client.get("/api/v1/courses/", {"name": course_name})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == course_name


# Тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_name = "Python. Основы программирования"
    course = course_factory(name=course_name)
    new_course_name = "Python-разработчик: расширенный курс"

    url = f"/api/v1/courses/{course.id}/"
    response = client.put(url, {"name": new_course_name})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_course_name

    course.refresh_from_db()
    assert course.name == new_course_name


# Тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_name = "JavaScript. Пособия для начинающих"
    course = course_factory(name=course_name)

    url = f"/api/v1/courses/{course.id}/"
    response = client.delete(url)

    assert response.status_code == 204

    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


# Тест валидации на максимальное число студентов на курсе
@pytest.mark.django_db
@pytest.mark.parametrize(
    "num_students, expected_success",
    [
        (settings.MAX_STUDENTS_PER_COURSE - 1, True),
        (settings.MAX_STUDENTS_PER_COURSE, True),
        (settings.MAX_STUDENTS_PER_COURSE + 1, False),
    ],
)
def test_student_limit_on_course(
    student_factory, course_factory, num_students, expected_success
):
    course_name = "Python. Основы программирования"
    course = course_factory(name=course_name)
    students = student_factory(_quantity=num_students)

    for student in students:
        course.students.add(student)

    if expected_success:
        course.clean()
    else:
        with pytest.raises(
            ValidationError,
            match=f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}",
        ):
            course.clean()
