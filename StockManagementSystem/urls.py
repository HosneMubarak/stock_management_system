"""StockManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from stockmgmnt.views import home, list_items, add_items, update_items, delete_items, stock_details, issue_items, \
    receive_item, reorder_level_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', home, name='home'),
                  path('list_items/', list_items, name='list-items'),
                  path('add_items/', add_items, name='add-items'),
                  path('update_items/<str:pk>', update_items, name='update-items'),
                  path('delete_items/<str:pk>', delete_items, name='delete-items'),
                  path('stock_detail/<str:pk>', stock_details, name='stock-detail'),
                  path('issue_item/<str:pk>', issue_items, name='issue-item'),
                  path('receive_item/<str:pk>', receive_item, name='receive-item'),
                  path('reorder_level/<str:pk>', reorder_level_view, name='reorder-level'),

                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
