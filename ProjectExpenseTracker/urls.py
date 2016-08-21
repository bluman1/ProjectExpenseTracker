"""ProjectExpenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from ExpenseTracker.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login),
    url(r'^signup/', signup),
    url(r'^newexpense/', create_new_expense),
    url(r'^dayexpense/', view_day_expense),
    url(r'^weekexpense/', view_week_expense),
    url(r'^monthexpense/', view_month_expense),
    url(r'^expensehistory/', view_expense_history),
    url(r'^about/', view_about),
    url(r'^profile/', view_profile)
]
