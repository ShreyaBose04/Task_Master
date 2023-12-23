from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Profile(models.Model):
#     user = models.OneToOneField(User)
#     auth_token = models.CharField(max_length=100)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


class ToDoList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todolist", null=True
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
