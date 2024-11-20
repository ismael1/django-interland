from difflib import context_diff
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from click import Context
from servicioVenta.serializers import FiltroServiceSerializer
from django.shortcuts import render


from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models.query_utils import Q

#Generar PDF Librerias Necesarias Agregado David
import os
from django.views.generic import ListView, View 
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import context, pisa
from django.contrib.staticfiles import finders
#Fin Librerias PDF Necesarias

#Nueva Llibreria PDF
# from weasyprint import HTML
#Fi Libreria PDF

###
import smtplib
from smtplib import SMTPException, SMTPSenderRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.conf import settings

from datetime import datetime, date

from servicioVenta.serializers import ServicioVenta
from servicios.views import ServicesViewSet 
from servicios.serializers import ServicesSerializer
from .models import ServicioCotizacion, ContactoCotizacion, ServiciosAgregadosCotizacion, Consecutivo, Rutas, Tarifas
from .serializers import FiltroServicioCotizacion, SerializerServicioCotizacion, SerializerContactoCotizacion, SerializerServiciosAgregadosCotizacion, SerializerConsecutivo, SerializerTarifas, SerializerRutas
from catalogos.models import ClaveProdServ
from catalogos.serializers import ClaveProdServSerializer
from administracion.models import EmailDatos
from administracion.serializers import EmailDatosSerializer

from customer.models import ZonasHijos
from customer.serializers import ZonasHijosSerializer


from io import BytesIO



class ServicioCotizaciones(viewsets.ModelViewSet):
    queryset = ServicioCotizacion.objects.all()
    serializer_class = SerializerServicioCotizacion

class ServiciosAgregadosCotizaciones(viewsets.ModelViewSet):
    queryset = ServiciosAgregadosCotizacion.objects.all()
    serializer_class = SerializerServiciosAgregadosCotizacion

class ContactoCotizaciones(viewsets.ModelViewSet):
    queryset = ContactoCotizacion.objects.all()
    serializer_class = SerializerContactoCotizacion

#Consulta consecutivo de cotizaciones
@csrf_exempt 
@api_view(['POST'])
def getConsecutivo(request):

    id = request.data.get('id')
    if id:
        consecutivo = Consecutivo.objects.all().order_by("-id")[:1]

        serializer = SerializerConsecutivo(consecutivo, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST', 'GET'])
def insertConsecutivo(request):  

    id = request.data.get('idAnt')
    fecConse = request.data.get('fecConse')
    fecHoy = request.data.get('fechaHoy')

    format = "%Y/%m/%d" #specifify the format of the date_string.
    date1 = datetime.strptime(fecConse, format)
    date2 = datetime.strptime(fecHoy, format)

    anio1 = int(date1.year)
    anio2 = int(date2.year)

    if anio2 > anio1:
        consecutivo = Consecutivo.objects.create(id=id+1, numero=0, control="SC", fecha=date2)
        serializer = SerializerConsecutivo(consecutivo)
        return Response('Exito')
    else:
        return Response('No actualiza')

@csrf_exempt 
@api_view(['PUT'])
def updateConsecutivo(request, pk):
    
    id = request.data.get('id')
    num = request.data.get('numero')
    anio = request.data.get('anio')

    if id:
        consecutivo = Consecutivo.objects.get(id=id)
        consecutivo.numero = num
        consecutivo.save()
        return Response("exito")
    else:
        return Response({"no update"})

@csrf_exempt 
@api_view(['POST'])
def ServiceCoincidencia(request):

    paisOri = request.data.get('paisOrigen')
    estadoOri = request.data.get('estadoOrigen')
    ciudadOri = request.data.get('ciudadOrigen')
    paisDes = request.data.get('paisDestino')
    estadoDes = request.data.get('estadoDestino')
    ciudadDes = request.data.get('ciudadDestino')
    fechaFin = request.data.get('dateFin')
    tipoCarga = request.data.get('unidaModality')
    tipoUnidad = request.data.get('tipoUnidad_id')
    
    # fecha_hoy= 2021-07-13
    # select * from servicos_venata  where fecha_vigencia >  fecha_hoy

    # __lte Se utiliza para fechas -> equivalente a fechaFin <= fecha hoy
    # __gte Se utiliza para fechas -> equivalente a fechaFin >= fecha hoy

    if paisOri:
        #relacionar = ServicioVenta.objects.filter(paisOrigen=paisOri).filter(estadoOrigen=estadoOri).filter(ciudadOrigen=ciudadOri).filter(paisDestino=paisDes).filter(estadoDestino=estadoDes).filter(ciudadDestino=ciudadDes).filter(unidaModality=tipoCarga).filter(tipoUnidad_id=tipoUnidad).filter(dateFin__gte=fechaFin).filter(checkVentas="SI").order_by('-id')[:3]
        relacionar = ServicioVenta.objects.filter(paisOrigen=paisOri).filter(estadoOrigen=estadoOri).filter(ciudadOrigen=ciudadOri).filter(paisDestino=paisDes).filter(estadoDestino=estadoDes).filter(ciudadDestino=ciudadDes).filter(unidaModality=tipoCarga).filter(tipoUnidad_id=tipoUnidad).filter(checkVentas="SI").order_by('-id')[:3]
        # red = str(relacionar.query)
        # print (red)
        serializer = FiltroServiceSerializer(relacionar, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST'])
def tarifaCoincidencia(request):
    paisOri = request.data.get('paisOrigen')
    estadoOri = request.data.get('estadoOrigen')
    ciudadOri = request.data.get('ciudadOrigen')
    coloniaOri = request.data.get('coloniaOrigen')
    cpOrigen = request.data.get('cpOrigen')
    paisDes = request.data.get('paisDestino')
    estadoDes = request.data.get('estadoDestino')
    ciudadDes = request.data.get('ciudadDestino')
    cpDestino = request.data.get('cpDestino')
    coloniaDes = request.data.get('coloniaDestino')
    fechaFin = request.data.get('dateFin')
    tipoCarga = request.data.get('unidaModality')
    tipoUnidad = request.data.get('tipoUnidad_id')

    #SE VALIDA LA EXISTENCIA DE LOS CODIGOS POSTALES EN LA TABLA DE ZONAS
    if ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri).exists() and ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes).exists():
        idorigenE = ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri)
        idorigenESer = ZonasHijosSerializer(idorigenE, many=True)

        idOrigen = idorigenESer.data[0]['idZonasHijo']

        iddestinoE = ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes)
        iddestinoESer = ZonasHijosSerializer(iddestinoE, many=True)

        idDestino = iddestinoESer.data[0]['idZonasHijo']

        existeTarifa = Tarifas.objects.filter(idTarifasOrigen_id=idOrigen).filter(idTarifasDestino_id=idDestino).exists()
        
        if existeTarifa:
            datosTarifa = Tarifas.objects.filter(idTarifasOrigen_id=idOrigen).filter(idTarifasDestino_id=idDestino)
            datosTarSer = SerializerTarifas(datosTarifa, many=True)
            return Response(datosTarSer.data)
        else:
            datosTarifa = Tarifas.objects.create(
                idTarifasOrigen_id = idOrigen ,
                idTarifasDestino_id = idDestino,
                tarifaKilometro = 64.75,
                estatus = 1,
                dateCreate = datetime.now()
            )
            datosTarSer = SerializerTarifas(datosTarifa)
            return Response(datosTarSer.data)

    return Response({})

