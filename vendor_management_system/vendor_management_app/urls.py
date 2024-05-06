"""
URL configuration for vendor_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import Vendors,VendorsDetail,Purchase_Orders,Update_Purchase_Order,Performance_History,Vendor_Acknowledgement,CreateUser

urlpatterns = [
    path('vendors/',Vendors.as_view(),name='vendors'),
    path('user/',CreateUser.as_view(),name='user'),
    path('vendors/<str:vendor_code>/',VendorsDetail.as_view(),name='vendordetail'),
    path('purchase_orders/',Purchase_Orders.as_view(),name = 'purchase_orders'),
    path('purchase_orders/<str:po_number>/',Update_Purchase_Order.as_view(),name = 'update_purchase_order'),
    path('vendors/<str:vendor_code>/performance/',Performance_History.as_view(),name='performance'),
    path('purchase_orders/<str:po_number>/acknowledge/',Vendor_Acknowledgement.as_view(),name='acknowledgement'),
]
