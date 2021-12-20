from typing import List
from django import http
from django.forms.formsets import formset_factory
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views import View
from django.views.generic import ListView, DetailView
from .base import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class ClietsPage(LoginRequiredMixin, ListView):
    model=Client
    template_name = 'clients.html'
    context_object_name='clients'


class SearchResPage(ListView):
    model = Hotel
    template_name = 'search_page.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        if self.request.GET['sort'] == "cheap":
            return Hotel.objects.filter(country_id__id=self.request.GET['where']).order_by('price')
        elif self.request.GET['sort'] == "notcheap":
            return Hotel.objects.filter(country_id__id=self.request.GET['where']).order_by('-price')
        else:
            return HttpResponseRedirect('/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['town_from'] = self.request.GET['town']
        context['days'] = self.request.GET['how_long']
        context['when'] = self.request.GET['when']
        context['where']=self.request.GET['where']
        context['tourists'] = self.request.GET['tourists']
        context['call_form']=CallForm()
        return context


class MainPage(View):
    def get(self, request):
        searchform = SearchForm()
        call_form = CallForm()
        contract_form=SearchContractForm()
        context = {
                   'search_form': searchform,
                   'call_form': call_form,
                   'contract_search_form':contract_form
                   }
        return render(request, "index.html", context=context)


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


class CallsView(LoginRequiredMixin, ListView):
    redirect_field_name = None
    model = Calls
    template_name = 'call_request.html'
    context_object_name = 'call_requests'


class Agent(LoginRequiredMixin, ListView):
    redirect_field_name = None
    model = Contract
    template_name = 'agent.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        if self.request.GET.get('id_client'):
            clientId=self.request.GET.get('id_client')
            if GroupClient.objects.filter(client=clientId):
                groups = GroupClient.objects.filter(client=clientId)
                contracts=Contract.objects.filter(group_id=[group.id for group in groups])
                return contracts
            elif Contract.objects.filter(client_id=clientId).exists():
                return Contract.objects.filter(client_id=self.request.GET.get('id_client'))
            else:
               messages.error(self.request, 'Связанные заказы не найдены')
               return Contract.objects.all()
        else:
            return Contract.objects.all()


class FullContract(LoginRequiredMixin, View):
    redirect_field_name = None

    def get(self, request, id):
        contract = get_full_contract(id)
        context = {'full_contract': contract,
                   }
        return render(request, 'full_contract.html', context=context)


class ClientInfo(LoginRequiredMixin, View):
    redirect_field_name = None

    def get(self, request, id):

        client = get_client_info(id)

        form = VisaForm()
        visas = get_client_visas(id)
        typesV = get_visas_types()
        boolVisa = Visa.objects.filter(client_id=client).exists()

        context = {
            'visas': visas,
            'visas_type': typesV,
            'visaExists': boolVisa,
            'visaForm': form,
            'client': client,
        }

        return render(request, "client_info.html", context=context)

    def post(self, request, contract_id, id):
        visa = VisaForm(request.POST or None)
        if visa.is_valid():
            obj_visa = visa.save()
            visa = VisaForm()
            return HttpResponseRedirect(f'/agent/contract/{contract_id}')
        client = get_client_info(id)
        contract = get_full_contract(contract_id)

        form = VisaForm()
        visas = get_client_visas(id)
        typesV = get_visas_types()
        boolVisa = Visa.objects.filter(client_id=client).exists()
        context = {
            'contract': contract,
            'visas': visas,
            'visas_type': typesV,
            'visaExists': boolVisa,
            'visaForm': visa,
            'client': client,
        }
        return render(request, 'client_info.html', context=context)

def get_ClientContract_info(request):
    id = request.GET['search']
    print(id)
    contract = Contract.objects.filter(id=id)
    searchform = SearchForm()
    call_form = CallForm()
    contract_form=SearchContractForm(request.GET)
    if contract.exists():
        context = {
            'search_form': searchform,
            'call_form': call_form,
            'contract_search_form':contract_form,
            'contract':contract.first(),
            'boolModal':1
            }
        return render(request, 'index.html', context=context)
    messages.error(request, 'Заказ не найден')
    return HttpResponseRedirect('/')
        
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def makeorder(request, id):
    search_form = SearchForm(request.GET)
    client_form = formset_factory(
        ClientForm, extra=int(request.GET['tourists']))

    hotel = get_hotel_byId(id)
    call_form = CallForm()
    context = {'hotel': hotel,
                'search_form': search_form,
                'call_form':call_form
                }
    client_ids_arr = []

    if request.method == "POST":
        formset = client_form(request.POST)
        contact_number = NumberForm(request.POST)
        if(formset.is_valid() and contact_number.is_valid()):  # Валидация форм
            for form in formset:  # Перебор форм в формсете
                # Проверка туриста на наличие в базе данных
                pass_ind_form = "%s-%s" % (
                    form.cleaned_data['pass_serial'], form.cleaned_data['pass_number'])
                if Client.objects.filter(pass_and_serial=pass_ind_form).exists() == False:
                    obj_form = form.save()  # Сохранение данных в форме
                    client_ids_arr.append(obj_form.id)
                else:
                    client = Client.objects.get(pass_and_serial=pass_ind_form)
                    client_ids_arr.append(client.id)

            # Если туристов больше одного, они обьединяются в группу
            if (int(request.GET['tourists']) > 1):
                create_group = GroupClient()  # Создание группы
                create_group.save()

                group = create_group

                for client_id in client_ids_arr:  # Запись всех клиентов в группу
                    client = Client.objects.get(id=client_id)
                    group.client.add(client)

                main_client = Client.objects.get(
                    id=client_ids_arr[0])  # Создание контракта
                create_contract = Contract(client_id=main_client, hotel_id=hotel, group_id=group,
                                           start_date=datetime.strptime(
                                               request.GET['when'], '%Y-%m-%d'),
                                           end_date=(datetime.strptime(request.GET['when'], '%Y-%m-%d')+timedelta(days=int(request.GET['how_long']))), contact_number=request.POST.get('contact_number'))
                create_contract.save()

            else:  # Если турист один, то создается контракт без группы
                client = client = Client.objects.get(id=client_ids_arr[0])
                create_contract = Contract(client_id=client, hotel_id=hotel,
                                           start_date=datetime.strptime(
                                               request.GET['when'], '%Y-%m-%d'),
                                           end_date=(datetime.strptime(request.GET['when'], '%Y-%m-%d')+timedelta(days=int(request.GET['how_long']))), contact_number=request.POST.get('contact_number'))
                create_contract.save()
            messages.success(request, f'Ваш заказ сформирован, номер заказа: {create_contract.id}')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'В форме были допущены ошибки!')
            context['formset']=formset
            context['contact_number']=contact_number
            return render(request, "make_order.html", context=context)

    context['formset']=client_form
    context['contact_number']=NumberForm()
    return render(request, "make_order.html", context=context)