@csrf_exempt 
@api_view(['POST'])
def rutasCoincidencia(request):
    paisOri = request.data.get('paisOrigen')
    estadoOri = request.data.get('estadoOrigen')
    ciudadOri = request.data.get('ciudadOrigen')
    coloniaOri = request.data.get('coloniaOrigen')
    cpOrigen = request.data.get('cpOrigen')
    paisDes = request.data.get('paisDestino')
    estadoDes = request.data.get('estadoDestino')
    ciudadDes = request.data.get('ciudadDestino')
    cpDestino = request.data.get('cpDestino')
    coloniaDes = request.data.get('coloniaDestino')
    fechaFin = request.data.get('dateFin')
    tipoCarga = request.data.get('unidaModality')
    tipoUnidad = request.data.get('tipoUnidad_id')

    #SE VALIDA LA EXISTENCIA DE LOS CODIGOS POSTALES EN LA TABLA DE ZONAS
    print(ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri).exists())
    print(ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes).exists())
    if ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri).exists() and ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes).exists():
        idorigenE = ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri)
        idorigenESer = ZonasHijosSerializer(idorigenE, many=True)

        idOrigen = idorigenESer.data[0]['idZonasHijo']

        iddestinoE = ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes)
        iddestinoESer = ZonasHijosSerializer(iddestinoE, many=True)

        idDestino = iddestinoESer.data[0]['idZonasHijo']

        existeRuta = Rutas.objects.filter(idrutasOrigen_id=idOrigen).filter(idrutasDestino_id=idDestino).exists()
        
        if existeRuta:
            datosRuta = Rutas.objects.filter(idrutasOrigen_id=idOrigen).filter(idrutasDestino_id=idDestino)
            print(datosRuta.query)
            datosRutSer = SerializerRutas(datosRuta, many=True)
            return Response(datosRutSer.data)

    return Response({})

