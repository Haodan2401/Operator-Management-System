from app01 import models
from django import forms
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="name")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "savings", "create_time", "gender", "depart"]



class PrettyAddModelForm(BootStrapModelForm):
    # mobile = forms.CharField(
    #     label="mobile",
    #     validators=[RegexValidator(r'^1[3-9]/d{9}$', 'Incorrect type for phone number')]
    #
    # )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("Phone number already exists!")

        if len(txt_mobile) != 11:
            raise ValidationError("Incorrect type for phone number")
        return txt_mobile

class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(
    #     label="mobile",
    #     validators=[RegexValidator(r'^1[3-9]/d{9}$', 'Incorrect type for phone number')]
    #
    # )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("Phone number already exists!")

        if len(txt_mobile) != 11:
            raise ValidationError("Incorrect type for phone number")
        return txt_mobile