def add_call(request):
    searchform = SearchForm()
    call_form = CallForm()

    context = {
               'search_form': searchform,
               'call_form': call_form,
               }

    if request.method == "POST":
        call = CallForm(request.POST or None)
        if call.is_valid():
            obj_call = call.save()
            messages.success(request, 'Звонок успешно зарегистрирован')
            return HttpResponseRedirect(reverse('MainPage'))
        else:
            messages.error(request, 'Есть ошибки в заполнении формы')
            context = {
                       'search_form': searchform,
                       'call_form': call,
                       }
    return render(request, "index.html", context=context)


@login_required
def edit_visa(request, contract_id, client_id, id):
    obj = get_visa_byId(id)
    if request.method == "POST":
        visa = VisaForm(request.POST or None, instance=obj)
        context = {'form': visa}
        if visa.is_valid():
            obj_visa = visa.save(commit=False)
            obj_visa.save()
            return HttpResponseRedirect(f'/agent/contract/{contract_id}/client/{client_id}/')
    visa_form = VisaForm(instance=obj)
    context = {'form': visa_form}
    return render(request, 'edit_visa.html', context=context)


@login_required
def delete_contract(request, id):
    instance = get_full_contract(id)
    if instance.group_id != None:
        GroupClient.objects.filter(id=instance.group_id.id).delete()
    instance.delete()
    return HttpResponseRedirect('/agent')


@login_required
def delete_visa(request, contract_id, client_id, id):
    visa = get_visa_byId(id)
    visa.delete()
    return HttpResponseRedirect(f'/agent/contract/{contract_id}/client/{client_id}/')

@login_required
def delete_call(request, id):
    call = get_call_byId(id)
    call.delete()
    return HttpResponseRedirect('/agent/calls')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
# Create your views here.
