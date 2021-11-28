from django.db import models
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MinLengthValidator, RegexValidator


class Country(models.Model):
    name = models.CharField(max_length=30)
    money = models.CharField(max_length=30)
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Client(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pass_and_serial = models.CharField(
        max_length=12, db_index=True, null=True, blank=True)
    pass_number = models.CharField(max_length=6, validators=[
                                   MinLengthValidator(6, 'Длина номера паспорта 6 цифр')])
    pass_serial = models.CharField(max_length=4, validators=[
                                   MinLengthValidator(4, 'Длина серии паспорта 4 цифры')])

    def __str__(self):
        return "%s | %s %s %s, %s %s" % (
            self.id, self.surname, self.name, self.patronymic, self.pass_number, self.pass_serial
        )


class GroupClient(models.Model):
    client = models.ManyToManyField(Client, blank=True)


class Hotel(models.Model):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    wi_fi = models.CharField(
        choices=(('1', '1'), ('0', '0')), default=0, max_length=30)
    beach = models.CharField(
        choices=(('1', '1'), ('0', '0')), default=0, max_length=30)
    air_conditioning = models.CharField(
        choices=(('1', '1'), ('0', '0')), default=0, max_length=30)
    child = models.CharField(
        choices=(('1', '1'), ('0', '0')), default=0, max_length=30)
    bar = models.CharField(
        choices=(('1', '1'), ('0', '0')), default=0, max_length=30)
    desc = models.TextField(max_length=200)

    def __str__(self):
        return "%s | %s" % (
            self.id, self.name
        )


class VisaType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Visa(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    type_id = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    visa_number = models.CharField(max_length=10)
    visa_serial = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=18, decimal_places=2)


class Contract(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    group_id = models.ForeignKey(
        GroupClient, on_delete=models.CASCADE, blank=True, null=True)
    sell_date = models.DateField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    contact_numberRegex = RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
                                         message="Номер телефона введен в неверном формате! Пример: +79261234567, 89261234567, 79261234567, 123-45-67 и т.п.")
    contact_number = models.CharField(
        max_length=13, validators=[contact_numberRegex])


class Calls(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    contact_numberRegex = RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
                                         message="Номер телефона введен в неверном формате! Пример: +79261234567, 89261234567, 79261234567, 123-45-67 и т.п.")
    contact_number = models.CharField(
        validators=[contact_numberRegex], max_length=13, blank=True)


def pre_save_client_receiver(sender, instance, *args, **kwargs):
    pass_serial = instance.pass_serial
    pass_number = instance.pass_number
    pass_and_serial = "%s-%s" % (pass_serial, pass_number)

    instance.pass_and_serial = pass_and_serial


pre_save.connect(pre_save_client_receiver, sender=Client)
# Create your models here.
