import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from cotizaciones.models import ServicioCotizacion, ServiciosAgregadosCotizacion, ContactoCotizacion
from cotizaciones.serializers import SerializerServicioCotizacion, SerializerServiciosAgregadosCotizacion, SerializerContactoCotizacion, FiltroServicioCotizacion

from django.http.response import Http404
from django.shortcuts import render
from .models import ServicioVenta
from .serializers import SerializerServicioVenta,FiltroServiceSerializer

from catalogos.models import ClaveProdServ
from catalogos.serializers import ClaveProdServSerializer

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models.query_utils import Q
from django.db.models import OuterRef, Subquery
from django.template.loader import render_to_string

from administracion.models import EmailDatos
from administracion.serializers import EmailDatosSerializer

# Create your views here.
class ServicioVentas(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServicioVenta.objects.all()
    serializer_class = SerializerServicioVenta


@csrf_exempt 
@api_view(['GET'])
def ListServiceFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        datosRes = []

        fecha = datetime.datetime.now()
        fecha : fecha.strptime(fecha, '%Y-%m-%d %H:%M:%S')

        if (palabra == ""):
            #goodslist=ServicioVenta.objects.filter(estatusCompleto=0)[data_start:data_end]
            #goodslist=ServicioVenta.objects.extra(select={'folioCotiza': 'select "folioConsecutivo" from "cotizaciones_serviciocotizacion" where "cotizaciones_serviciocotizacion"."idVenta" = 271'},).order_by('id').filter(estatusCompleto=0)[data_start:data_end]

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.all().filter(estatusCompleto=0).filter(dateCreate__lte=fecha).filter(dateFin__gte=fecha).filter(dateFin__isnull=False).annotate(folCon=Subquery(coti.values('folioConsecutivo')))[data_start:data_end]

            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })
            

            count=goodslist.count()
        else:   
            palabra_min=palabra.lower()
            palabra_may=palabra.upper()
            #goodslist = ServicioVenta.objects.order_by('id').filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=0)[data_start:data_end]
            #count=ServicioVenta.objects.filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=0)[data_start:data_end].count()
        
            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=0).filter(dateCreate__lte=fecha).filter(dateFin__gte=fecha).filter(dateFin__isnull=False).annotate(folCon=Subquery(coti.values('folioConsecutivo'))).order_by('id')[data_start:data_end]

            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })

            count = goodslist.count()
        #goods_ser=FiltroServiceSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data': datosRes, #goods_ser.data,
        })

@csrf_exempt 
@api_view(['GET'])
def ListServiceFiltroIncompleto(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        datosRes = []

        fecha = datetime.datetime.now()
        fecha : fecha.strptime(fecha, '%Y-%m-%d %H:%M:%S')

        if (palabra == ""): 
            #goodslist = ServicioVenta.objects.order_by('id').filter(estatusCompleto=3)[data_start:data_end]
            #count=ServicioVenta.objects.filter(estatusCompleto=3).count()

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.all().filter(estatusCompleto=3).filter(dateCreate__lte=fecha).filter(dateFin__isnull=True).annotate(folCon=Subquery(coti.values('folioConsecutivo')))[data_start:data_end]

            
            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })

            count=goodslist.count()
        else:
            #goodslist = ServicioVenta.objects.objects.order_by('id').filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=3)[data_start:data_end]

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=3).filter(dateCreate__lte=fecha).filter(dateFin__isnull=True).annotate(folCon=Subquery(coti.values('folioConsecutivo'))).order_by('id')[data_start:data_end]

            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })


            count=goodslist.count()

        #goods_ser=FiltroServiceSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data': datosRes,#goods_ser.data
        })

@csrf_exempt 
@api_view(['GET'])
def ListServiceFiltroExpirados(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        datosRes = []

        fecha = datetime.datetime.now()
        fecha : fecha.strptime(fecha, '%Y-%m-%d %H:%M:%S')

        if (palabra == ""): 
            #goodslist = ServicioVenta.objects.order_by('id').filter(estatusCompleto=3)[data_start:data_end]
            #count=ServicioVenta.objects.filter(estatusCompleto=3).count()

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.all().filter(estatusCompleto=0).filter(dateFin__lte=fecha).filter(dateFin__isnull=False).annotate(folCon=Subquery(coti.values('folioConsecutivo')))[data_start:data_end]

            
            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })

            count=goodslist.count()
        else:
            #goodslist = ServicioVenta.objects.objects.order_by('id').filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=3)[data_start:data_end]

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=0).filter(dateFin__lte=fecha).filter(dateFin__isnull=False).annotate(folCon=Subquery(coti.values('folioConsecutivo'))).order_by('id')[data_start:data_end]

            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })


            count=goodslist.count()

        #goods_ser=FiltroServiceSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data': datosRes,#goods_ser.data
        })

