from .models import *

def get_clients():
    clients = Client.objects.all()
    return clients

def get_client_info(id):
    client = Client.objects.get(id = id)
    return client

def get_contracts():
    contracts = Contract.objects.all()
    return contracts

def get_client_visas(id):
    visas = Visa.objects.filter(client_id = id)
    return visas

def get_visas_types(): 
    typesV = VisaType.objects.all()
    return typesV

def get_full_contract(id):
    contract = Contract.objects.filter(id=id).first()
    return contract

def get_hotel_byId(id):
    hotel = Hotel.objects.filter(id=id).first()
    return hotel

def get_visa_byId(id):
    visa = Visa.objects.filter(id=id).first()
    return visa

def get_calls():
    calls = Calls.objects.all()
    return calls

def  get_call_byId(id):
    call = Calls.objects.get(id=id)
    return call