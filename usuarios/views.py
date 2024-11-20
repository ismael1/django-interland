import base64
from calendar import timegm
from datetime import datetime, date
import os
from django.core.files.storage import default_storage

import smtplib
from smtplib import SMTPException, SMTPSenderRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.conf import settings

from django.shortcuts import render
import jwt
from rest_framework import serializers, viewsets
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import json

# from rest_framework_api_key.permissions import HasAPIKey
from django.db.models.query_utils import Q
from django.db.models import Count

from .models import Usuarios
from .serializers import UsuariosSerializer

from django.contrib.auth import get_user_model, user_logged_in

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from rest_framework_simplejwt import compat
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from catalogos.models import Permisos, Modulos


from django.contrib.auth.models import update_last_login

from rest_framework import status

from administracion.models import EmailDatos
from administracion.serializers import EmailDatosSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

@csrf_exempt
@api_view(['GET'])
def ListUsuarios(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Usuarios.objects.filter(Q(estatus=1))[data_start:data_end]
            count = Usuarios.objects.filter(Q(estatus=1)).count()
        else:
            goodslist = Usuarios.objects.filter(Q(nombre__icontains=palabra) | Q(apellidos__icontains=palabra)).filter(Q(estatus=1))[data_start:data_end]
            count = Usuarios.objects.filter(Q(nombre__icontains=palabra) | Q(apellidos__icontains=palabra)).filter(Q(estatus=1))[data_start:data_end].count()
        goods_ser=UsuariosSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt 
@api_view(['POST'])
def ValidaUsuario(request):

    ape = request.data.get('apellidos')
    nom = request.data.get('nombre')
    logi = request.data.get('login')
    pss = request.data.get('pass')
    mail = request.data.get('email')
    
    # fecha_hoy= 2021-07-13
    # select * from servicos_venata  where fecha_vigencia >  fecha_hoy

    # __lte Se utiliza para fechas -> equivalente a fechaFin <= fecha hoy
    # __gte Se utiliza para fechas -> equivalente a fechaFin >= fecha hoy

    if (ape == Usuarios.apellidos | nom == Usuarios.nombre):
        # relacionar = ServicioVenta.objects.filter(paisOrigen=paisOri).filter(estadoOrigen=estadoOri).filter(ciudadOrigen=ciudadOri).filter(paisDestino=paisDes).filter(estadoDestino=estadoDes).filter(ciudadDestino=ciudadDes).filter(unidaModality=tipoCarga).filter(tipoUnidad_id=tipoUnidad).filter(dateFin__gte=fechaFin).filter(checkVentas="SI").order_by('-id')[:3]
        # relacionar = Usuarios.objects.filter(apellidos=ape).filter(nombre=nom).filter(login=logi).filter(password=pss).filter(email=mail).count()
        relacionar = Usuarios.objects.filter(apellidos=ape).filter(nombre=nom)
        count = Usuarios.objects.filter(apellidos=ape).filter(nombre=nom).count()
        red = str(relacionar.query)
        # serializer = UsuariosSerializer(relacionar, many=True)
        return Response({
            'total':count,
        })
    else:
        count = Usuarios.objects.filter(Q(login=logi) | Q(password=pss) | Q(email=mail)).count()
        return Response({
            'total': count,
        })

@csrf_exempt 
@api_view(['POST'])
def ValidUser(request):

    email = request.data.get('email')
    passw = request.data.get('password')

    if email :
        relacionar = Usuarios.objects.filter(email=email).filter(password=passw)
        serializer = UsuariosSerializer(relacionar, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class UserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
##LOGIN

def jwt_payload_handler(user):
    """
    Custom payload handler 
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """

    ACCESS_TOKEN_LIFETIME = api_settings.ACCESS_TOKEN_LIFETIME
    return {
        'user_id': user.id,
        'email': user.login,
        'is_superuser': user.administrador,
        'exp': datetime.utcnow() + api_settings.ACCESS_TOKEN_LIFETIME,
        'orig_iat': timegm(datetime.utcnow().utctimetuple())
    }

@api_view(['POST','GET'])
def authenticate_user(request):

    permission_classes = [IsAuthenticated]
    
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        datosPer = []

        if auth_header is None:
            res = {'estatus': False, 'detail':'Falta el encabezado de autorización', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        try:
            auth_type, auth_string = auth_header.split(' ')
        except ValueError:
            res = {'estatus': False, 'detail':'Encabezado de autorización mal formateado', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        if auth_type != 'Basic':
            res = {'estatus': False, 'detail':'Tipo de token de autorización no válido', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        try:
            decoded_auth_string = base64.b64decode(auth_string).decode()
        except Exception as e:
            res = {'estatus': False, 'detail':'Credenciales mal codificadas', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_428_PRECONDITION_REQUIRED}
            return Response(res)
        
        username, password = decoded_auth_string.split(':')

        valuser = Usuarios.objects.filter(login=str(username), password=str(password))

        if valuser.exists():
            try:
                user = Usuarios.objects.get(login=str(username), password=str(password))#DATOS DEL USUARIO
                permisos = Permisos.objects.filter(idUsuario_id=user.id).select_related('idModulo').values('idModulo__id','idModulo__nombre','idModulo__estatus','idModulo__isSubmenu','idModulo__link','idModulo__idMenu','idModulo__icon','lectura','agregar','eliminar','editar','usuarioAsigna').order_by('idModulo__nombre')
                for permiso in permisos:
                    datosPer.append({
                        "modulos_id":permiso['idModulo__id'],
                        "modulos_nombre":permiso['idModulo__nombre'],
                        "modulos_estatus":permiso['idModulo__estatus'],
                        "modulos_isSubmenu":permiso['idModulo__isSubmenu'],
                        "modulos_icon":permiso['idModulo__icon'],
                        "modulos_idMenu":permiso['idModulo__idMenu'],
                        "modulos_link":permiso['idModulo__link'],
                        "permisos_lectura":permiso['lectura'],
                        "permisos_agregar":permiso['agregar'],
                        "permisos_eliminar":permiso['eliminar'],
                        "permisos_editar":permiso['editar'],
                        "permisos_usuarioAsigna":permiso['usuarioAsigna'],
                    })
                
                payload = jwt_payload_handler(user)
                
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (user.nombre, user.apellidos)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                res = {'estatus': True, 'detail':'Usuario Valido', 'token':token, 'user':'valid', 'nameuser':"%s %s" % (user.nombre, user.apellidos), 'email':user.email , 'usuario':user.login , 'id':user.id , 'puesto':user.puesto_funcion,  'admin':user.administrador, 'urlImg':user.urlImg, 'permisos':datosPer, 'statusHttp':status.HTTP_200_OK}
                return Response(res)
            except Exception as e:
                #raise e
                res = {'estatus': False, 'detail':'Su correo y/o contraseña no coinciden con un usuario existente, verifiquelos por favor.', 'token':'', 'user':'valid', 'nameuser':"", 'email':"" , 'usuario':'' , 'id':'' , 'puesto':'', 'statusHttp':status.HTTP_200_OK}
                raise Response(res)
        else:
            res = {'estatus': False, 'detail':'Su correo y/o contraseña no coinciden con un usuario existente, verifiquelos por favor.', 'token':'', 'user':'valid', 'nameuser':"", 'email':"" , 'usuario':'' , 'id':0 , 'puesto':'', 'statusHttp':status.HTTP_200_OK}
            return Response(res)
    except KeyError:
        res = {'estatus': False, 'detail':'Ocurrio un error inesperado, avise a sistemas!', 'token':'', 'user':'invalid', 'statusHttp':status.HTTP_403_FORBIDDEN}
        return Response(res)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)

@csrf_exempt 
@api_view(['POST'])
def validarUsuario(request):

    user = request.data.get('username')

    usuario = Usuarios.objects.filter(login=user)
        
    if usuario.count() > 0:
        resp = [{"validate": False, "msg": "Usuario Ocupado",}]
    else:
        resp = [{"validate": True, "msg": "Usuario Valido",}]
    
    
    return Response(resp)
    
@csrf_exempt 
@api_view(['GET','POST'])
def registraUsuario(request):

    protocol = request.META['wsgi.url_scheme']+'://'
    host = request.META['HTTP_HOST']+'/'

    if request.method == 'POST':
        datos = request.data

        
        apellidos = request.data.get('lastname')
        nombre = request.data.get('name')
        login = request.data.get('username')
        password = request.data.get('pass')
        movil = request.data.get('phone')
        email = request.data.get('email')
        estatus = 1
        terminos_condiciones = bool(request.data.get('terms'))
        calle_fiscal = request.data.get('calle_fiscal')
        ciudad_fiscal = request.data.get('ciudad_fiscal')
        cp_fiscal = request.data.get('cp_fiscal')
        estado_fiscal = request.data.get('estado_fiscal')

        nom_fiscal = ''
        ext_fiscal = ''

        nom_cuenta = ''
        ext_cuenta = ''

        nombre_estado_cuenta = ''
        nombre_comprobante_domicilio_fiscal = ''

        comprobante_domicilio_fiscal = request.data.get('comprobante_domicilio_fiscal')

        if comprobante_domicilio_fiscal != 'null':
            nom_fiscal, ext_fiscal = os.path.splitext(comprobante_domicilio_fiscal.name)
            nombre_comprobante_domicilio_fiscal = nom_fiscal+'_cd'+ext_fiscal

            print(nombre_comprobante_domicilio_fiscal)

        estado_cuenta = request.data.get('estado_cuenta')
        if estado_cuenta != 'null':
            nom_cuenta, ext_cuenta = os.path.splitext(estado_cuenta.name)
            nombre_estado_cuenta = nom_cuenta+'_ec'+ext_cuenta
            print(nombre_estado_cuenta)

        

        forma_pago = request.data.get('forma_pago')
        metodo_pago = request.data.get('metodo_pago')
        nombre_empresa = request.data.get('nombre_empresa')
        numero_exterior_fiscal = request.data.get('numero_exterior_fiscal')
        numero_interior_fiscal = request.data.get('numero_interior_fiscal')
        pais_fiscal = request.data.get('pais_fiscal')
        regimen_fiscal = request.data.get('regimen_fiscal')
        rfc = request.data.get('rfc')
        tipo_cliente = request.data.get('tipo_cliente')
        tipo_empresa = request.data.get('tipo_empresa')
        tipo_persona = request.data.get('tipo_persona')

        if pais_fiscal == 'Mexico':
            pais_fiscal = 2
        else:
            pais_fiscal = 1
        
        create = Usuarios.objects.create(apellidos=apellidos, 
                                 nombre=nombre,
                                 login=login,
                                 password=password,
                                 administrador=False,
                                 movil=movil,
                                 email=email,
                                 terminos_condiciones=terminos_condiciones,
                                 dateCreate=datetime.now(),
                                 estatus=estatus,
                                 calle_fiscal=calle_fiscal,
                                 ciudad_fiscal=ciudad_fiscal,
                                 comprobante_domicilio_fiscal = nombre_comprobante_domicilio_fiscal,
                                 cp_fiscal=cp_fiscal,
                                 estado_fiscal=estado_fiscal,
                                 estado_cuenta = nombre_estado_cuenta,
                                 forma_pago = forma_pago,
                                 metodo_pago = metodo_pago,
                                 nombre_empresa = nombre_empresa,
                                 numero_exterior_fiscal = numero_exterior_fiscal,
                                 numero_interior_fiscal = numero_interior_fiscal,
                                 pais_fiscal = pais_fiscal,
                                 regimen_fiscal = regimen_fiscal,
                                 rfc = rfc,
                                 tipo_cliente = tipo_cliente,
                                 tipo_empresa = tipo_empresa,
                                 tipo_persona = tipo_persona,
                                 )

        usuario = Usuarios.objects.filter(apellidos=apellidos).filter(nombre=nombre).filter(login=login).filter(password=password).filter(movil=movil).filter(email=email)
        usr = UsuariosSerializer(usuario, many=True)

        idUsr = int(usr.data[0]['id'])

        carpeta = "media/docs/"+str(idUsr)

        if not os.path.exists(carpeta):
            # Si no existe, crear la carpeta
            os.makedirs(carpeta)

        if comprobante_domicilio_fiscal != 'null':
            default_storage.save(os.path.join(settings.MEDIA_ROOT+'/docs/'+str(idUsr)+'/', nombre_comprobante_domicilio_fiscal), comprobante_domicilio_fiscal)

        if estado_cuenta != 'null':
            default_storage.save(os.path.join(settings.MEDIA_ROOT+'/docs/'+str(idUsr)+'/', nombre_estado_cuenta), estado_cuenta)
        
        Permisos.objects.create(usuarioAsigna='sys', idModulo_id = 31, idUsuario_id = idUsr, lectura=1, pdf=1, editar=1)

        pkC = idUsr
        email = email
        nombre_contacto = nombre + ' ' + apellidos
        
        emailD = EmailDatos.objects.filter(idEmail=1)
        emailS = EmailDatosSerializer(emailD, many=True)

        correoInt = emailS.data[0]['correo']
        contraInt = emailS.data[0]['contra']
        hostInter = emailS.data[0]['host']
        puerInter = emailS.data[0]['port']

        mensaje = MIMEMultipart()

        mailServer = smtplib.SMTP(hostInter, puerInter)
            
        mailServer.starttls()

        mailServer.login(correoInt, contraInt)
        email_to=email

        mensaje['From']= correoInt
        mensaje['To']=email_to
        mensaje['Subject'] = "Interland | Avisos"

        content = render_to_string('mail/registro.html', {'name': nombre_contacto, "email":email, "usuario":login, "pass": password, "telefono": movil})
        mensaje.attach(MIMEText(content,'html'))

        mailServer.sendmail(correoInt, email_to, mensaje.as_string())

        resp = True

        mailServer.quit()

        resp = [{"validate": True, "msg": "Usuario Generado Correctamente, en breve recibiras un correo electrónico con los datos necesarios para iniciar sesión.",}]
    else:
        resp = [{"validate": False, "msg": "Ocurrio un error al dar de alta al Usuario.",}]
    
    return Response(resp)

@csrf_exempt 
@api_view(['POST', 'GET'])
def getUsuarios(request, pk):

    user = Usuarios.objects.get(id=pk)
    serializer = UsuariosSerializer(user)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def editarUsuario(request):

    protocol = request.META['wsgi.url_scheme']+'://'
    host = request.META['HTTP_HOST']+'/'

    if request.method == 'POST':
        datos = request.POST

        es_cadena_ec = False
        es_cadena_cd = False

        id = int(datos.get('id'))
        apellidos = datos.get('lastname')
        nombre = datos.get('name')
        password = datos.get('pass')
        movil = datos.get('phone')
        email = datos.get('email')
        calle_fiscal = datos.get('calle_fiscal')
        ciudad_fiscal = datos.get('ciudad_fiscal')
        cp_fiscal = datos.get('cp_fiscal')
        estado_fiscal = datos.get('estado_fiscal')

        nom_fiscal = ''
        ext_fiscal = ''

        nom_cuenta = ''
        ext_cuenta = ''

        nombre_estado_cuenta = ''
        nombre_comprobante_domicilio_fiscal = ''

        comprobante_domicilio_fiscal = request.data.get('comprobante_domicilio_fiscal')
        if comprobante_domicilio_fiscal != 'null':
            es_cadena_cd = isinstance(comprobante_domicilio_fiscal, str)
            
            if es_cadena_cd is False:
                nom_fiscal, ext_fiscal = os.path.splitext(comprobante_domicilio_fiscal.name)
                nombre_comprobante_domicilio_fiscal = nom_fiscal+'_cd'+ext_fiscal
            else:
                nombre_comprobante_domicilio_fiscal = comprobante_domicilio_fiscal

        estado_cuenta = request.data.get('estado_cuenta')
        if estado_cuenta != 'null':
            es_cadena_ec = isinstance(estado_cuenta, str)

            if es_cadena_ec is False:
                
                nom_cuenta, ext_cuenta = os.path.splitext(estado_cuenta.name)
                nombre_estado_cuenta = nom_cuenta+'_ec'+ext_cuenta
                
            else:
                nombre_estado_cuenta = estado_cuenta


        forma_pago = int(datos.get('forma_pago'))
        metodo_pago = int(datos.get('metodo_pago'))
        nombre_empresa = datos.get('nombre_empresa')
        numero_exterior_fiscal = datos.get('numero_exterior_fiscal')
        numero_interior_fiscal = datos.get('numero_interior_fiscal')
        pais_fiscal = datos.get('pais_fiscal')
        regimen_fiscal = datos.get('regimen_fiscal')
        rfc = datos.get('rfc')
        tipo_cliente = datos.get('tipo_cliente')
        tipo_cliente = tipo_cliente
        tipo_empresa = datos.get('tipo_empresa')
        tipo_empresa = tipo_empresa
        tipo_persona = datos.get('tipo_persona')
        tipo_persona = tipo_persona

        #Usuarios.objects.filter(id = id).update()

        usr = Usuarios.objects.get(id=id)
                
        usr.nombre=nombre
        usr.apellidos=apellidos
        usr.password=password
        usr.movil=movil
        usr.email=email
        usr.calle_fiscal=calle_fiscal
        usr.ciudad_fiscal=ciudad_fiscal
        usr.comprobante_domicilio_fiscal = nombre_comprobante_domicilio_fiscal
        usr.cp_fiscal=cp_fiscal
        usr.estado_fiscal=estado_fiscal
        usr.estado_cuenta = nombre_estado_cuenta
        usr.forma_pago = forma_pago
        usr.metodo_pago = metodo_pago
        usr.nombre_empresa = nombre_empresa
        usr.numero_exterior_fiscal = numero_exterior_fiscal
        usr.numero_interior_fiscal = numero_interior_fiscal
        usr.pais_fiscal = pais_fiscal
        usr.regimen_fiscal = regimen_fiscal
        usr.rfc = rfc
        usr.tipo_cliente = tipo_cliente
        usr.tipo_empresa = tipo_empresa
        usr.tipo_persona = tipo_persona

        usr.save()


        carpeta = "media/docs/"+str(id)

        if not os.path.exists(carpeta):
            # Si no existe, crear la carpeta
            os.makedirs(carpeta)

        if comprobante_domicilio_fiscal != 'null':
            if es_cadena_cd is False:

                for nombre_archivo in os.listdir(carpeta):
                    # Verifica si el archivo es un archivo PDF y si su nombre termina con "_cd"
                    if nombre_archivo.lower().endswith("_cd.pdf"):
                        # Crea la ruta completa al archivo
                        ruta_completa = os.path.join(carpeta, nombre_archivo)

                        # Elimina el archivo
                        os.remove(ruta_completa)
                        print(f"Archivo eliminado: {nombre_archivo}")

                default_storage.save(os.path.join(settings.MEDIA_ROOT+'/docs/'+str(id)+'/', nombre_comprobante_domicilio_fiscal), comprobante_domicilio_fiscal)

        if estado_cuenta != 'null':
            if es_cadena_ec is False:

                for nombre_archivo in os.listdir(carpeta):
                    # Verifica si el archivo es un archivo PDF y si su nombre termina con "_cd"
                    if nombre_archivo.lower().endswith("_ec.pdf"):
                        # Crea la ruta completa al archivo
                        ruta_completa = os.path.join(carpeta, nombre_archivo)

                        # Elimina el archivo
                        os.remove(ruta_completa)
                        print(f"Archivo eliminado: {nombre_archivo}")

                default_storage.save(os.path.join(settings.MEDIA_ROOT+'/docs/'+str(id)+'/', nombre_estado_cuenta), estado_cuenta)

        
        '''usuario = Usuarios.objects.filter(apellidos=apellidos).filter(nombre=nombre).filter(login=login).filter(password=password).filter(movil=movil).filter(email=email)
        usr = UsuariosSerializer(usuario, many=True)

        idUsr = int(usr.data[0]['id'])

        

        '''
        
        '''Permisos.objects.create(usuarioAsigna='sys', idModulo_id = 31, idUsuario_id = idUsr, lectura=1, pdf=1, editar=1)

        pkC = idUsr
        email = email
        nombre_contacto = nombre + ' ' + apellidos
        
        emailD = EmailDatos.objects.filter(idEmail=1)
        emailS = EmailDatosSerializer(emailD, many=True)

        correoInt = emailS.data[0]['correo']
        contraInt = emailS.data[0]['contra']
        hostInter = emailS.data[0]['host']
        puerInter = emailS.data[0]['port']

        mensaje = MIMEMultipart()

        mailServer = smtplib.SMTP(hostInter, puerInter)
            
        mailServer.starttls()

        mailServer.login(correoInt, contraInt)
        email_to=email

        mensaje['From']= correoInt
        mensaje['To']=email_to
        mensaje['Subject'] = "Interland | Avisos"

        content = render_to_string('mail/registro.html', {'name': nombre_contacto, "email":email, "usuario":login, "pass": password, "telefono": movil})
        mensaje.attach(MIMEText(content,'html'))

        mailServer.sendmail(correoInt, email_to, mensaje.as_string())

        resp = True

        mailServer.quit()'''

        resp = [{"validate": True, "msg": "Usuario Generado Correctamente, en breve recibiras un correo electrónico con los datos necesarios para iniciar sesión.",}]
    else:
        resp = [{"validate": False, "msg": "Ocurrio un error al dar de alta al Usuario.",}]
    
    return Response(resp)

@api_view(['POST','GET'])
def authenticate_user_invited(request):

    permission_classes = [IsAuthenticated]
    
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        datosPer = []
        invitado = []

        if auth_header is None:
            res = {'estatus': False, 'detail':'Falta el encabezado de autorización', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        try:
            auth_type, auth_string = auth_header.split(' ')
        except ValueError:
            res = {'estatus': False, 'detail':'Encabezado de autorización mal formateado', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        if auth_type != 'Basic':
            res = {'estatus': False, 'detail':'Tipo de token de autorización no válido', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_401_UNAUTHORIZED}
            return Response(res)
        
        try:
            decoded_auth_string = base64.b64decode(auth_string).decode()
        except Exception as e:
            res = {'estatus': False, 'detail':'Credenciales mal codificadas', 'token':'', 'user':'invalid', 'nameuser':'', 'statusHttp':status.HTTP_428_PRECONDITION_REQUIRED}
            return Response(res)
        
        username, passw = decoded_auth_string.split(':')

        nombreInvitado, apellidoInvitado = username.split('-')
        emailInvitado, telefonoInvitado = passw.split('-')

        create = Usuarios.objects.create(apellidos=apellidoInvitado, 
                                 nombre=nombreInvitado,
                                 login='Invitado',
                                 password='inter2023',
                                 administrador=False,
                                 movil=telefonoInvitado,
                                 email=emailInvitado,
                                 terminos_condiciones=True,
                                 dateCreate=datetime.now(),
                                 estatus=1)

        #res = {'estatus': False, 'detail':username, 'token':'', 'user':'valid', 'nameuser':"", 'email':"" , 'usuario':'' , 'id':'' , 'puesto':'', 'statusHttp':status.HTTP_200_OK}
    
        valuser = Usuarios.objects.filter(nombre=str(nombreInvitado), apellidos=str(apellidoInvitado), email=str(emailInvitado), movil=str(telefonoInvitado))

        if valuser.exists():
            try:
                user = Usuarios.objects.get(nombre=str(nombreInvitado), apellidos=str(apellidoInvitado), email=str(emailInvitado), movil=str(telefonoInvitado))#DATOS DEL USUARIO
                permisos = Permisos.objects.filter(idUsuario_id=user.id).select_related('idModulo').values('idModulo__id','idModulo__nombre','idModulo__estatus','idModulo__isSubmenu','idModulo__link','idModulo__idMenu','idModulo__icon','lectura','agregar','eliminar','editar','usuarioAsigna').order_by('idModulo__nombre')
                for permiso in permisos:
                    datosPer.append({
                        "modulos_id":permiso['idModulo__id'],
                        "modulos_nombre":permiso['idModulo__nombre'],
                        "modulos_estatus":permiso['idModulo__estatus'],
                        "modulos_isSubmenu":permiso['idModulo__isSubmenu'],
                        "modulos_icon":permiso['idModulo__icon'],
                        "modulos_idMenu":permiso['idModulo__idMenu'],
                        "modulos_link":permiso['idModulo__link'],
                        "permisos_lectura":permiso['lectura'],
                        "permisos_agregar":permiso['agregar'],
                        "permisos_eliminar":permiso['eliminar'],
                        "permisos_editar":permiso['editar'],
                        "permisos_usuarioAsigna":permiso['usuarioAsigna'],
                    })
                
                payload = jwt_payload_handler(user)
                
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (user.nombre, user.apellidos)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                res = {'estatus': True, 'detail':'Usuario Valido', 'token':token, 'user':'valid', 'nameuser':"%s %s" % (user.nombre, user.apellidos), 'email':user.email , 'usuario':user.login , 'id':user.id , 'puesto':user.puesto_funcion,  'admin':user.administrador, 'urlImg':user.urlImg, 'permisos':datosPer, 'statusHttp':status.HTTP_200_OK}
                return Response(res)
            except Exception as e:
                #raise e
                res = {'estatus': False, 'detail':'Su correo y/o contraseña no coinciden con un usuario existente, verifiquelos por favor.', 'token':'', 'user':'valid', 'nameuser':"", 'email':"" , 'usuario':'' , 'id':'' , 'puesto':'', 'statusHttp':status.HTTP_200_OK}
                raise Response(res)
        else:
            res = {'estatus': False, 'detail':'Su correo y/o contraseña no coinciden con un usuario existente, verifiquelos por favor.', 'token':'', 'user':'valid', 'nameuser':"", 'email':"" , 'usuario':'' , 'id':0 , 'puesto':'', 'statusHttp':status.HTTP_200_OK}
            return Response(res)
    except KeyError:
        res = {'estatus': False, 'detail':'Ocurrio un error inesperado, avise a sistemas!', 'token':'', 'user':'invalid', 'statusHttp':status.HTTP_403_FORBIDDEN}
        return Response(res)

# @csrf_exempt 
# @api_view(['POST'])
# def ServiceCoincidencia(request):

#     paisOri = request.data.get('paisOrigen')
#     estadoOri = request.data.get('estadoOrigen')
#     ciudadOri = request.data.get('ciudadOrigen')
#     paisDes = request.data.get('paisDestino')
#     estadoDes = request.data.get('estadoDestino')
#     ciudadDes = request.data.get('ciudadDestino')
#     fechaFin = request.data.get('dateFin')
#     tipoCarga = request.data.get('unidaModality')
#     tipoUnidad = request.data.get('tipoUnidad_id')

#     if paisOri:
#         relacionar = ServicioVenta.objects.filter(paisOrigen=paisOri).filter(estadoOrigen=estadoOri).filter(ciudadOrigen=ciudadOri).filter(paisDestino=paisDes).filter(estadoDestino=estadoDes).filter(ciudadDestino=ciudadDes).filter(unidaModality=tipoCarga).filter(tipoUnidad_id=tipoUnidad).filter(dateFin__gte=fechaFin).filter(checkVentas="SI").order_by('-id')[:3]
#         red = str(relacionar.query)
#         print (red)
#         serializer = FiltroServiceSerializer(relacionar, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"no result": []})