@csrf_exempt 
@api_view(['GET'])
def ListServiceFiltroNoContestados(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        datosRes = []

        if (palabra == ""): 
            #goodslist = ServicioVenta.objects.order_by('id').filter(estatusCompleto=3)[data_start:data_end]
            #count=ServicioVenta.objects.filter(estatusCompleto=3).count()

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.all().filter(estatusCompleto=4).annotate(folCon=Subquery(coti.values('folioConsecutivo')))[data_start:data_end]

            
            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })

            count=goodslist.count()
        else:
            #goodslist = ServicioVenta.objects.objects.order_by('id').filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=3)[data_start:data_end]

            coti = ServicioCotizacion.objects.filter(idVenta=OuterRef('idCotizacion')).values('folioConsecutivo')
            goodslist = ServicioVenta.objects.filter(Q(servicio__icontains=palabra) | Q(servicio__icontains=palabra)).filter(estatusCompleto=4).annotate(folCon=Subquery(coti.values('folioConsecutivo'))).order_by('id')[data_start:data_end]

            for dato in goodslist:
                datosRes.append({
                    'folioConsecutivo':dato.folCon,
                    'banCOntesto': dato.banCOntesto,
                    'checkVentas': dato.checkVentas,
                    'ciudadDestino': dato.ciudadDestino,
                    'ciudadOrigen': dato.ciudadOrigen,
                    'classHazmat': dato.classHazmat,
                    'cpDestino': dato.cpDestino,
                    'cpOrigen': dato.cpOrigen,
                    'dateCreate': dato.dateCreate,
                    'dateFin': dato.dateFin,
                    'dateInicio': dato.dateInicio,
                    'diasTransito': dato.diasTransito,
                    'divisa': dato.divisa,
                    'estadoDestino': dato.estadoDestino,
                    'estadoOrigen': dato.estadoOrigen,
                    'estatusCompleto': dato.estatusCompleto,
                    'fechaPricing': dato.fechaPricing,
                    'id': dato.id,
                    'idAduana': dato.idAduana,
                    'idCotizacion': dato.idCotizacion,
                    'idProveedor': dato.idProveedor,
                    'idServicio': dato.idServicio,
                    'idestadoDestino': dato.idestadoDestino,
                    'idestadoOrigen': dato.idestadoOrigen,
                    'idpaisDestino': dato.idpaisDestino,
                    'idpaisOrigen': dato.idpaisOrigen,
                    'iva': dato.iva,
                    'modality': dato.modality,
                    'nota': dato.nota,
                    'paisDestino': dato.paisDestino,
                    'paisOrigen': dato.paisOrigen,
                    'porcentajeVenta': dato.porcentajeVenta,
                    'porcentajeXpress': dato.porcentajeXpress,
                    'proveedor': dato.proveedor,
                    'retencion': dato.retencion,
                    'ruta': dato.ruta,
                    'servicio': dato.servicio,
                    'subtotal': dato.subtotal,
                    'tipoOperacion': dato.tipoOperacion,
                    'tipoServicio': dato.tipoServicio,
                    #'tipoUnidad': dato.tipoUnidad,
                    'total': dato.total,
                    'unHazmat': dato.unHazmat,
                    'unidaModality': dato.unidaModality,
                    'userCreate': dato.userCreate,
                    'valorMercancia': dato.valorMercancia,
                    'velocidadEnvio': dato.velocidadEnvio,
                    'zona':dato.zona
                })


            count=goodslist.count()

        #goods_ser=FiltroServiceSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data': datosRes,#goods_ser.data
        })

#agregado
@csrf_exempt 
@api_view(['GET'])
def ListService(request):       
    goodslist=ServicioVenta.objects.all()
    goods_ser=FiltroServiceSerializer(goodslist,many=True)
    return Response(goods_ser.data)


class ServiceSaleDetail(APIView):    
    
    def get_object(self, idServicio):
        try:
            return ServicioVenta.objects.get(id=idServicio)
        except ServicioVenta.DoesNotExist:
            return Http404
    
    def get(self, request, idServicio, format=None):
        
        servicio = self.get_object(idServicio)
        serializer = SerializerServicioVenta(servicio)
        return Response(serializer.data)

@csrf_exempt 
@api_view(['POST'])
def ConsultarCotizacionAgregada(request):
    
    venta = request.data.get('idVenta')

    if venta:
        buscarServicios = ServicioCotizacion.objects.filter(idVenta=venta)
        # red = str(buscarServicios.query)
        # print (red)
        serializer = SerializerServicioCotizacion(buscarServicios, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST'])
def ConsultarServiciosAgregados(request):
    
    venta = request.data.get('idVenta')

    if venta:
        buscarServicios = ServiciosAgregadosCotizacion.objects.filter(idVenta=venta)
        # red = str(buscarServicios.query)
        # print (red)
        serializer = SerializerServiciosAgregadosCotizacion(buscarServicios, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST'])
def ConsultarServiciosAgregar(request):
    
    servicio = request.data.get('data')

    fecha = datetime.datetime.now()
    fecha : fecha.strptime(fecha, '%Y-%m-%d %H:%M:%S')

    buscarServicios = ServicioVenta.objects.filter(servicio=servicio).filter(dateFin__gte=fecha)
    serializer = SerializerServicioVenta(buscarServicios, many=True)
    
    return Response(serializer.data)

@csrf_exempt 
@api_view(['POST', 'GET'])
def emailNuevoServicio(request):

    pkC = request.data.get('idcotizacion')
    folio = request.data.get('folio')
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
    email_to='daniel.gomez@interland.business'
    #email_to='ismael.martinez@interland.business'

    mensaje['From']= correoInt
    mensaje['To']=email_to
    mensaje['Subject'] = "Solicitud de Cotización"

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
                'priceService': dato.priceService,
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
                'priceService': dato.priceService,
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


    content = render_to_string('pdf/correoNuevoServicio.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'ContactoCotizacion': cont.data, 'clasif':cServ.data })
    mensaje.attach(MIMEText(content,'html'))

    try:
        # Envía el correo
        mailServer.sendmail('infor@mx-interland.com', email_to, mensaje.as_string())

        resp = True

        mailServer.quit()

    except smtplib.SMTPException as e:
        # Maneja la excepción
        resp = e

    return Response(resp)

@csrf_exempt 
@api_view(['POST', 'GET'])
def cerrarServicio(request):

    pkC = int(request.data.get('id'))
    motivo = request.data.get('motivo')

    if pkC > 0:
        ser = ServicioVenta.objects.get(id=pkC)
        ser.nota = motivo
        ser.estatusCompleto = 4
        ser.save()
        return Response(True)
    else:
        return Response(False)