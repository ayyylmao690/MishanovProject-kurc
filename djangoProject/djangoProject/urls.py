"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, re_path
from djangoApp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name="MainPage"),
    path('search-results/', SearchResPage.as_view(), name='search_res'),
    path('login/', LoginUser.as_view(), name='login'),
    path('agent/', Agent.as_view()),
    path('agent/calls/', CallsView.as_view(), name = "calls"),
    path('agent/contract/<int:id>/', FullContract.as_view(), name='get_full_contract'),
    path('agent/contract/<int:contract_id>/client/<int:id>/', ClientInfo.as_view(), name='get_client_info'),

    path('make-order/<int:id>/', makeorder, name = "make_order"),
    path('getCall/', add_call, name='add_call'),
    path('agent/calls/delete-call/<int:id>/', delete_call, name = "delete_call"),
    path('user/', get_ClientContract_info, name="get_ClientContract_info"),
    path('agent/contract/<int:contract_id>/client/<int:client_id>/delete-visa/<int:id>', delete_visa, name = "delete_visa"),
    path('agent/contract/<int:contract_id>/client/<int:client_id>/edit-visa/<int:id>', edit_visa, name = "edit_visa"),
    
    path('logout/', logout_user, name='logout'),
]
