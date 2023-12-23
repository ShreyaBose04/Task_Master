from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, item
from .forms import CreateNewList
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url="/login")
def index(request, id):
    ls = ToDoList.objects.get(id=id)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("save"):
            for item in ls.item_set.all():
                if request.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif request.POST.get("addItem"):
            text = request.POST.get("newItem")
            if len(text) > 2:
                ls.item_set.create(text=text, complete=False)
            else:
                print("invalid input")

    return render(request, "main/list.html", {"ls": ls})


@login_required(login_url="/login")
def home(request):
    return render(request, "main/home.html", {})


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)

        return HttpResponseRedirect("/%i" % t.id)

    else:
        form = CreateNewList()
        return render(request, "main/create.html", {"form": form})


@login_required(login_url="/login")
def view(request):
    return render(request, "main/view.html", {})
