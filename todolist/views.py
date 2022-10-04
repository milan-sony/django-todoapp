from django.shortcuts import redirect, render
from django.contrib import messages
import todolist
from todolist.forms import todoform
from todolist.models import todolists

# Create your views here.

def userhome_todo(request):
  if request.user.is_authenticated:
    user = request.user
    todolist = todolists.objects.filter(user = user)
    return render(request, "userhomepage.html", {'todolist':todolist})

def addtodolist(request):
  if request.method == 'POST':
    todo = request.POST['todo']
    todolist = todolists(user=request.user, todo=todo)
    todolist.save()
    messages.warning(request, "Your list is added")
    return redirect('userhome_todo')
  else:
    messages.warning(request, "Something went wrong please try again")
    return redirect('userhome_todo')

def edit_todo(request, id):
  todolist = todolists.objects.get(id=id)
  if request.method == 'POST':
    newtodo = request.POST['newtodo']
    todolist.todo = newtodo
    todolist.save()
    messages.warning(request, "Todolist updated")
    return redirect('userhome_todo')
  else:
    return render(request, "edit_todolist.html",{'todolist':todolist}) 


def status_update(request, id):
  todolist = todolists.objects.get(id=id)
  current_status = todolist.todo_completed
  todolist.todo_completed = not current_status 
  todolist.save()
  messages.warning(request, "Status updated")
  return redirect('userhome_todo') 


def delete_todo(request, id):
  todolist = todolists.objects.get(id=id)
  if request.method == 'POST':
    todolist.delete()
    messages.warning(request, "Todolist deleted")
    return redirect('userhome_todo')
  else:
    return render(request, "confirm_delete.html",{'todolist':todolist}) 