@csrf_exempt
@api_view(['GET'])
def ListCotizacionFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        user = str(request.GET.get('userSearch', 1))
        data_start = (page - 1) * size
        data_end = page * size

        now = datetime.now()

        year = now.year
        month = now.month
        day = now.day

        if (palabra == ""):
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).filter(Q(usuarioGenera = user)).count()
        else:
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0)).filter(Q(usuarioGenera = user)).count()

        goods_ser=FiltroServicioCotizacion(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListCotizacionFiltroContesta(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        user = str(request.GET.get('userSearch', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(estatus=1))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(estatus=1)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(estatus=1)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(estatus=1)).filter(Q(usuarioGenera = user)).count()
        else:
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=1))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=1)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioGenera = user)).count()

        goods_ser=FiltroServicioCotizacion(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListCotizacionFiltroNoContesta(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        user = str(request.GET.get('userSearch', 1))

        data_start = (page - 1) * size
        data_end = page * size
        
        now = datetime.now()
        
        fecha = str(now)[:10]

        if (palabra == ""):
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(estatus=0)).filter(dateCreate__lt=fecha)[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(estatus=0)).filter(dateCreate__lt=fecha).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(estatus=0)).filter(dateCreate__lt=fecha).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(estatus=0)).filter(dateCreate__lt=fecha).filter(Q(usuarioGenera = user)).count()
        else:
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=0)).filter(dateCreate__lt=fecha)[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=0)).filter(dateCreate__lt=fecha).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=0)).filter(Q(usuarioGenera = user)).filter(dateCreate__lt=fecha)[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(Q(estatus=0)).filter(Q(usuarioGenera = user)).filter(dateCreate__lt=fecha).count()

        goods_ser=FiltroServicioCotizacion(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

# Consultar Folio
class ConsultarFolio(APIView):
    def get(self, request, format=None):
        buscarFolio = ServicioCotizacion.objects.latest('folio')
        serializer = FiltroServicioCotizacion(buscarFolio)
        return Response(serializer.data)

@csrf_exempt 
@api_view(['POST'])
def ServicePrice(request):
    
    nombreServicio = request.data.get('servicio')

    if nombreServicio:
        buscar = ServicioVenta.objects.filter(servicio=nombreServicio).order_by('-id')[0:1]
        # red = str(buscar.query)
        # print (red)
        serializer = FiltroServiceSerializer(buscar, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

# Consultar Servicios Agregados
@csrf_exempt 
@api_view(['POST'])
def ConsultarServiciosAgregados(request):
    
    servicios = request.data.get('idcotizacion')

    if servicios:
        buscarServicios = ServiciosAgregadosCotizacion.objects.filter(idcotizacion=servicios)
        # red = str(buscarServicios.query)
        # print (red)
        serializer = SerializerServiciosAgregadosCotizacion(buscarServicios, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

# Consultar Contacto Agregado
@csrf_exempt 
@api_view(['POST'])
def ConsultarContactoAgregado(request):
    
    contacto = request.data.get('idcotizacion')

    if contacto:
        buscarServicios = ContactoCotizacion.objects.filter(idcotizacion=contacto)
        # red = str(buscarServicios.query)
        # print (red)
        serializer = SerializerContactoCotizacion(buscarServicios, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

# GENERAR PDF Prueba 1
# class PDFCotizacion(APIView):
#     def get(self, request, *args, **kwargs):
#         cotiza = ServicioCotizacion.objects.filter(id=15)        
#         serializer = FiltroServicioCotizacion(cotiza, many=True)
#         # return Response(serializer.data)
#         # template = get_template('pdf/customers.html')
#         template = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': serializer.data})   
#         # print(template)
#         # context = {'title': 'Lista Clientes PDF'}
#         # html = template.render(context)
#         html = template
#         response = HttpResponse(content_type= 'application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="Cotizacion.pdf"'
#         pisa_status = pisa.CreatePDF(html, dest = response)
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
#         return response


# GENERAR PDF Prueba 2 WeasyPrint
class PDFCotizacion(View):

    # def link_callback(self, request, *args, **kwargs):
    #     sUrl = settings.STATIC_URL
    #     sRoot = settings.STATIC_ROOT
    #     mUrl = settings.MEDIA_URL
    #     mRoot = settings.MEDIA_ROOT
    #     return os.path

    def get(self,request, pk):
        ids=pk
        servRes = []
        # ids=3

        # context = {
        #     'icon': '{}{}'.format(settings.STATIC_URL, '/media/img/logo_i.png')
        # }
        
        cotiza = ServicioCotizacion.objects.filter(id=ids)
        coti = FiltroServicioCotizacion(cotiza, many=True)

        divisa = int(coti.data[0]['divisaFinal'])
        valorDolar = 19.8532

        service = ServiciosAgregadosCotizacion.objects.filter(idcotizacion_id=ids)
        serv = SerializerServiciosAgregadosCotizacion(service, many=True)

            
        if divisa == 2:
            for dato in service:

                ajustePorcentOpt = float(dato.porcentajeVenta) ## 10
                ajustePorcentExp = float(dato.porcentajeXpress) ## 10


                #------------------------------------INICIA OPTIMO------------------------------------#

                porcentajeBaseOptExt = float(dato.subtotal) * ((ajustePorcentOpt) / 100); ## 2000 * ((10+13)/100) = 460

                precioBaseOptExt = float(dato.subtotal) + porcentajeBaseOptExt ## 2000 + 460 = 2460

                porcentajeIvaOpt = precioBaseOptExt * (float(dato.iva) / 100) ## 2460 * (16 / 100) = 393.6

                totalOptExt = precioBaseOptExt + porcentajeIvaOpt
                
                monedaOptExt = totalOptExt / float(valorDolar)

                #------------------------------------TERMINA OPTIMO------------------------------------#

                #------------------------------------INICIA EXPRESS------------------------------------#

                porcentajeBaseExpExt = float(dato.subtotal) * ((ajustePorcentExp) / 100); ## 2000 * ((10)/100) = 200

                precioBaseExpExt = float(dato.subtotal) + porcentajeBaseOptExt + porcentajeBaseExpExt; ## 2000 + 200 + 200 = 2400

                porcentajeIvaExp = precioBaseExpExt * (float(dato.iva) / 100); ## 2400 * (16 / 100) = 384

                totalExpExt = precioBaseExpExt + porcentajeIvaExp; ## 2400 + 384

                monedaExpExt = totalExpExt / float(valorDolar)

                #------------------------------------TERMINA EXPRESS------------------------------------#

                servRes.append({
                    'id': dato.id,
                    'idService': dato.idService,
                    'nameService': dato.nameService,
                    'priceService': float(dato.priceService),
                    'subtotalNoAgrega': float(dato.priceService) / ((float(dato.iva)/100.00) + 1) if int(dato.iva) > 0 else float(0),
                    'ivaNoAgrega': (float(dato.priceService) / ((float(dato.iva)/100.00) + 1)) * (float(dato.iva)/100.00) if int(dato.iva) > 0 else float(0),
                    'subtotalNoAgregaExp': precioBaseExpExt,
                    'ivaNoAgregaExp': porcentajeIvaExp,
                    'totalExpNoAgrega': totalExpExt,
                    'dateCreate': dato.dateCreate,
                    'idcotizacion_id': dato.idcotizacion_id,
                    'ajusteTotal': dato.ajusteTotal,
                    'ajusteVenta': dato.ajusteVenta,
                    'porcentaje': dato.porcentaje,
                    'agregado': dato.agregado,
                    'idVenta': dato.idVenta,
                    'divisa': dato.divisa,
                    'iva': dato.iva,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'retencion': dato.retencion if not dato.retencion is None else 0,
                    'subtotal': dato.subtotal,
                    'total': dato.total,
                    'basePorcExp': dato.basePorcExp,
                    'basePorcOpt': dato.basePorcOpt,
                    'monedaExpExt': dato.monedaExpExt,
                    'monedaOptExt': dato.monedaOptExt,
                    'porcentajeBaseExpExt': dato.porcentajeBaseExpExt,
                    'porcentajeBaseOptExt': dato.porcentajeBaseOptExt,
                    'porcentajeExtra': dato.porcentajeExtra,
                    'porcentajeIvaExp': dato.porcentajeIvaExp,
                    'porcentajeIvaOpt': dato.porcentajeIvaOpt,
                    'precioBaseExpExt': dato.precioBaseExpExt,
                    'precioBaseOptExt': dato.precioBaseOptExt,
                    'totalExpExt': dato.totalExpExt,
                    'totalOptExt': dato.totalOptExt,
                })
        else:
            for dato in service:
                ajustePorcentOpt = float(dato.porcentajeVenta) ## 10
                ajustePorcentExp = float(dato.porcentajeXpress) ## 10


                #------------------------------------INICIA OPTIMO------------------------------------#

                porcentajeBaseOptExt = float(dato.subtotal) * ((ajustePorcentOpt) / 100); ## 2000 * ((10+13)/100) = 460

                precioBaseOptExt = float(dato.subtotal) + porcentajeBaseOptExt ## 2000 + 460 = 2460

                porcentajeIvaOpt = precioBaseOptExt * (float(dato.iva) / 100) ## 2460 * (16 / 100) = 393.6

                totalOptExt = precioBaseOptExt + porcentajeIvaOpt

                #------------------------------------TERMINA OPTIMO------------------------------------#

                #------------------------------------INICIA EXPRESS------------------------------------#

                porcentajeBaseExpExt = float(dato.subtotal) * ((ajustePorcentExp) / 100); ## 2000 * ((10)/100) = 200

                precioBaseExpExt = float(dato.subtotal) + porcentajeBaseOptExt + porcentajeBaseExpExt; ## 2000 + 200 + 200 = 2400

                porcentajeIvaExp = precioBaseExpExt * (float(dato.iva) / 100); ## 2400 * (16 / 100) = 384

                totalExpExt = precioBaseExpExt + porcentajeIvaExp; ## 2400 + 384

                #------------------------------------TERMINA EXPRESS------------------------------------#

                servRes.append({
                    'id': dato.id,
                    'idService': dato.idService,
                    'nameService': dato.nameService,
                    'priceService': float(dato.priceService),
                    'subtotalNoAgrega': ((float(dato.priceService) / ((float(dato.iva)/100.00) + 1))) / float(valorDolar)  if int(dato.iva) > 0 else float(0),
                    'ivaNoAgrega': (((float(dato.priceService) / ((float(dato.iva)/100.00) + 1)) * (float(dato.iva)/100.00)))  / float(valorDolar) if int(dato.iva) > 0 else float(0),
                    'subtotalNoAgregaExp': precioBaseExpExt / float(valorDolar),
                    'ivaNoAgregaExp': porcentajeIvaExp / float(valorDolar),
                    'totalExpNoAgrega': totalExpExt / float(valorDolar),
                    'dateCreate': dato.dateCreate,
                    'idcotizacion_id': dato.idcotizacion_id,
                    'ajusteTotal': dato.ajusteTotal,
                    'ajusteVenta': dato.ajusteVenta,
                    'porcentaje': dato.porcentaje,
                    'agregado': dato.agregado,
                    'idVenta': dato.idVenta,
                    'divisa': dato.divisa,
                    'iva': dato.iva,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'retencion': dato.retencion if not dato.retencion is None else 0,
                    'subtotal': dato.subtotal,
                    'total': dato.total,
                    'basePorcExp': dato.basePorcExp,
                    'basePorcOpt': dato.basePorcOpt,
                    'monedaExpExt': dato.monedaExpExt,
                    'monedaOptExt': dato.monedaOptExt,
                    'porcentajeBaseExpExt': float(dato.porcentajeBaseExpExt) / float(valorDolar),
                    'porcentajeBaseOptExt': float(dato.porcentajeBaseOptExt) / float(valorDolar),
                    'porcentajeExtra': float(dato.porcentajeExtra) / float(valorDolar),
                    'porcentajeIvaExp': float(dato.porcentajeIvaExp) / float(valorDolar),
                    'porcentajeIvaOpt': float(dato.porcentajeIvaOpt) / float(valorDolar),
                    'precioBaseExpExt': float(dato.precioBaseExpExt) / float(valorDolar),
                    'precioBaseOptExt': float(dato.precioBaseOptExt) / float(valorDolar),
                    'totalExpExt': float(dato.totalExpExt) / float(valorDolar),
                    'totalOptExt': float(dato.totalOptExt) / float(valorDolar),
                })

        print(servRes)

        contact = ContactoCotizacion.objects.filter(idcotizacion_id=ids)
        cont = SerializerContactoCotizacion(contact, many=True)

        catServ = ClaveProdServ.objects.filter(clave_prodserv=coti.data[0]['idclasificacion']) 
        cServ = ClaveProdServSerializer(catServ, many=True)

        html = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'ContactoCotizacion': cont.data, 'clasif':cServ.data }) 
        # html= template = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': serv.data, 'ContactoCotizacion': cont.data }, context) 
        # template = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': serializer.data}, {'ServiciosAgregadosCotizacion': serializer.data})
        response = HttpResponse(content_type= 'application/pdf')
        pisa_status = pisa.CreatePDF(html, dest=response)
        # pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

@csrf_exempt 
@api_view(['POST', 'GET'])
def send_email(request):

    pkC = request.data.get('idcotizacion')
    email = request.data.get('email')
    nombre_contacto = request.data.get('name')
    servRes = []

    # Establecemos conexion con el servidor smtp de gmail
    # mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    
    emailD = EmailDatos.objects.filter(idEmail=1)
    emailS = EmailDatosSerializer(emailD, many=True)

    correoInt = emailS.data[0]['correo']
    contraInt = emailS.data[0]['contra']
    hostInter = emailS.data[0]['host']
    puerInter = emailS.data[0]['port']

    mensaje = MIMEMultipart()

    #mailServer = smtplib.SMTP('smtp.office365.com', 587)

    mailServer = smtplib.SMTP(hostInter, puerInter)
    
    #mailServer.set_debuglevel(2)
        
    mailServer.starttls()

    mailServer.login(correoInt, contraInt)
    #mailServer.login('infor@mx-interland.com', '=wAQ15&ix8')
    email_to=email

    mensaje['From']= correoInt
    mensaje['To']=email_to
    mensaje['Subject'] = "Solicitud de Cotización"

    content = render_to_string('pdf/correoCotizacion.html', {'name': nombre_contacto})
    mensaje.attach(MIMEText(content,'html'))

    cotiza = ServicioCotizacion.objects.filter(id=pkC)
    coti = FiltroServicioCotizacion(cotiza, many=True)

    divisa = int(coti.data[0]['divisaFinal'])
    valorDolar = 19.8532

    service = ServiciosAgregadosCotizacion.objects.filter(idcotizacion_id=pkC)
    serv = SerializerServiciosAgregadosCotizacion(service, many=True)

    if divisa == 2:
        for dato in service:

            ajustePorcentOpt = float(dato.porcentajeVenta) ## 10
            ajustePorcentExp = float(dato.porcentajeXpress) ## 10


            #------------------------------------INICIA OPTIMO------------------------------------#

            porcentajeBaseOptExt = float(dato.subtotal) * ((ajustePorcentOpt) / 100); ## 2000 * ((10+13)/100) = 460

            precioBaseOptExt = float(dato.subtotal) + porcentajeBaseOptExt ## 2000 + 460 = 2460

            porcentajeIvaOpt = precioBaseOptExt * (float(dato.iva) / 100) ## 2460 * (16 / 100) = 393.6

            totalOptExt = precioBaseOptExt + porcentajeIvaOpt
                
            monedaOptExt = totalOptExt / float(valorDolar)

            #------------------------------------TERMINA OPTIMO------------------------------------#

            #------------------------------------INICIA EXPRESS------------------------------------#

            porcentajeBaseExpExt = float(dato.subtotal) * ((ajustePorcentExp) / 100); ## 2000 * ((10)/100) = 200

            precioBaseExpExt = float(dato.subtotal) + porcentajeBaseOptExt + porcentajeBaseExpExt; ## 2000 + 200 + 200 = 2400

            porcentajeIvaExp = precioBaseExpExt * (float(dato.iva) / 100); ## 2400 * (16 / 100) = 384

            totalExpExt = precioBaseExpExt + porcentajeIvaExp; ## 2400 + 384

            monedaExpExt = totalExpExt / float(valorDolar)

            #------------------------------------TERMINA EXPRESS------------------------------------#

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'priceService': float(dato.priceService),
                'subtotalNoAgrega': float(dato.priceService) / ((float(dato.iva)/100.00) + 1) if int(dato.iva) > 0 else float(0),
                'ivaNoAgrega': (float(dato.priceService) / ((float(dato.iva)/100.00) + 1)) * (float(dato.iva)/100.00) if int(dato.iva) > 0 else float(0),
                'subtotalNoAgregaExp': precioBaseExpExt,
                'ivaNoAgregaExp': porcentajeIvaExp,
                'totalExpNoAgrega': totalExpExt,
                'dateCreate': dato.dateCreate,
                'idcotizacion_id': dato.idcotizacion_id,
                'ajusteTotal': dato.ajusteTotal,
                'ajusteVenta': dato.ajusteVenta,
                'porcentaje': dato.porcentaje,
                'agregado': dato.agregado,
                'idVenta': dato.idVenta,
                'divisa': dato.divisa,
                'iva': dato.iva,
                'porcentajeVenta': dato.porcentajeVenta,
                'porcentajeXpress': dato.porcentajeXpress,
                'retencion': dato.retencion if not dato.retencion is None else 0,
                'subtotal': dato.subtotal,
                'total': dato.total,
                'basePorcExp': dato.basePorcExp,
                'basePorcOpt': dato.basePorcOpt,
                'monedaExpExt': dato.monedaExpExt,
                'monedaOptExt': dato.monedaOptExt,
                'porcentajeBaseExpExt': dato.porcentajeBaseExpExt,
                'porcentajeBaseOptExt': dato.porcentajeBaseOptExt,
                'porcentajeExtra': dato.porcentajeExtra,
                'porcentajeIvaExp': dato.porcentajeIvaExp,
                'porcentajeIvaOpt': dato.porcentajeIvaOpt,
                'precioBaseExpExt': dato.precioBaseExpExt,
                'precioBaseOptExt': dato.precioBaseOptExt,
                'totalExpExt': dato.totalExpExt,
                'totalOptExt': dato.totalOptExt,
            })
    else:
        for dato in service:
            ajustePorcentOpt = float(dato.porcentajeVenta) ## 10
            ajustePorcentExp = float(dato.porcentajeXpress) ## 10

            #------------------------------------INICIA OPTIMO------------------------------------#

            porcentajeBaseOptExt = float(dato.subtotal) * ((ajustePorcentOpt) / 100); ## 2000 * ((10+13)/100) = 460
            precioBaseOptExt = float(dato.subtotal) + porcentajeBaseOptExt ## 2000 + 460 = 2460

            porcentajeIvaOpt = precioBaseOptExt * (float(dato.iva) / 100) ## 2460 * (16 / 100) = 393.6

            totalOptExt = precioBaseOptExt + porcentajeIvaOpt

            #------------------------------------TERMINA OPTIMO------------------------------------#

            #------------------------------------INICIA EXPRESS------------------------------------#

            porcentajeBaseExpExt = float(dato.subtotal) * ((ajustePorcentExp) / 100); ## 2000 * ((10)/100) = 200

            precioBaseExpExt = float(dato.subtotal) + porcentajeBaseOptExt + porcentajeBaseExpExt; ## 2000 + 200 + 200 = 2400

            porcentajeIvaExp = precioBaseExpExt * (float(dato.iva) / 100); ## 2400 * (16 / 100) = 384

            totalExpExt = precioBaseExpExt + porcentajeIvaExp; ## 2400 + 384

            #------------------------------------TERMINA EXPRESS------------------------------------#

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'priceService': float(dato.priceService),
                'subtotalNoAgrega': ((float(dato.priceService) / ((float(dato.iva)/100.00) + 1))) / float(valorDolar)  if int(dato.iva) > 0 else float(0),
                'ivaNoAgrega': (((float(dato.priceService) / ((float(dato.iva)/100.00) + 1)) * (float(dato.iva)/100.00)))  / float(valorDolar) if int(dato.iva) > 0 else float(0),
                'subtotalNoAgregaExp': precioBaseExpExt / float(valorDolar),
                'ivaNoAgregaExp': porcentajeIvaExp / float(valorDolar),
                'totalExpNoAgrega': totalExpExt / float(valorDolar),
                'dateCreate': dato.dateCreate,
                'idcotizacion_id': dato.idcotizacion_id,
                'ajusteTotal': dato.ajusteTotal,
                'ajusteVenta': dato.ajusteVenta,
                'porcentaje': dato.porcentaje,
                'agregado': dato.agregado,
                'idVenta': dato.idVenta,
                'divisa': dato.divisa,
                'iva': dato.iva,
                'porcentajeVenta': dato.porcentajeVenta,
                'porcentajeXpress': dato.porcentajeXpress,
                'retencion': dato.retencion if not dato.retencion is None else 0,
                'subtotal': dato.subtotal,
                'total': dato.total,
                'basePorcExp': dato.basePorcExp,
                'basePorcOpt': dato.basePorcOpt,
                'monedaExpExt': dato.monedaExpExt,
                'monedaOptExt': dato.monedaOptExt,
                'porcentajeBaseExpExt': float(dato.porcentajeBaseExpExt) / float(valorDolar),
                'porcentajeBaseOptExt': float(dato.porcentajeBaseOptExt) / float(valorDolar),
                'porcentajeExtra': float(dato.porcentajeExtra) / float(valorDolar),
                'porcentajeIvaExp': float(dato.porcentajeIvaExp) / float(valorDolar),
                'porcentajeIvaOpt': float(dato.porcentajeIvaOpt) / float(valorDolar),
                'precioBaseExpExt': float(dato.precioBaseExpExt) / float(valorDolar),
                'precioBaseOptExt': float(dato.precioBaseOptExt) / float(valorDolar),
                'totalExpExt': float(dato.totalExpExt) / float(valorDolar),
                'totalOptExt': float(dato.totalOptExt) / float(valorDolar),
            })

    contact = ContactoCotizacion.objects.filter(idcotizacion_id=pkC)
    cont = SerializerContactoCotizacion(contact, many=True)
        
    catServ = ClaveProdServ.objects.filter(clave_prodserv=coti.data[0]['idclasificacion']) 
    cServ = ClaveProdServSerializer(catServ, many=True)

    nombre = "Cotizacion-"+coti.data[0]['folioConsecutivo']+".pdf"

    html = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'ContactoCotizacion': cont.data, 'clasif':cServ.data }) 
    name_file = "cotizaciones/templates/pdf/"+nombre

    result_file = open(name_file, "w+b")

    pisa_status = pisa.CreatePDF(html,dest=result_file)

    result_file.close()

    with open(name_file, "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename=str(nombre))
    mensaje.attach(attach)

    try:
        # Envía el correo
        mailServer.sendmail('infor@mx-interland.com', email_to, mensaje.as_string())

        resp = True

        mailServer.quit()

    except SMTPException as e:
        # Maneja la excepción
        resp = e

    os.unlink(name_file)
    return Response({"msg":resp})

@csrf_exempt 
@api_view(['POST', 'GET'])
def folioServicio(request):  

    id = request.data.get('id')

    serv = ServicioCotizacion.objects.values('folioConsecutivo').filter(idVenta=id)
    ser = SerializerServicioCotizacion(serv, many=True)

    return Response(ser.data)

@csrf_exempt 
@api_view(['POST', 'GET'])
def editarServicios(request):  

    data = request.data.get('data')
    con = request.data.get('consecutivo')
    servicios = []

    idCotiza = 0

    for dato in data:

        servicios.append(dato)
    
    for serv in servicios:

        eliminar=serv['eliminar']
        if eliminar == 0:
            id = serv['id']
        else:
            id = 0
        idService = serv['idService']
        nameService=serv['nameService']
        priceService=serv['priceService']
        idcotizacion_id=serv['idcotizacion']
        idCotiza = serv['idcotizacion']
        ajusteTotal=serv['ajusteTotal']
        ajusteVenta=serv['ajusteVenta']
        porcentaje=serv['porcentaje']
        agregado=serv['agregado']
        idVenta=serv['idVenta']
        divisa=serv['divisa']
        iva=serv['iva']
        porcentajeVenta=serv['porcentajeVenta']
        porcentajeXpress=serv['porcentajeXpress']
        retencion = serv['retencion']
        subtotal=serv['subtotal']
        total= serv['total']
        basePorcExp=serv['basePorcExp']
        basePorcOpt=serv['basePorcOpt']
        monedaExpExt=serv['monedaExpExt']
        monedaOptExt=serv['monedaOptExt']
        porcentajeBaseExpExt=serv['porcentajeBaseExpExt']
        porcentajeBaseOptExt=serv['porcentajeBaseOptExt']
        porcentajeExtra=serv['porcentajeExtra']
        porcentajeIvaExp=serv['porcentajeIvaExp']
        porcentajeIvaOpt=serv['porcentajeIvaOpt']
        precioBaseExpExt=serv['precioBaseExpExt']
        precioBaseOptExt=serv['precioBaseOptExt']
        totalExpExt=serv['totalExpExt']
        totalOptExt=serv['totalOptExt'] 

        if con == 0:

            if eliminar == 0:
                
                serv = ServiciosAgregadosCotizacion.objects.get(id=id)
                
                serv.idService=idService
                serv.nameService=nameService
                serv.priceService=priceService
                serv.idcotizacion_id=idcotizacion_id
                serv.ajusteTotal=ajusteTotal
                serv.ajusteVenta=ajusteVenta
                serv.porcentaje=porcentaje
                serv.agregado=agregado
                serv.idVenta=idVenta
                serv.divisa=divisa
                serv.iva=iva
                serv.porcentajeVenta=porcentajeVenta
                serv.porcentajeXpress=porcentajeXpress
                serv.retencion = retencion
                serv.subtotal=subtotal
                serv.total= total
                serv.basePorcExp=basePorcExp
                serv.basePorcOpt=basePorcOpt
                serv.monedaExpExt=monedaExpExt
                serv.monedaOptExt=monedaOptExt
                serv.porcentajeBaseExpExt=porcentajeBaseExpExt
                serv.porcentajeBaseOptExt=porcentajeBaseOptExt
                serv.porcentajeExtra=porcentajeExtra
                serv.porcentajeIvaExp=porcentajeIvaExp
                serv.porcentajeIvaOpt=porcentajeIvaOpt
                serv.precioBaseExpExt=precioBaseExpExt
                serv.precioBaseOptExt=precioBaseOptExt
                serv.totalExpExt=totalExpExt
                serv.totalOptExt=totalOptExt

                serv.save()
            
            elif eliminar == 1:
                nuevoServ = ServiciosAgregadosCotizacion.objects.create(
                    idService=idService,
                    nameService=nameService,
                    priceService=priceService,
                    idcotizacion_id=idcotizacion_id,
                    ajusteTotal=ajusteTotal,
                    ajusteVenta=ajusteVenta,
                    porcentaje=porcentaje,
                    agregado=agregado,
                    idVenta=idVenta,
                    divisa=divisa,
                    iva=iva,
                    porcentajeVenta=porcentajeVenta,
                    porcentajeXpress=porcentajeXpress,
                    retencion = retencion,
                    subtotal=subtotal,
                    total= total,
                    basePorcExp=basePorcExp,
                    basePorcOpt=basePorcOpt,
                    monedaExpExt=monedaExpExt,
                    monedaOptExt=monedaOptExt,
                    porcentajeBaseExpExt=porcentajeBaseExpExt,
                    porcentajeBaseOptExt=porcentajeBaseOptExt,
                    porcentajeExtra=porcentajeExtra,
                    porcentajeIvaExp=porcentajeIvaExp,
                    porcentajeIvaOpt=porcentajeIvaOpt,
                    precioBaseExpExt=precioBaseExpExt,
                    precioBaseOptExt=precioBaseOptExt,
                    totalExpExt=totalExpExt,
                    totalOptExt=totalOptExt)

                serializer = SerializerServiciosAgregadosCotizacion(nuevoServ)
            
            cotizacion = ServicioCotizacion.objects.get(id=idCotiza)
            cotizacion.primerCambio = 1
            cotizacion.save()

        elif con == 1: 

            if eliminar == 0:
                
                serv = ServiciosAgregadosCotizacion.objects.get(id=id)
                
                serv.idService=idService
                serv.nameService=nameService
                serv.priceService=priceService
                serv.idcotizacion_id=idcotizacion_id
                serv.ajusteTotal=ajusteTotal
                serv.ajusteVenta=ajusteVenta
                serv.porcentaje=porcentaje
                serv.agregado=agregado
                serv.idVenta=idVenta
                serv.divisa=divisa
                serv.iva=iva
                serv.porcentajeVenta=porcentajeVenta
                serv.porcentajeXpress=porcentajeXpress
                serv.retencion = retencion
                serv.subtotal=subtotal
                serv.total= total
                serv.basePorcExp=basePorcExp
                serv.basePorcOpt=basePorcOpt
                serv.monedaExpExt=monedaExpExt
                serv.monedaOptExt=monedaOptExt
                serv.porcentajeBaseExpExt=porcentajeBaseExpExt
                serv.porcentajeBaseOptExt=porcentajeBaseOptExt
                serv.porcentajeExtra=porcentajeExtra
                serv.porcentajeIvaExp=porcentajeIvaExp
                serv.porcentajeIvaOpt=porcentajeIvaOpt
                serv.precioBaseExpExt=precioBaseExpExt
                serv.precioBaseOptExt=precioBaseOptExt
                serv.totalExpExt=totalExpExt
                serv.totalOptExt=totalOptExt

                serv.save()
            
            elif eliminar == 1:
                nuevoServ = ServiciosAgregadosCotizacion.objects.create(
                    idService=idService,
                    nameService=nameService,
                    priceService=priceService,
                    idcotizacion_id=idcotizacion_id,
                    ajusteTotal=ajusteTotal,
                    ajusteVenta=ajusteVenta,
                    porcentaje=porcentaje,
                    agregado=agregado,
                    idVenta=idVenta,
                    divisa=divisa,
                    iva=iva,
                    porcentajeVenta=porcentajeVenta,
                    porcentajeXpress=porcentajeXpress,
                    retencion = retencion,
                    subtotal=subtotal,
                    total= total,
                    basePorcExp=basePorcExp,
                    basePorcOpt=basePorcOpt,
                    monedaExpExt=monedaExpExt,
                    monedaOptExt=monedaOptExt,
                    porcentajeBaseExpExt=porcentajeBaseExpExt,
                    porcentajeBaseOptExt=porcentajeBaseOptExt,
                    porcentajeExtra=porcentajeExtra,
                    porcentajeIvaExp=porcentajeIvaExp,
                    porcentajeIvaOpt=porcentajeIvaOpt,
                    precioBaseExpExt=precioBaseExpExt,
                    precioBaseOptExt=precioBaseOptExt,
                    totalExpExt=totalExpExt,
                    totalOptExt=totalOptExt)

                serializer = SerializerServiciosAgregadosCotizacion(nuevoServ)

    busqueda = ServicioCotizacion.objects.values('cambiosConsecutivo').filter(id=idCotiza)
        
    busqueda = int(busqueda[0]['cambiosConsecutivo']) + 1

    conse = ServicioCotizacion.objects.get(id=idCotiza)
    conse.cambiosConsecutivo = busqueda
    conse.save()
    
    return Response(True)

