from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import login, logout, authenticate
from .forms import Taskform
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def Home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        print("Enviando formulario")
        return render(request, "signup.html",{
            "form": UserCreationForm
        })
    
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user=User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("Tasks")
            
            except:
                return render(request, "signup.html",{
                    "form": UserCreationForm,
                    "error":"El usuario ya fue ingresado"
        })
        else:
           return render(request, "signup.html",{
                    "form": UserCreationForm,
                    "error":"Las contraseñas no coinciden"
           })

@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, "Task/tasks.html",{
        "task":tasks
    })

@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull = False).order_by ("-datecompleted")
    return render(request, "Task/tasks.html",{
        "task":tasks
    })

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request,"Task/create_tasks.html", {
        "form":Taskform
        })
    else:
        try:
            form=Taskform(request.POST)
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect ("Tasks")
        except:
            return render(request,"Task/create_tasks.html", {
            "form":Taskform,
            "Error":"ERROR:Por favor ingrese bien los datos"
        })

@login_required
def detalle_tarea(request, task_id):
    if request.method == "GET":
        tasks=get_object_or_404(Task,pk=task_id, user=request.user)
        form=Taskform(instance=tasks)
        return render(request,"Task/task_detail.html",{
            "tarea":tasks,
            "form":form
        })
    
    else:
        try:
            print(request.POST)
            print(task_id)
            obj=get_object_or_404(Task,pk=task_id, user=request.user)
            obj2=Taskform(request.POST, instance=obj)
            obj2.save()
            return redirect("Tasks")
        except:
            return render(request,"Task/task_detail.html",{
                "error":"La tarea no se pudo actualizar"
        })

@login_required
def complete_task(request,task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect ("Tasks")

@login_required
def delete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect ("Tasks")

@login_required
def Salir(request):
    logout(request)
    return redirect("Home")

def Entrar(request):
    if request.method == "GET":
        return render(request, "signin.html",{
        "autentificacion": AuthenticationForm
        })
    else:
        user=authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "signin.html",{
            "autentificacion": AuthenticationForm,
            "error":"El usuario no a sido encontrado"
            })
        else:
            login(request, user)
            return redirect("Tasks")