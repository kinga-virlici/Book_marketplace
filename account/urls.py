from django.urls import path
from .views import LoginView, register
# in acest fisier definim rutele specifice acestei functionalitati

app_name = 'account' # in cadrul variabilei app_name salvam numele aplicatiei unde am definit url-urile specifice acesti functionaliati
                     # ne vom folosi de acest nume cand vom  gestiona url-urile in sabloanele(fisierele html)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    # aici vom adauga si alte rute specifice acestei functionalitati
]