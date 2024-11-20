from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from django.db.models.query_utils import Q
from django.db.models import Count

from .models import EmailDatos, Ofertas, rango_kilometraje, porcentajes_operacion, rango_carga
from .serializers import EmailDatosSerializer, OfertasSerializer, rango_kilometraje_serializer, porcentajes_operacion_serializer, rango_carga_serializer

from datetime import datetime

@csrf_exempt 
@api_view(['POST'])
def datosEmail(request):

    datos = []
    idEma = int(request.data.get('idEmail'))
    correo = str(request.data.get('correo'))
    contra = str(request.data.get('contra'))
    host = str(request.data.get('host'))
    port = int(request.data.get('puerto'))
    usuarioModifica = str(request.data.get('usuario'))

    editar = EmailDatos.objects.get(idEmail=idEma)

    editar.correo = correo
    editar.contra = contra
    editar.host = host
    editar.port = port
    editar.usuarioModifica = usuarioModifica
    editar.dateEdita = datetime.now()
    
    res = editar.save()

    return Response({'data':True})

@csrf_exempt 
@api_view(['POST'])
def obtenerDatosEmail(request):

    editar = EmailDatos.objects.filter(idEmail=1)
    ser = EmailDatosSerializer(editar, many=True)
    
    return Response(ser.data)

