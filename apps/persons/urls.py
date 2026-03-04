from django.urls import path
from apps.persons.controllers import person_controller
from apps.persons.controllers.person_controller import (
    index,
    create,
    edit,
    store,
    delete,
    update,
)

# URL patterns for the persons app, mapping URLs to their corresponding views.
app_name = "persons"

# Define the URL patterns for the persons app, mapping URLs to their corresponding views.
urlpatterns = [
    path("", index, name="index"),
    path("create/", create, name="create"),
    path("store/", store, name="store"),
    path("edit/<int:person_id>/", edit, name="edit"),
    path("delete/<int:person_id>/", delete, name="delete"),
    path("update/<int:person_id>/", update, name="update"),
]
