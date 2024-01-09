from django.urls import path
from . import views
urlpatterns = [
    path("", views.Home, name="Home"),
    path("signup/", views.signup, name="Signup"),
    path("tasks/", views.tasks, name="Tasks"),
    path("tasks/completed", views.tasks_completed, name="Tareas_completadas"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.detalle_tarea, name="detalle_tarea"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="tarea_completada"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="tarea_eliminada"),
    path("logout/", views.Salir, name="Salir"),
    path("signin/", views.Entrar, name="Entrar"),
]