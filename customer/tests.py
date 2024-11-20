from django.conf import settings

# from django.conf.wsgi import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# from .serializers import  DataComplementarySerializer

from django.template.loader import render_to_string

# from django.db import models
# from pathlib import Path

from .models import DataComplementary

# from customer import models

# 
# from django.conf.urls.static import static
# from django.conf import settings

# Create your tests here.
def send_email():
    try:
        # Establecemos conexion con el servidor smtp de gmail
        # mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)

        mailServer = smtplib.SMTP('smtp.office365.com', 587)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login('info@mx-interland.com', '=wAQ15&ix8')
        print('Conectado...')

        #construye el mensaje simple
        email_to='ismael.martinez@mx-mcl.com'

        
        mensaje = MIMEText("""Este es el mensaje""")
        mensaje['From']= 'info@mx-interland.com'
        mensaje['To']=email_to
        mensaje['Subject'] = "Solicitud de Credito"

        # render_to_string('send_email.html', {'solicitud': DataComplementary.objects.get(id=1)})
        content = render_to_string('send_email.html', {'DataComplementary': DataComplementary.objects.get(id=1)})
        mensaje.attach(MIMEText(content, 'html'))


        mailServer.sendmail('info@mx-interland.com',
                             email_to,
                             mensaje.as_string())

        print('Correo enviado')

    except Exception  as e:
        print(e)

send_email()


# class DataComplementaryViewSet(viewsets.ModelViewSet): #Agregado David 310521
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)
    # queryset = DataComplementary.objects.all()
    # serializer_class = DataComplementarySerializer


# DJANGO_SETTINGS_MODULE = 'inland_django.settings'
# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'info@mx-interland.com'
# EMAIL_HOST_PASSWORD = '=wAQ15&ix8'
