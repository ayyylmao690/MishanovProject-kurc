from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from django.forms.fields import CharField, ChoiceField, DateField, IntegerField
from django.forms.widgets import DateInput, Select
from .models import Visa, Country, Client, Calls
from django.core.validators import MinLengthValidator, RegexValidator

class VisaForm(ModelForm):
    class Meta:
        model = Visa
        fields = '__all__'
        labels = {
            'client_id': 'ФИО',
            'country_id': 'Страна пребывания',
            'type_id': 'Тип визы',
            'visa_number': 'Номер визы',
            'visa_serial': 'Серия визы',
            'start_date': 'Дата выдачи',
            'end_date': 'Действительна до',
            'price': 'Цена',
        }
        widgets = {
            'client_id': forms.Select(attrs={'class': 'form-control', 'id': 'resident-name', }),
            'country_id': forms.Select(attrs={'class': 'form-control', 'id': 'country-name', }),
            'type_id': forms.Select(attrs={'class': 'form-control'}),
            'visa_number': forms.TextInput(attrs={'class': 'form-control'}),
            'visa_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','min':'0.01'}),

        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'patronymic', 'address',
                  'email', 'pass_number', 'pass_serial', ]
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'address': 'Адрес проживания',
            'email': 'Адрес электронной почты',
            'pass_number': 'Номер пасспорта',
            'pass_serial': 'Серия пасспорта',
        }
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control field', 'placeholder': 'Мишанов', 'required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control field', 'placeholder': 'Иван', 'required': 'required'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control field', 'placeholder': 'Олегович', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control field', 'placeholder': 'Московская обл, ул. Пушкина, д. Колотушкина, д. 30 кв. 14', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control field', 'type': 'email', 'placeholder': 'youremail@email.com', 'required': 'required'}),
            'pass_number': forms.TextInput(attrs={'class': 'form-control field', 'required': 'required'}),
            'pass_serial': forms.TextInput(attrs={'class': 'form-control field', 'required': 'required'}),
        }


class CallForm(ModelForm):
    class Meta:
        model = Calls
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'contact_number':'Номер телефона'
        }
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван', 'required': 'required'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мишанов', 'required': 'required'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Олегович', 'required': 'required'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79506353088', 'required': 'required'}),
        }
        

class NumberForm(forms.Form):
    contact_numberRegex = RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
                                         message="Номер телефона введен в неверном формате! Пример: +79261234567, 89261234567, 79261234567, 123-45-67 и т.п.")
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control field', 'placeholder': '+79506353088', 'required': 'required'}), label="Номер телефона", max_length=13, validators=[contact_numberRegex])


class SearchContractForm(forms.Form):
    search = IntegerField(widget=forms.NumberInput(attrs={'class': 'enterPL-input', 'placeholder': 'Номер заказа', 'name':'get_contract_byId', 'style':'height:60px;', 'step':'1'}),min_value=0, label='')


class SearchForm(forms.Form):
    town = CharField(widget=forms.TextInput(attrs={
                     'class': 'form-control search-input', 'placeholder': 'Откуда летим', 'name': 'town'}))
    where = ModelChoiceField(queryset=Country.objects.all(), empty_label="Выбрать куда летим", widget=forms.Select(
        attrs={'class': 'form-control search-input', 'name': 'where'}))
    how_long = IntegerField(widget=forms.NumberInput(attrs={
                            'class': 'form-control search-input', 'step': '1', 'placeholder': 'Дней отдыха', 'name': 'how_long'}), min_value=0)
    when = DateField(widget=DateInput(format=(
        '%m/%d/%Y'), attrs={'class': 'form-control search-input', 'name': 'when', 'type': 'date'}))
    tourists = ChoiceField(choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')), widget=forms.Select(
        attrs={'class': 'form-control search-input', 'id': 'tourists', 'name': 'tourists'}))


class LoginForm(AuthenticationForm):
    username = CharField(label="Логин", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
