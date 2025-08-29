from django.db import models

# Create your models here.
class Admin(models.Model):
    """ Admin """
    username = models.CharField(verbose_name="username", max_length=32)
    password = models.CharField(verbose_name="password", max_length=64)

    def __str__(self):
        return self.username

class Department(models.Model):
    """ department table """
    title = models.CharField(verbose_name="Department Title", max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """ Employee Table """
    name = models.CharField(verbose_name="Employee Name", max_length=32)
    password = models.CharField(verbose_name="password", max_length=64)
    age = models.IntegerField(verbose_name="age")
    savings = models.DecimalField(verbose_name="savings", max_digits=10, decimal_places=2, default=0)

    create_time = models.DateField(verbose_name="create date")

    # depart_id = models.BigIntegerField(verbose_name="department ID")
    # depart = models.ForeignKey(to="Department", to_fields="id", on_delete=models.CASCADE)
    depart = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, "male"),
        (2, "female"),
    )
    gender = models.SmallIntegerField(verbose_name="gender", choices=gender_choices)

class PrettyNum(models.Model):
    """ Phone Number """
    mobile = models.CharField(verbose_name="phone", max_length=11)
    price = models.IntegerField(verbose_name="price", default=0)

    level_choices = (
        (1, "1 level"),
        (2, "2 level"),
        (3, "3 level"),
        (4, "4 level")
    )
    level = models.SmallIntegerField(verbose_name="level", choices=level_choices, default=1)

    status_choice = (
        (1, "use"),
        (2, "unused")
    )
    status = models.SmallIntegerField(verbose_name="status", choices=status_choice, default=2)

class Task(models.Model):
    """ Task """
    level_choice = (
        (1, "urgent"),
        (2, "normal"),
        (3, "temporary")
    )

    level = models.SmallIntegerField(verbose_name="level", choices=level_choice, default=1)
    title = models.CharField(verbose_name="title", max_length=32)
    details = models.TextField(verbose_name="details", max_length=64)
    assignee = models.ForeignKey(verbose_name="assignee", to="Admin", on_delete=models.CASCADE)

class Order(models.Model):
    """ Order """
    oid = models.CharField(verbose_name="oid", max_length=64)
    title = models.CharField(verbose_name="title", max_length=32)
    price = models.IntegerField(verbose_name="price")

    status_choice = (
        (1, "paid"),
        (2, "unpaid")
    )

    status = models.SmallIntegerField(verbose_name="status", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="admin", to="Admin", on_delete=models.CASCADE)

class Boss(models.Model):
    name = models.CharField(verbose_name="Employee Name", max_length=32)
    age = models.IntegerField(verbose_name="age")
    img = models.CharField(verbose_name="img", max_length=128)

class City(models.Model):
    name = models.CharField(verbose_name="name", max_length=32)
    population = models.IntegerField(verbose_name="population")
    # 本质也是charfield,django内部自动帮助保存数据
    logo = models.FileField(verbose_name="logo", max_length=128, upload_to='city/')