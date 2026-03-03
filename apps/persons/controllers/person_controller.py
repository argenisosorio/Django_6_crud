from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from apps.persons.dtos.person_dto import PersonDTO, UpdatePersonDTO
from apps.persons.models.person import Person
from apps.persons.requests.create_person import CreatePersonRequest
from apps.persons.requests.update_person import UpdatePersonRequest
from apps.persons.services import person_service


def index(request):
    persons = person_service.get_all_persons()
    context = {"persons": persons}
    return render(request, "persons/index.html", context)


@require_GET
def create(request: HttpRequest) -> HttpResponse:
    return render(request, "persons/create_person.html")


def edit(request, person_id):
    person = person_service.get_person(person_id)
    context = {"person": person}
    return render(request, "persons/update.html", context)


@require_POST
def store(request: HttpRequest) -> HttpResponse:
    form = CreatePersonRequest(request.POST)

    if not form.is_valid():
        return HttpResponse(f"Invalid data: {form.errors}", status=400)

    person_dto = PersonDTO(**form.cleaned_data)
    person_service.create_person(person_dto)
    return redirect(reverse("persons:index"))


def delete(request: HttpRequest, person_id: int) -> HttpResponse:
    person_service.delete_person(person_id)
    return redirect(reverse("persons:index"))


def update(request: HttpRequest, person_id: int) -> HttpResponse:
    person_data = UpdatePersonRequest(request.POST)
    if not person_data.is_valid():
        return HttpResponse(f"Invalid data: {person_data.errors}", status=400)

    person_dto = UpdatePersonDTO(**person_data.cleaned_data)
    person_service.update_person(person_id, person_dto)
    return redirect(reverse("persons:index"))