@csrf_exempt
@api_view(['GET'])
def ListOfertaFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = request.GET.get('usuario')
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Ofertas.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()

    goods_ser=OfertasSerializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def ListOfertaActivoFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = str(request.GET.get('userSearch', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Ofertas.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()

    goods_ser=OfertasSerializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def ListOfertaInactivaFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = str(request.GET.get('userSearch', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Ofertas.objects.filter(Q(estatus=2)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(estatus=2)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=2)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Ofertas.objects.filter(Q(oferta__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=2)).filter(Q(usuarioAlta = user)).count()

    goods_ser=OfertasSerializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['GET','POST'])
def AgregarOferta(request):

    protocol = request.META['wsgi.url_scheme']+'://'
    host = request.META['HTTP_HOST']+'/'

    if request.method == 'POST':
        datos = request.data

        oferta = request.POST.get('oferta')
        descripcion = request.POST.get('descripcion')
        delDia = request.POST.get('delDia')
        usuarioAlta = request.POST.get('usuarioAlta')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')
        estatus = request.POST.get('estatus')

        if delDia == 'true':
            delDia = 1
        else:
            delDia = 0

        if estatus == 'true':
            estatus = 1
        else:
            estatus = 0
        
        uploaded_image = request.FILES['image']
        
        # Generar un nombre único para la imagen
        nom, ext = os.path.splitext(uploaded_image.name)

        image_name = nom+'-'+oferta+'-'+inicio+ext
        uploaded_image.name = image_name
        # Obtener la URL de la imagen
        image_url = protocol+host+'media/ofertas/'+ uploaded_image.name

        Ofertas.objects.create(oferta = oferta, descripcion = descripcion, delDia = delDia, rutaImg = image_url, inicio = inicio, fin = fin, estatus = estatus, nombreImg = uploaded_image.name, usuarioAlta = usuarioAlta, dateCreate = datetime.now())
        
        validaInsert = Ofertas.objects.filter(Q(oferta=oferta)).filter(Q(descripcion = descripcion)).filter(Q(delDia = delDia)).filter(Q(rutaImg = image_url)).filter(Q(inicio = inicio)).filter(Q(fin = fin)).filter(Q(estatus = estatus)).filter(Q(nombreImg = uploaded_image.name))
        valIns = OfertasSerializer(validaInsert, many=True)
    
        idOferta = int(valIns.data[0]['idOferta'])

        if idOferta > 0 & idOferta != '':


            # Guardar la imagen en el directorio de media
            image_path = default_storage.save(os.path.join(settings.MEDIA_ROOT+'/ofertas/', uploaded_image.name), uploaded_image)
            
            # Guarda la imagen en una ubicación específica en el servidor
            # Ajusta la ruta y el nombre del archivo según tu configuración
            
            with open('administracion/templates/img/ofertas/' + uploaded_image.name, 'wb') as file:
                for chunk in uploaded_image.chunks():
                    file.write(chunk)
            
            # Aquí puedes realizar cualquier otra operación que necesites, como guardar la ruta en la base de datos
            
            resp = [{"insert": True, "msg": "La oferta se dio de alta correctamente.",}] #print(create.idTarifa)
        else:
            resp = [{"insert": False, "msg": "Ocurrio un error al intentar guardar la oferta, comunicate con sistemas.",}]
    else:
        resp = [{"insert": False, "msg": "Ocurrio un error al intentar recuperar la información de la peitcion, comunicate con sistemas.",}]
    
    return Response(resp)

@csrf_protect
def get_csrf_token(request):
    
    if request.method == 'GET':
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})
    
@csrf_exempt 
@api_view(['POST', 'GET'])
def getOferta(request, pk):

    oferta = Ofertas.objects.get(idOferta=pk)
    serializer = OfertasSerializer(oferta)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def editarOferta(request):

    protocol = request.META['wsgi.url_scheme']+'://'
    host = request.META['HTTP_HOST']+'/'

    if request.method == 'POST':

        idOferta = int(request.POST.get('idO'))
        oferta = request.POST.get('oferta')
        descripcion = request.POST.get('descripcion')
        delDia = int(request.POST.get('delDia'))
        usuarioAlta = request.POST.get('usuarioAlta')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')
        estatus = int(request.POST.get('estatus'))
        uploaded_image = request.FILES['image']
        csrfmiddlewaretoken = request.POST.get['csrfmiddlewaretoken']
        rutaImg = request.POST.get['rutaImg']
        nombreImg = request.POST.get['nombreImg']
        
        # Generar un nombre único para la imagen
        nom, ext = os.path.splitext(uploaded_image.name)

        image_name = nom+'-'+oferta+'-'+inicio+ext
        uploaded_image.name = image_name

        # Obtener la URL de la imagen
        image_url = protocol+host+'media/ofertas/'+ uploaded_image.name

        if rutaImg == '':

            rutaImagen = 'administracion/templates/img/ofertas/' + nombreImg
            os.remove(rutaImagen)
            # Guardar la imagen en el directorio de media
            image_path = default_storage.save(os.path.join(settings.MEDIA_ROOT+'/ofertas/', uploaded_image.name), uploaded_image)
                
            # Guarda la imagen en una ubicación específica en el servidor
            # Ajusta la ruta y el nombre del archivo según tu configuración
                
            with open('administracion/templates/img/ofertas/' + uploaded_image.name, 'wb') as file:
                for chunk in uploaded_image.chunks():
                    file.write(chunk)
                
            # Aquí puedes realizar cualquier otra operación que necesites, como guardar la ruta en la base de datos
        else:
            # Guardar la imagen en el directorio de media
            image_path = default_storage.save(os.path.join(settings.MEDIA_ROOT+'/ofertas/', uploaded_image.name), uploaded_image)
                
            # Guarda la imagen en una ubicación específica en el servidor
            # Ajusta la ruta y el nombre del archivo según tu configuración
                
            with open('administracion/templates/img/ofertas/' + uploaded_image.name, 'wb') as file:
                for chunk in uploaded_image.chunks():
                    file.write(chunk)
                
            # Aquí puedes realizar cualquier otra operación que necesites, como guardar la ruta en la base de datos

        oferta = Ofertas.objects.get(idOferta=idOferta)
        oferta.oferta = oferta
        oferta.descripcion = descripcion
        oferta.delDia = delDia
        oferta.rutaImg = image_url
        oferta.nombreImg = nombreImg
        oferta.inicio = inicio
        oferta.fin = fin
        oferta.estatus = estatus
        oferta.nombreImg = uploaded_image.name
        oferta.usuarioModifica = usuarioAlta
        oferta.dateEdita = datetime.now()
            
        resp = [{"insert": True, "msg": "La oferta se dio de alta correctamente.",}]
        
    else:
        resp = [{"insert": False, "msg": "Ocurrio un error al intentar recuperar la información de la peitcion, comunicate con sistemas.",}]
    
    return Response(resp)

@csrf_exempt
@api_view(['GET'])
def ListOfertaPublico(request):

    goodslist = Ofertas.objects.filter(Q(estatus=1))
    goods_ser=OfertasSerializer(goodslist,many=True)

    return Response({'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def ListRangoKilometraje(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = request.GET.get('usuario')
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = rango_kilometraje.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = rango_kilometraje.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = rango_kilometraje.objects.filter(Q(min__icontains=palabra) | Q(max__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = rango_kilometraje.objects.filter(Q(min__icontains=palabra) | Q(max__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()

    goods_ser=rango_kilometraje_serializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['POST'])
def AgregarRango(request):

    min = int(request.data.get('min'))
    max = int(request.data.get('max'))
    orden = int(request.data.get('orden'))
    estatus = request.data.get('estatus')
    usuarioAlta = request.data.get('usuarioAlta')

    count = rango_kilometraje.objects.filter(Q(min=min)).filter(Q(max = max)).count()
    if count == 0:

        rango_kilometraje.objects.create(min = min, max = max, orden = orden, estatus = estatus, usuarioAlta = usuarioAlta, dateCreate = datetime.now())
        resp = [{"insert": True, "msg": "El Rango de Kilometraje se dio de alta correctamente.",}]
    else:
        resp = [{"insert": False, "msg": "El rango de kilometraje que intentas dar de alta, ya esta registrado.",}]
    
    return Response(resp)

@csrf_exempt
@api_view(['GET'])
def ListPorcentajesOperacion(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = request.GET.get('usuario')
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = porcentajes_operacion.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = porcentajes_operacion.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = porcentajes_operacion.objects.filter(Q(mercancia__icontains=palabra) | Q(porcentaje__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = porcentajes_operacion.objects.filter(Q(mercancia__icontains=palabra) | Q(porcentaje__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()

    goods_ser=porcentajes_operacion_serializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['POST'])
def AgregarPorcentajes(request):

    mercancia = request.data.get('mercancia')
    porcentaje = float(request.data.get('porcentaje'))
    estatus = request.data.get('estatus')
    usuarioAlta = request.data.get('usuarioAlta')
    tipo = request.data.get('tipo')

    count = porcentajes_operacion.objects.filter(Q(mercancia=mercancia)).filter(Q(porcentaje = porcentaje)).count()
    if count == 0:

        porcentajes_operacion.objects.create(mercancia = mercancia, porcentaje = porcentaje, estatus = estatus, usuarioAlta = usuarioAlta, tipo = tipo, dateCreate = datetime.now())
        resp = [{"insert": True, "msg": "El Porcentaje se dio de alta correctamente.",}]
    else:
        resp = [{"insert": False, "msg": "El Porcentaje que intentas dar de alta, ya esta registrado.",}]
    
    return Response(resp)

@csrf_exempt
@api_view(['GET'])
def ListRangos(request):

    goodslist = rango_kilometraje.objects.filter(Q(estatus=1)).order_by('orden')
    goods_ser=rango_kilometraje_serializer(goodslist,many=True)

    return Response({'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def getPorcentajesOperacion(request):

    goodslist = porcentajes_operacion.objects.filter(Q(estatus=1)).order_by('id_incremento')
    goods_ser = porcentajes_operacion_serializer(goodslist,many=True)

    return Response({'data':goods_ser.data})

@csrf_exempt 
@api_view(['POST', 'GET'])
def getIncremento(request, pk):

    incremento = porcentajes_operacion.objects.get(id_incremento=pk)
    serializer = porcentajes_operacion_serializer(incremento)
    return Response(serializer.data)

@csrf_exempt 
@api_view(['PUT'])
def editarIncremento(request):

    resp = {}

    id = int(request.data.get('id_incremento'))
    mercancias = request.data.get('mercancias')
    porcentaje = request.data.get('porcentaje')
    estatus = bool(request.data.get('estatus'))
    if estatus:
        estatus = 1
    else:
        estatus = 0
    usuario = request.data.get('usuario')
    tipo = request.data.get('tipoPorcentaje')
    vigencia_inicio = request.data.get('vigencia_inicio')
    vigencia_fin = request.data.get('vigencia_fin')

    if id != 0:
        incremento = porcentajes_operacion.objects.get(id_incremento=id)
        incremento.mercancia = mercancias
        incremento.porcentaje = porcentaje
        incremento.estatus = estatus
        incremento.usuarioModifica = usuario
        incremento.dateEdita = datetime.now()
        incremento.tipo = tipo
        incremento.vigencia_inicio = vigencia_inicio
        incremento.vigencia_fin = vigencia_fin
        incremento.save()

        resp = [{"update": True, "msg": "El Porcentaje se actualizó correctamente.",}]
    else:
        resp = [{"update": False, "msg": "Se encontro un problema al actualizar el Porcentaje, comunicate con sistemas.",}]
    
    return Response(resp)

@csrf_exempt
@api_view(['GET'])
def ListRangosMercancias(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = request.GET.get('usuario')
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = rango_carga.objects.filter(Q(estatus=1)).order_by('orden')[data_start:data_end]
        count = rango_carga.objects.filter(Q(estatus=1)).count()
    else:
        goodslist = rango_carga.objects.filter(Q(min__icontains=palabra) | Q(max__icontains=palabra)).filter(Q(estatus=1))[data_start:data_end]
        count = rango_carga.objects.filter(Q(min__icontains=palabra) | Q(max__icontains=palabra)).filter(Q(estatus=1)).count()

    goods_ser = rango_carga_serializer(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['POST'])
def AgregarRangoMercancia(request):

    min = request.data.get('min')
    max = request.data.get('max')
    orden = int(request.data.get('orden'))
    estatus = request.data.get('estatus')
    usuarioAlta = request.data.get('usuarioAlta')
    porcentaje = float(request.data.get('porcentaje'))

    count = rango_carga.objects.filter(Q(min=min)).filter(Q(max = max)).count()
    if count == 0:

        rango_carga.objects.create(min = min, max = max, orden = orden, estatus = estatus, usuarioAlta = usuarioAlta, dateCreate = datetime.now(), porcentaje = porcentaje)
        resp = [{"insert": True, "msg": "El Rango de la Mercancia se dio de alta correctamente.",}]
    else:
        resp = [{"insert": False, "msg": "El Rango de la Mercancia que intentas dar de alta, ya esta registrado.",}]
    
    return Response(resp)

@csrf_exempt
@api_view(['GET'])
def ListRangosCargas(request):
    
    goodslist = rango_carga.objects.filter(Q(estatus=1)).order_by('orden')
    
    goods_ser=rango_carga_serializer(goodslist,many=True)

    return Response(goods_ser.data)

@csrf_exempt 
@api_view(['POST', 'GET'])
def send_email_carlos(request):
    from_email = 'danielrg841@hotmail.com'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'danielrg841@hotmail.com'
    smtp_password = 'tu_contraseña'

    nombreEmpresa = request.data.get('company_name')
    emails_d = request.data.get('emails')
    subject = f"Mensaje para {nombreEmpresa}"
    
    # Datos para la plantilla
    context = {
        'nombreEmpresa': nombreEmpresa,
    }

    # Renderizar la plantilla HTML
    html_content = render_to_string('html/correoCarlos.html', context)
    
    try:
        # Crear el objeto EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, '', from_email, emails_d)
        msg.attach_alternative(html_content, "text/html")

        # Configurar el servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        # Enviar el correo
        server.sendmail(from_email, emails_d, msg.as_string())
        server.quit()

        return JsonResponse({'status': 'success'}, status=200)
    except smtplib.SMTPAuthenticationError as e:
        return JsonResponse({'status': 'error', 'message': f'Authentication error: {e.smtp_code} {e.smtp_error.decode()}'}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid request'}, status=400)
