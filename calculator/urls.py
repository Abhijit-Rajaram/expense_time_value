from django.urls import path, include
from calculator.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', home, name='home'),
    path('expense/', expense_form, name='expense_form'),  # URL for expense form
    path('add-month/', add_month, name='add_month'),  # URL for adding a new month
]

urlpatterns += static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)
