from difflib import context_diff
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import json
import locale
from click import Context
from requests import Request

import requests 
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
from django.db.models import Sum, OuterRef, Subquery, Max
from django.db.models.functions import RowNumber
from django.db import connection

from collections import namedtuple

#Generar PDF Librerias Necesarias Agregado David
import os
from django.views.generic import ListView, View 
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import context, pisa
from django.contrib.staticfiles import finders
#Fin Librerias PDF Necesarias

import smtplib
from smtplib import SMTPException, SMTPSenderRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.conf import settings

from datetime import datetime, date
from django.utils import timezone

from servicioVenta.serializers import ServicioVenta
from servicios.views import ServicesViewSet 
from servicios.serializers import ServicesSerializer
from cotizaciones.models import Mercancias, Planes, TarifasFTL
from cotizaciones.serializers import SerializerMercancias, SerializerPlanes
from .models import ServicioCotizacion, ContactoCotizacion, ServiciosAgregadosCotizacion, Consecutivo, Rutas, Tarifario, DireccionCotizacion
from .serializers import FiltroServicioCotizacion, SerializerServicioCotizacion, SerializerContactoCotizacion, SerializerServiciosAgregadosCotizacion, SerializerConsecutivo, SerializerRutas, SerializerTarifario, SerializerTarifasFTL, SerializerDireccionCotizacion
from catalogos.models import ClaveProdServ, Terminos_Condiciones, Geocercas, UnitBox
from catalogos.serializers import ClaveProdServSerializer, TerminosCondicionesSerializer, GeocercasSerializer, UnitBoxSerializer
from administracion.models import EmailDatos
from administracion.serializers import EmailDatosSerializer

from customer.models import ZonasHijos
from customer.serializers import ZonasHijosSerializer

from chatboot.models import leds_chatboot, numeros_ejecutivos_chatboot
from chatboot.serializers import LedsSerializer, NumerosSerializer
from chatboot.views import envia_mensajes

from inland_django.utils import compress_and_encode_image


class ServicioCotizaciones(viewsets.ModelViewSet):
    queryset = ServicioCotizacion.objects.all()
    serializer_class = SerializerServicioCotizacion

class ServiciosAgregadosCotizaciones(viewsets.ModelViewSet):
    queryset = ServiciosAgregadosCotizacion.objects.all()
    serializer_class = SerializerServiciosAgregadosCotizacion

class ContactoCotizaciones(viewsets.ModelViewSet):
    queryset = ContactoCotizacion.objects.all()
    serializer_class = SerializerContactoCotizacion

class MercanciasCotizaciones(viewsets.ModelViewSet):
    queryset = Mercancias.objects.all()
    serializer_class = SerializerMercancias

class PlanesCotizaciones(viewsets.ModelViewSet):
    queryset = Planes.objects.all()
    serializer_class = SerializerPlanes

class DireccionCotizaciones(viewsets.ModelViewSet):
    queryset = DireccionCotizacion.objects.all()
    serializer_class = SerializerDireccionCotizacion

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

'''@csrf_exempt 
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
    modalidad = request.data.get('modalidad')
    tarifaKilometro = 0

    #SE VALIDA LA EXISTENCIA DE LOS CODIGOS POSTALES EN LA TABLA DE ZONAS

    existeOrigen = ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri).exists()
    existeDestino = ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes).exists()

    if existeOrigen and existeDestino:
        idorigenE = ZonasHijos.objects.filter(codigoPostal=cpOrigen).filter(colonia=coloniaOri)
        idorigenESer = ZonasHijosSerializer(idorigenE, many=True)

        idOrigen = idorigenESer.data[0]['idZonasHijo']

        iddestinoE = ZonasHijos.objects.filter(codigoPostal=cpDestino).filter(colonia=coloniaDes)
        iddestinoESer = ZonasHijosSerializer(iddestinoE, many=True)

        idDestino = iddestinoESer.data[0]['idZonasHijo']

        existeTarifa = Tarifas.objects.filter(idTarifasOrigen_id=idOrigen).filter(idTarifasDestino_id=idDestino).filter(tipoUnidad=tipoUnidad).exists()
        
        if existeTarifa:
            datosTarifa = Tarifas.objects.filter(idTarifasOrigen_id=idOrigen).filter(idTarifasDestino_id=idDestino).filter(tipoUnidad=tipoUnidad)
            datosTarSer = SerializerTarifas(datosTarifa, many=True)
            return Response(datosTarSer.data)
        else:

            if modalidad == 'FTL': 
                if tipoUnidad == 4: #CAJA DE 53 
                    tarifaKilometro = 95.00
                elif tipoUnidad == 5: #CAJA DE 48
                    tarifaKilometro = 64.00
                elif tipoUnidad == 13: #TORTON
                    tarifaKilometro = 60.00
                elif tipoUnidad == 3: #RABON
                    tarifaKilometro = 55.00
                elif tipoUnidad == 2: #3 1/2
                    tarifaKilometro = 43.00
                elif tipoUnidad == 1: #3 1/2 PICK UPS
                    tarifaKilometro = 33.00
                else:
                    tarifaKilometro = 64.00

            if modalidad == 'FCL':
                if tipoUnidad == 9: #PATAFORMA DE 4 
                    tarifaKilometro = 70.00
                elif tipoUnidad == 6: #CAJA DE 48
                    tarifaKilometro = 100.00

            datosTarifa = Tarifas.objects.create(
                idTarifasOrigen_id = idOrigen ,
                idTarifasDestino_id = idDestino,
                tarifaKilometro = tarifaKilometro,
                estatus = 1,
                tipoUnidad = tipoUnidad,
                dateCreate = datetime.now(),
            )
            datosTarifa = Tarifas.objects.filter(idTarifasOrigen_id=idOrigen).filter(idTarifasDestino_id=idDestino).filter(tipoUnidad=tipoUnidad)
            datosTarSer = SerializerTarifas(datosTarifa, many=True)
            return Response(datosTarSer.data)
    else:
        return Response([{"existeOrigen": existeOrigen, "existeDestino": existeDestino}])'''

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
    modalidad = request.data.get('modalidad')
    tarifaKilometro = 0

    datosTarSer = {}

    #SE VALIDA LA EXISTENCIA DE LOS CODIGOS POSTALES EN LA TABLA DE TARIFAS FTL

    existeTarifa = TarifasFTL.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(tipo_unidad=tipoUnidad).filter(tipo_unidad=tipoUnidad).exists()

    if existeTarifa:
        datosTarifa = TarifasFTL.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(tipo_unidad=tipoUnidad)
        datosTarSer = SerializerTarifasFTL(datosTarifa, many=True)
        
        
    else:

        if modalidad == 'FTL': 
            if tipoUnidad == 5: #CAJA DE 53 
                tarifaKilometro = 79.2
            elif tipoUnidad == 4: #CAJA DE 48
                tarifaKilometro = 79.2
            elif tipoUnidad == 13: #TORTON
                tarifaKilometro = 63.00
            elif tipoUnidad == 3: #RABON
                tarifaKilometro = 57.2
            elif tipoUnidad == 2: #3.5
                tarifaKilometro = 52.8
            elif tipoUnidad == 1: #PICK UPS
                tarifaKilometro = 46.00


        if modalidad == 'FCL':
            if tipoUnidad == 9: #SENCILLO 
                tarifaKilometro = 126.3
            elif tipoUnidad == 6: #FULL / DOBLE REMOLQUE
                tarifaKilometro = 126.3

        datosTarifa = TarifasFTL.objects.create(
            tarifa_kilometro = tarifaKilometro,
            estatus	= 1,
            pais_origen = paisOri,
            estado_origen = estadoOri,
            ciudad_origen = ciudadOri,
            cp_origen = cpOrigen,
            pais_destino = paisDes,
            estado_destino = estadoDes,
            ciudad_destino = ciudadDes,
            cp_destino = cpDestino,
            tipo_unidad = tipoUnidad,
            date_create = datetime.now()
        )
        
    datosTarifa = TarifasFTL.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(tipo_unidad=tipoUnidad)
    datosTarSer = SerializerTarifasFTL(datosTarifa, many=True)
    return Response(datosTarSer.data)
        #return Response([{"existeOrigen": existeOrigen, "existeDestino": existeDestino}])

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
    termodalidad = request.data.get('termodalidad')

    existeRuta = Rutas.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(modalidad=termodalidad).exists()
    
    if existeRuta:
        datosRuta = Rutas.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(modalidad=termodalidad)
        datosRutSer = SerializerRutas(datosRuta, many=True)
        return Response(datosRutSer.data)
    else:
        
        origen = paisOri+", "+cpOrigen+", "+estadoOri+", "+ciudadOri
        
        destino = paisDes+", "+cpDestino+", "+estadoDes+", "+ciudadDes
        
        params = {
                    "destinations": destino,
                    "origins": origen,
                    "units": "metric",
                    "key": "AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y"
                } 
        
        response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params)
        
        data = json.loads(response.text)
        km = str(data['rows'][0]['elements'][0]['distance']['text'])
        
        if km:
            tiempo = str(data['rows'][0]['elements'][0]['duration']['text'])
            km = km.replace("km", "")
            km = km.strip()
            km = float(km)
            
            if km > 0:
                datosRuta = Rutas.objects.create(
                kilometraje = km,
                porc_zona_no_com = 15,
                porc_zona_pelig = 15,
                date_create = datetime.now(),
                tiempo_estimado = tiempo,
                pais_origen = paisOri,
                estado_origen = estadoOri,
                ciudad_origen = ciudadOri,
                cp_origen = cpOrigen,
                pais_destino = paisDes,
                estado_destino = estadoDes,
                ciudad_destino = ciudadDes,
                cp_destino = cpDestino,
                modalidad = termodalidad,
                
            )

        
        datosRuta = Rutas.objects.filter(pais_origen=paisOri).filter(estado_origen=estadoOri).filter(ciudad_origen=ciudadOri).filter(cp_origen=cpOrigen).filter(pais_destino=paisDes).filter(estado_destino=estadoDes).filter(ciudad_destino=ciudadDes).filter(cp_destino=cpDestino).filter(modalidad=termodalidad)
        datosRutSer = SerializerRutas(datosRuta, many=True)
        return Response(datosRutSer.data)


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
                goodslist = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).filter(Q(usuarioGenera = user)).count()
        else:
            if user == 'admin':
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).count()
            else:
                goodslist = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folioConsecutivo__icontains=palabra) | Q(tipoEnvio__icontains=palabra) | Q(modoEnvio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).filter(Q(usuarioGenera = user))[data_start:data_end]
                count = ServicioCotizacion.objects.filter(Q(tipoServicio__icontains=palabra) | Q(folio__icontains=palabra)).filter(dateCreate__year=str(year), dateCreate__month=str(month), dateCreate__day=str(day)).filter(Q(estatus = 0) | Q(estatus = 4)).filter(Q(usuarioGenera = user)).count()

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
                subquery = Mercancias.objects.filter(
                    idCotizacion=OuterRef('id')
                ).values('idCotizacion').annotate(
                    total_peso=Sum('pesoVolumetricoTotal')
                ).values('total_peso')[:1]

                # Consulta principal para obtener las cotizaciones
                goodslist = ServicioCotizacion.objects.filter(
                    estatus=0,
                    dateCreate__lt=fecha
                ).annotate(
                    total_peso=Subquery(subquery)
                ).values('tipoServicio', 'tipoEnvio', 'modoEnvio', 'paisOrigen', 'idpaisOrigen', 'cpOrigen', 'estadoOrigen', 'idestadoOrigen', 'ciudadOrigen', 'calleOrigen', 'numExtOrigen', 'numIntOrigen', 'almacenOcurreOrigen', 'paisDestino', 'idpaisDestino', 'cpDestino', 'estadoDestino', 'idestadoDestino', 'ciudadDestino', 'calleDestino', 'numExtDestino', 'numIntDestino', 'almacenOcurreDestino', 'dateCreate', 'fechaCarga', 'tipoOperacion', 'tipoCarga', 'tipoUnidad', 'precioTotalInicial', 'precioTotalFinal', 'divisaInicial', 'divisaFinal', 'serie', 'folio', 'estatus', 'usuario', 'rechazo', 'idVenta', 'diasTransito', 'estibable', 'nametipoUnidad', 'folioConsecutivo', 'gradosRef', 'tipoUnidadRef', 'unHaz', 'classHaz', 'embalaje', 'idclasificacion', 'cantidad', 'largo', 'alto', 'ancho', 'volumen', 'pesoTotal', 'unidadMedida', 'unidadPeso', 'descrip', 'velocidadEnvio', 'zona', 'cambiosConsecutivo', 'primerCambio', 'valorDeclaradoMerc', 'usuarioGenera', 'total_peso')
                #goodslist = ServicioCotizacion.objects.filter(Q(estatus=0)).filter(dateCreate__lt=fecha)[data_start:data_end]
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

        #goods_ser=FiltroServicioCotizacion(goodslist,many=True)

        return Response({
            'total':count,
            'data':goodslist
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
        merchGlob = []
        servGlob = []

        cantidad = 0
        volTot = 0
        pesoVol = 0
        pesoTot = 0

        susbtotalGlob = 0
        porcIvaGlob = 0
        totalServicioGlob = 0
        # ids=3

        # context = {
        #     'icon': '{}{}'.format(settings.STATIC_URL, '/media/img/logo_i.png')
        # }
        
        cotiza = ServicioCotizacion.objects.filter(id=ids)
        coti = FiltroServicioCotizacion(cotiza, many=True)

        divisa = int(coti.data[0]['divisaFinal'])
        tipoOp = str(coti.data[0]['tipoOperacion'])
        valorDolar = 19.8532

        service = ServiciosAgregadosCotizacion.objects.filter(idcotizacion_id=ids)
        serv = SerializerServiciosAgregadosCotizacion(service, many=True)

            
        if divisa == 2:
            for dato in service:

                susbtotalGlob = susbtotalGlob + float(dato.subtotal)
                porcIvaGlob = porcIvaGlob + float(dato.porcIva)
                totalServicioGlob = totalServicioGlob + float(dato.totalServicio)

                subtotal = float(dato.subtotal)
                subtotal = "{:,.2f}".format(subtotal)
                porcIva = float(dato.porcIva)
                porcIva = "{:,.2f}".format(porcIva)
                totalServicio = float(dato.totalServicio)
                totalServicio = "{:,.2f}".format(totalServicio)

                servRes.append({
                    'id': dato.id,
                    'idService': dato.idService,
                    'nameService': dato.nameService,
                    'susbtotal': subtotal,
                    'kilometraje': float(dato.kilometraje),
                    'porcIva': porcIva,
                    'porcNComercial': float(dato.porcNComercial),
                    'porcSobrepeso': float(dato.porcSobrepeso),
                    'porcSusceptible': float(dato.porcSusceptible),
                    'porcZPeligrosa': float(dato.porcZPeligrosa),
                    'tarifaKilometraje': float(dato.tarifaKilometraje),
                    'totalServicio': totalServicio,
                })

            susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
            porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
            totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

            servGlob.append({
                'susbtotalGlob': susbtotalGlob,
                'porcIvaGlob': porcIvaGlob,
                'totalServicioGlob': totalServicioGlob,
            })
        else:
            for dato in service:

                susbtotalGlob = susbtotalGlob + round((float(dato.subtotal) / valorDolar), 2)
                porcIvaGlob = porcIvaGlob + round((float(dato.porcIva) / valorDolar), 2)
                totalServicioGlob = totalServicioGlob + round((float(dato.totalServicio) / valorDolar), 2)

                subtotal = round((float(dato.subtotal) / valorDolar), 2)
                subtotal = "{:,.2f}".format(subtotal)
                porcIva = round((float(dato.porcIva) / valorDolar), 2)
                porcIva = "{:,.2f}".format(porcIva)
                totalServicio = round((float(dato.totalServicio) / valorDolar), 2)
                totalServicio = "{:,.2f}".format(totalServicio)

                servRes.append({
                    'id': dato.id,
                    'idService': dato.idService,
                    'nameService': dato.nameService,
                    'susbtotal': subtotal,
                    'kilometraje': round((float(dato.kilometraje) / valorDolar), 2),
                    'porcIva': porcIva,
                    'porcNComercial': round((float(dato.porcNComercial) / valorDolar), 2),
                    'porcSobrepeso': round((float(dato.porcSobrepeso) / valorDolar), 2),
                    'porcSusceptible': round((float(dato.porcSusceptible) / valorDolar), 2),
                    'porcZPeligrosa': round((float(dato.porcZPeligrosa) / valorDolar), 2),
                    'tarifaKilometraje': round((float(dato.tarifaKilometraje) / valorDolar), 2),
                    'totalServicio': totalServicio,
                    
                })

            susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
            porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
            totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

            servGlob.append({
                'susbtotalGlob': susbtotalGlob,
                'porcIvaGlob': porcIvaGlob,
                'totalServicioGlob': totalServicioGlob,
            })

        contact = ContactoCotizacion.objects.filter(idcotizacion_id=ids)
        cont = SerializerContactoCotizacion(contact, many=True)

        catServ = ClaveProdServ.objects.filter(clave_prodserv=coti.data[0]['idclasificacion']) 
        cServ = ClaveProdServSerializer(catServ, many=True)

        merch = Mercancias.objects.filter(idCotizacion_id=ids)
        merc = SerializerMercancias(merch, many=True)

        cantitadad = 0
        volTot = 0
        pesoVol = 0
        pesoTot = 0

        for dato in merch:
        
            cantidad = cantidad + int(dato.cantidad)
            volTot = volTot + float(dato.volumenTotal)
            pesoVol = pesoVol + float(dato.pesoVolumetricoTotal)
            pesoTot = pesoTot + float(dato.pesoTotal)
        
        merchGlob.append({
            'cantidad': cantidad,
            'volTot': volTot,
            'pesoVol': pesoVol,
            'pesoTotal': pesoTot,
        })

        planes = Planes.objects.filter(idCotizacion_id=ids).order_by('orden')
        plan = SerializerPlanes(planes, many=True)

        terminos = Terminos_Condiciones.objects.filter(aplica__icontains=tipoOp).order_by('orden')
        term = TerminosCondicionesSerializer(terminos, many=True)

        img_cinta = compress_and_encode_image('cotizaciones/templates/img/Interland-cinta.png', 75)
        img_planes = compress_and_encode_image('cotizaciones/templates/img/delivery-truck.png', 75)
        img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)

        html = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'ServiciosAgregadosCotizacionGlobal': servGlob, 'ContactoCotizacion': cont.data, 'clasif':cServ.data, 'mercancias':  merc.data, 'mercanciasGlob':  merchGlob, "planes":plan.data, "imgCinta":img_cinta, "imgPlanes":img_planes, "imgLogo":img_logo, "disclamers":term.data})
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
    merchGlob = []
    servGlob = []

    cantidad = 0
    volTot = 0
    pesoVol = 0
    pesoTot = 0

    susbtotalGlob = 0
    porcIvaGlob = 0
    totalServicioGlob = 0
    # Establecemos conexion con el servidor smtp de gmail
    # mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    
    emailD = EmailDatos.objects.filter(idEmail=1)
    emailS = EmailDatosSerializer(emailD, many=True)

    correoInt = 'sisproyect@gmail.com' #emailS.data[0]['correo']
    contraInt = 'ntbl mrgu brvv qmiq' #emailS.data[0]['contra']
    hostInter = 'smtp.gmail.com' #emailS.data[0]['host']
    puerInter = 587 #emailS.data[0]['port']

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

    cotiza = ServicioCotizacion.objects.filter(id=pkC)
    coti = FiltroServicioCotizacion(cotiza, many=True)

    divisa = int(coti.data[0]['divisaFinal'])
    tipoOp = str(coti.data[0]['tipoOperacion'])
    valorDolar = 19.8532

    content = render_to_string('pdf/correoCotizacion.html', {'name': nombre_contacto, 'folioCotizacion': coti.data[0]['folioConsecutivo']})
    mensaje.attach(MIMEText(content,'html'))

    service = ServiciosAgregadosCotizacion.objects.filter(idcotizacion_id=pkC)
    serv = SerializerServiciosAgregadosCotizacion(service, many=True)

    if divisa == 2:
        for dato in service:

            susbtotalGlob = susbtotalGlob + float(dato.subtotal)
            porcIvaGlob = porcIvaGlob + float(dato.porcIva)
            totalServicioGlob = totalServicioGlob + float(dato.totalServicio)

            subtotal = float(dato.subtotal)
            subtotal = "{:,.2f}".format(subtotal)
            porcIva = float(dato.porcIva)
            porcIva = "{:,.2f}".format(porcIva)
            totalServicio = float(dato.totalServicio)
            totalServicio = "{:,.2f}".format(totalServicio)

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'susbtotal': subtotal,
                'kilometraje': float(dato.kilometraje),
                'porcIva': porcIva,
                'porcNComercial': float(dato.porcNComercial),
                'porcSobrepeso': float(dato.porcSobrepeso),
                'porcSusceptible': float(dato.porcSusceptible),
                'porcZPeligrosa': float(dato.porcZPeligrosa),
                'tarifaKilometraje': float(dato.tarifaKilometraje),
                'totalServicio': totalServicio,
            })
        
        susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
        porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
        totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

        servGlob.append({
            'susbtotalGlob': susbtotalGlob,
            'porcIvaGlob': porcIvaGlob,
            'totalServicioGlob': totalServicioGlob,
        })
    else:
        for dato in service:

            susbtotalGlob = susbtotalGlob + round((float(dato.subtotal) / valorDolar), 2)
            porcIvaGlob = porcIvaGlob + round((float(dato.porcIva) / valorDolar), 2)
            totalServicioGlob = totalServicioGlob + round((float(dato.totalServicio) / valorDolar), 2)

            subtotal = round((float(dato.subtotal) / valorDolar), 2)
            subtotal = "{:,.2f}".format(subtotal)
            porcIva = round((float(dato.porcIva) / valorDolar), 2)
            porcIva = "{:,.2f}".format(porcIva)
            totalServicio = round((float(dato.totalServicio) / valorDolar), 2)
            totalServicio = "{:,.2f}".format(totalServicio)

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'susbtotal': subtotal,
                'kilometraje': round((float(dato.kilometraje) / valorDolar), 2),
                'porcIva': porcIva,
                'porcNComercial': round((float(dato.porcNComercial) / valorDolar), 2),
                'porcSobrepeso': round((float(dato.porcSobrepeso) / valorDolar), 2),
                'porcSusceptible': round((float(dato.porcSusceptible) / valorDolar), 2),
                'porcZPeligrosa': round((float(dato.porcZPeligrosa) / valorDolar), 2),
                'tarifaKilometraje': round((float(dato.tarifaKilometraje) / valorDolar), 2),
                'totalServicio': totalServicio,
                    
            })

        susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
        porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
        totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

        servGlob.append({
            'susbtotalGlob': susbtotalGlob,
            'porcIvaGlob': porcIvaGlob,
            'totalServicioGlob': totalServicioGlob,
        })

    contact = ContactoCotizacion.objects.filter(idcotizacion_id=pkC)
    cont = SerializerContactoCotizacion(contact, many=True)

    merch = Mercancias.objects.filter(idCotizacion_id=pkC)
    merc = SerializerMercancias(merch, many=True)

    unidadElegida = UnitBox.objects.filter(id=coti.data[0]['id_unidad'])
    undidadEl = UnitBoxSerializer(unidadElegida, many=True)
    
    direcciones = DireccionCotizacion.objects.filter(idcotizacion_id=pkC).order_by('id')
    dir = SerializerDireccionCotizacion(direcciones, many=True)
    
    for dato in merch:
        
        cantidad = cantidad + int(dato.cantidad)
        volTot = volTot + float(dato.volumenTotal)
        pesoVol = pesoVol + float(dato.pesoVolumetricoTotal)
        pesoTot = pesoTot + float(dato.pesoTotal)
    
    merchGlob.append({
        'cantidad': cantidad,
        'volTot': volTot,
        'pesoVol': pesoVol,
        'pesoTotal': pesoTot,
    })

    planes = Planes.objects.filter(idCotizacion_id=pkC).order_by('orden')
    plan = SerializerPlanes(planes, many=True)

    terminos = Terminos_Condiciones.objects.filter(aplica__icontains=tipoOp).order_by('orden')
    term = TerminosCondicionesSerializer(terminos, many=True)

    img_cinta = compress_and_encode_image('cotizaciones/templates/img/Interland-cinta.png', 75)
    img_planes = compress_and_encode_image('cotizaciones/templates/img/delivery-truck.png', 75)
    img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)

    nombre = "Cotizacion-"+coti.data[0]['folioConsecutivo']+".pdf"

    html = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'direcciones':dir.data,'ServiciosAgregadosCotizacionGlobal': servGlob, 'ContactoCotizacion': cont.data, 'unidad':undidadEl.data, 'mercancias':  merc.data, 'mercanciasGlob':  merchGlob, "planes":plan.data, "imgCinta":img_cinta, "imgPlanes":img_planes, "imgLogo":img_logo, "disclamers":term.data}) 
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

        aumento=serv['aumento']
        id=serv['id']
        idService=serv['idService']
        idCotiza=serv['idcotizacion']
        iva=serv['iva']
        kilometraje=serv['kilometraje']
        nameService=serv['nombreSer']
        porcAumento=serv['porcAumento']
        porcIva=serv['porcIva']
        porcNComercial=serv['porcNComercial']
        porcSobrepeso=serv['porcSobrepeso']
        porcSusceptible=serv['porcSusceptible']
        porcZPeligrosa=serv['porcZPeligrosa']
        subtotal=serv['subtotal']
        tarifaKilometraje=serv['tarifaK']
        totalServicio=serv['totalServicio']

        if con == 0:

            if eliminar == 0:
                
                serv = ServiciosAgregadosCotizacion.objects.get(id=id)
                
                serv.aumento=aumento
                serv.iva=iva
                serv.kilometraje=kilometraje
                serv.nameService=nameService
                serv.porcAumento=porcAumento
                serv.porcIva=porcIva
                serv.porcNComercial=porcNComercial
                serv.porcSobrepeso=porcSobrepeso
                serv.porcSusceptible=porcSusceptible
                serv.porcZPeligrosa=porcZPeligrosa
                serv.subtotal=subtotal
                serv.tarifaKilometraje=tarifaKilometraje
                serv.totalServicio=totalServicio

                serv.save()
            
            elif eliminar == 1:
                nuevoServ = ServiciosAgregadosCotizacion.objects.create(
                    idService=idService,
                    nameService=nameService,
                    aumento=aumento,
                    iva=iva,
                    kilometraje=kilometraje,
                    porcAumento=porcAumento,
                    porcIva=porcIva,
                    porcNComercial=porcNComercial,
                    porcSobrepeso=porcSobrepeso,
                    porcSusceptible=porcSusceptible,
                    porcZPeligrosa=porcZPeligrosa,
                    subtotal=subtotal,
                    tarifaKilometraje=tarifaKilometraje,
                    totalServicio=totalServicio,
                    )

                serializer = SerializerServiciosAgregadosCotizacion(nuevoServ)
            
            cotizacion = ServicioCotizacion.objects.get(id=idCotiza)
            cotizacion.primerCambio = 1
            cotizacion.save()

        elif con == 1: 

            if eliminar == 0:
                
                serv = ServiciosAgregadosCotizacion.objects.get(id=id)
                
                serv.aumento=aumento
                serv.iva=iva
                serv.kilometraje=kilometraje
                serv.nameService=nameService
                serv.porcAumento=porcAumento
                serv.porcIva=porcIva
                serv.porcNComercial=porcNComercial
                serv.porcSobrepeso=porcSobrepeso
                serv.porcSusceptible=porcSusceptible
                serv.porcZPeligrosa=porcZPeligrosa
                serv.subtotal=subtotal
                serv.tarifaKilometraje=tarifaKilometraje
                serv.totalServicio=totalServicio

                serv.save()
            
            elif eliminar == 1:
                nuevoServ = ServiciosAgregadosCotizacion.objects.create(
                    idService=idService,
                    nameService=nameService,
                    aumento=aumento,
                    iva=iva,
                    kilometraje=kilometraje,
                    porcAumento=porcAumento,
                    porcIva=porcIva,
                    porcNComercial=porcNComercial,
                    porcSobrepeso=porcSobrepeso,
                    porcSusceptible=porcSusceptible,
                    porcZPeligrosa=porcZPeligrosa,
                    subtotal=subtotal,
                    tarifaKilometraje=tarifaKilometraje,
                    totalServicio=totalServicio,)

                serializer = SerializerServiciosAgregadosCotizacion(nuevoServ)

    busqueda = ServicioCotizacion.objects.values('cambiosConsecutivo').filter(id=idCotiza)
        
    busqueda = int(busqueda[0]['cambiosConsecutivo']) + 1

    conse = ServicioCotizacion.objects.get(id=idCotiza)
    conse.cambiosConsecutivo = busqueda
    conse.save()
    
    return Response(True)

@csrf_exempt 
@api_view(['POST', 'GET'])
def getTarifario(request):

    pais_ori = request.data.get('pais_origen')
    estado_ori = request.data.get('estado_origen')
    ciudad_ori = request.data.get('ciudad_origen')
    pais_des = request.data.get('pais_destino')
    estado_des = request.data.get('estado_destino')
    ciudad_des = request.data.get('ciudad_destino')
    mod = request.data.get('modalidad')
    #ori = ori.upper()
    #des = des.upper()
    tarRes = []

    if estado_ori == 'Ciudad de Mexico':
        ciudad_ori = 'Ciudad de Mexico'
    if estado_des == 'Ciudad de Mexico':
        ciudad_des = 'Ciudad de Mexico'

    d = Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=ciudad_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=ciudad_des).filter(aplica__icontains=mod)
    print(d.query)

    if Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=ciudad_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=ciudad_des).filter(aplica__icontains=mod).exists():

        tarif = Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=ciudad_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=ciudad_des).filter(aplica__icontains=mod)
        tarifa = SerializerTarifario(tarif, many=True)
    
        return Response(tarifa.data)

    elif Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=estado_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=ciudad_des).filter(aplica__icontains=mod).exists():
        tarif = Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=estado_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=ciudad_des).filter(aplica__icontains=mod)
        tarifa = SerializerTarifario(tarif, many=True)
    
        return Response(tarifa.data)
    elif Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=ciudad_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=estado_des).filter(aplica__icontains=mod).exists():
        tarif = Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=ciudad_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=estado_des).filter(aplica__icontains=mod)
        tarifa = SerializerTarifario(tarif, many=True)
    
        return Response(tarifa.data)
    else:
        tarif = Tarifario.objects.filter(pais_origen=pais_ori).filter(estado_origen=estado_ori).filter(ciudad_origen=estado_ori).filter(pais_destino=pais_des).filter(estado_destino=estado_des).filter(ciudad_destino=estado_des).filter(aplica__icontains=mod)
        tarifa = SerializerTarifario(tarif, many=True)
    
        return Response(tarifa.data)
    
@csrf_exempt
@api_view(['GET'])
def ListTarifarioFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = str(request.GET.get('userSearch', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Tarifario.objects.filter(Q(estatus=0)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(estatus=0)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=0)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=0)).filter(Q(usuarioAlta = user)).count()

    goods_ser=SerializerTarifario(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def ListTarifarioActivoFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = str(request.GET.get('userSearch', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Tarifario.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=1)).filter(Q(usuarioAlta = user)).count()

    goods_ser=SerializerTarifario(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt
@api_view(['GET'])
def ListTarifarioInactivoFiltro(request):

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))
    palabra=str(request.GET.get('palabra', 1))
    user = str(request.GET.get('userSearch', 1))
    data_start = (page - 1) * size
    data_end = page * size

    if (palabra == ""):
        goodslist = Tarifario.objects.filter(Q(estatus=2)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(estatus=2)).filter(Q(usuarioAlta = user)).count()
    else:
        goodslist = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=2)).filter(Q(usuarioAlta = user))[data_start:data_end]
        count = Tarifario.objects.filter(Q(origen__icontains=palabra) | Q(desitino__icontains=palabra)).filter(Q(estatus=2)).filter(Q(usuarioAlta = user)).count()

    goods_ser=SerializerTarifario(goodslist,many=True)

    return Response({'total':count, 'data':goods_ser.data})

@csrf_exempt 
@api_view(['POST', 'GET'])
def insertTarifa(request):  

    data = request.data.get('datos')
    tarifa = []

    for dato in data:

        tarifa.append(dato)

    for tar in tarifa:

        origen=tar['origen']
        destino=tar['destino']
        factor_conversion=tar['factor_conversion']
        recoleccion_tres_y_media=tar['recoleccion_tres_y_media']
        recoleccion_rabon=tar['recoleccion_rabon']
        recoleccion_torton=tar['recoleccion_torton']
        flete_nacional=tar['flete_nacional']
        entrega_puerto_nissan=tar['entrega_puerto_nissan']
        entrega_puerto_tres_y_media=tar['entrega_puerto_tres_y_media']
        entrega_rabon=tar['entrega_rabon']
        entrega_torton=tar['entrega_torton']
        usuarioAlta=tar['usuario']
        
        create = Tarifario.objects.create(origen=origen, 
                                 destino=destino,
                                 factor_conversion=factor_conversion,
                                 recoleccion_tres_y_media=recoleccion_tres_y_media,
                                 recoleccion_rabon=recoleccion_rabon,
                                 recoleccion_torton=recoleccion_torton,
                                 flete_nacional=flete_nacional,
                                 entrega_puerto_nissan=entrega_puerto_nissan,
                                 entrega_puerto_tres_y_media=entrega_puerto_tres_y_media,
                                 entrega_rabon=entrega_rabon,
                                 entrega_torton=entrega_torton,
                                 estatus=0,
                                 usuarioAlta=usuarioAlta,
                                 dateCreate=datetime.now())

    if create.idTarifa > 0:

        resp = [{"insert": True, "msg": "La tarifa se dio de alta correctamente.",}]
    else:
        resp = [{"insert": False, "msg": "Ocurrio un error al intentar dar de alta la tarfia, avisa a Sistemas.",}]
    
    
    return Response(resp)
    
@csrf_exempt 
@api_view(['PUT'])
def deleteTarifa(request, pk):
    
    idT = pk
    
    if idT != 0:
        tarifa = Tarifario.objects.get(idTarifa=idT)
        tarifa.estatus = 3
        tarifa.save()
        resp = [{"delete": True, "msg": "La tarifa se dio de baja correctamente.",}]
    else:
        resp = [{"delete": False, "msg": "Ocurrio un error al intentar dar de baja la tarfia, avisa a Sistemas.",}]
    
    return Response(resp)

@csrf_exempt 
@api_view(['POST','GET'],)
def getTarifa(request, pk):

    id = pk

    tarifa = Tarifario.objects.filter(idTarifa=id)
    tar = SerializerTarifario(tarifa, many=True)

    return Response(tar.data)

@csrf_exempt 
@api_view(['POST'])
def updateTarifa(request):  

    data = request.data.get('datos')
    tarifa = []
    idTarifa = 0
    origen = ""
    destino = ""
    factor_conversion = 0
    recoleccion_tres_y_media = 0
    recoleccion_rabon = 0
    recoleccion_torton = 0
    flete_nacional = 0
    entrega_puerto_nissan = 0
    entrega_puerto_tres_y_media = 0
    entrega_rabon = 0
    entrega_torton = 0
    usuarioAlta = 0
    
    resp = [{"update": True, "msg": "La tarifa se dio de alta correctamente.",}]

    for dato in data:

        tarifa.append(dato)

    for tar in tarifa:

        idTarifa=tar['idTarifa']
        origen=tar['origen']
        destino=tar['destino']
        factor_conversion=tar['factor_conversion']
        recoleccion_tres_y_media=tar['recoleccion_tres_y_media']
        recoleccion_rabon=tar['recoleccion_rabon']
        recoleccion_torton=tar['recoleccion_torton']
        flete_nacional=tar['flete_nacional']
        entrega_puerto_nissan=tar['entrega_puerto_nissan']
        entrega_puerto_tres_y_media=tar['entrega_puerto_tres_y_media']
        entrega_rabon=tar['entrega_rabon']
        entrega_torton=tar['entrega_torton']
        usuarioAlta=tar['usuario']
        estatus=tar['estatus']

        if idTarifa != 0:
            tarifa = Tarifario.objects.get(idTarifa=idTarifa)
            tarifa.origen = origen
            tarifa.destino = destino
            tarifa.factor_conversion = factor_conversion
            tarifa.recoleccion_tres_y_media = recoleccion_tres_y_media
            tarifa.recoleccion_rabon = recoleccion_rabon
            tarifa.recoleccion_torton = recoleccion_torton
            tarifa.flete_nacional = flete_nacional
            tarifa.entrega_puerto_nissan = entrega_puerto_nissan
            tarifa.entrega_puerto_tres_y_media = entrega_puerto_tres_y_media
            tarifa.entrega_rabon = entrega_rabon
            tarifa.entrega_torton = entrega_torton
            tarifa.usuarioModifica = usuarioAlta
            tarifa.dateEdita = timezone.now()
            tarifa.estatus = estatus
            tarifa.save()

            resp = [{"update": True, "msg": "La tarifa se actualizó correctamente.",}]
        else:
            resp = [{"update": False, "msg": "Ocurrio un error al intentar atualizar la tarfia, avisa a Sistemas.",}]
    
    
    return Response(resp)

@csrf_exempt 
@api_view(['POST','GET'],)
def getMercancias(request, pk):

    id = pk

    mercancias = Mercancias.objects.filter(idCotizacion=id)
    merc = SerializerMercancias(mercancias, many=True)

    return Response(merc.data)

@csrf_exempt 
@api_view(['POST','GET'],)
def getPlanes(request, pk):

    id = pk

    planes = Planes.objects.filter(idCotizacion=id)
    plan = SerializerPlanes(planes, many=True)

    return Response(plan.data)   

@csrf_exempt
@api_view(['GET'])
def obtener_detalles_ubicacion(request):

    direccion =  request.GET.get('direccion')
    direccion_dividida = direccion.split(", " )

    if direccion_dividida[2] == 'Edo. Mexico':
        direccion_dividida[2] = 'Estado de Mexico'
    

    busqueda_aeropuerto = 'aeropuerto ' + direccion_dividida[2]
    busqueda_aduanas = 'aduana ' + direccion_dividida[2]
    busqueda_puertos = 'puerto marítimo ' + direccion_dividida[2]
    tipo_aeropuerto = 'airport'
    tipo_aduana = 'customs'
    tipo_puerto = 'harbor'
    
    arrayAeropuertos = []
    arrayAduanas = []
    arrayPuertos = []

    API_KEY = 'AIzaSyAKaWnY1l7mejTiKUf2cg_fRR7SVINOr8o'
    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': direccion,
        'key': API_KEY,
    }

    response = requests.get(url, params=params)
    detalles = response.json()
    lat = detalles['results'][0]['geometry']['location']['lat']
    lng = detalles['results'][0]['geometry']['location']['lng']
    #print(lat, lng, 'primer función')

    aduanas_cercanas = buscar_lugares_cercanos(lat, lng, busqueda_aduanas, 15000, tipo_aduana)
    for aduana in aduanas_cercanas:
        arrayAduanas.append(aduana['name'])

    aeropuertos_cercanos = buscar_lugares_cercanos(lat, lng, busqueda_aeropuerto, 15000, tipo_aeropuerto)
    for aeropuerto in aeropuertos_cercanos:
        arrayAeropuertos.append(aeropuerto['name'])

    puertos_cercanos = buscar_lugares_cercanos(lat, lng, busqueda_puertos, 10000, tipo_puerto)
    for puerto in puertos_cercanos:
        arrayPuertos.append(puerto['name'])

    return Response({'aeropuertos': arrayAeropuertos, 'aduanas':arrayAduanas, 'puertos':arrayPuertos})

def buscar_lugares_cercanos(latitud, longitud, keyword, radius, tipo):
    API_KEY = 'AIzaSyAKaWnY1l7mejTiKUf2cg_fRR7SVINOr8o'
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{latitud},{longitud}',
        'radius': radius,
        'type': tipo,
        'keyword': keyword, 
        'key': API_KEY,
        'language': 'es',
    }

    response = requests.get(url, params=params)
    lugares_cercanos = response.json()
    return lugares_cercanos['results']

@csrf_exempt
@api_view(['GET'])
def obtener_detalles_geocerca(request):
    cp =  request.GET.get('cp')
    estado =  request.GET.get('estado')
    print(cp, estado)
    #cp =  '54918'

    arrayGeo = {}
    arrayDatosGeo = []
    arrayDatosTotal = []

    #poligono = Geocercas.objects.filter(codigoPostal=cp, estado=estado).aggregate(Max('poligono'))['poligono__max']
    poligono = Geocercas.objects.filter(codigoPostal=cp, estado__icontains=estado).aggregate(Max('poligono'))['poligono__max']
    
    if poligono is None:
        poligono = 0
    poligono = (int(poligono) +1)

    if poligono > 0:
        for i in range(poligono):  # Itera desde 1 hasta 5 (excluyendo 6)
            geocercas = Geocercas.objects.filter(codigoPostal=cp, estado__icontains=estado).filter(poligono=(i+1)).order_by('orden').values("codigoPostal", "lat", "lng", "orden", "poligono")

            for element in geocercas:

                arrayDatosGeo.append({'lat':float(element['lat']), 'lng':float(element['lng'])})
            
            if len(arrayDatosGeo) > 0:
                arrayDatosTotal.append(arrayDatosGeo)
            arrayDatosGeo = []
        
        arrayGeo['estatus'] = True
        arrayGeo['datos'] = arrayDatosTotal
    else:
        arrayGeo['estatus'] = False
        arrayGeo['datos'] = 'La dirección que intentas ingresar no está dentro de nuestra cobertura, intentalo con otra dirección.'


    '''for resultado in resultados:
        print(f"Código Postal: {resultado.codigoPostal}, Latitud: {resultado.latitud}, Longitud: {resultado.longitud}, Orden: {resultado.orden}, Polígono: {resultado.poligono}")'''

    return Response({'geocerca': arrayGeo})

@csrf_exempt
@api_view(['GET'])
def obtener_detalles_geocerca_puertos(request):
    nom_cort =  request.GET.get('nombre_corto')

    #poligono = Geocercas.objects.filter(codigoPostal=cp, estado=estado).aggregate(Max('poligono'))['poligono__max']
    datosGeo = Geocercas.objects.filter(nombre_corto=nom_cort)
    serDatos = GeocercasSerializer(datosGeo, many=True)
    return Response({'geocerca': serDatos.data})

@csrf_exempt
@api_view(['GET'])
def detalles_geocerca(request):
    pais = request.GET.get('pais')
    estado = request.GET.get('estado')
    ciudad = request.GET.get('ciudad')

    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
    trans = str.maketrans(a,b)

    #poligono = Geocercas.objects.filter(codigoPostal=cp, estado=estado).aggregate(Max('poligono'))['poligono__max']
    datosGeo = Geocercas.objects.filter(pais=pais.translate(trans), estado=estado.translate(trans), ciudad=ciudad.translate(trans))
    
    serDatos = GeocercasSerializer(datosGeo, many=True)
    return Response({'geocerca': serDatos.data})


@csrf_exempt 
@api_view(['POST', 'GET'])
def send_email_agente(request):

    pkC = request.data.get('id')
    email = request.data.get('correoAgente')
    nombre_contacto = request.data.get('nombreCliente')

    motivo = request.data.get('motivoAgente')
    email_cliente = request.data.get('emailCliente')
    telefono_cliente = request.data.get('telefonoCliente')
    telefonoAgente = ''
    nombreAgente = ''
    apellidoAgente = ''
    infoAgente = {}
    telefonoClienteChat = telefono_cliente.replace('+52','521')

    numeroBoot = '5215541708682'

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    # Filtrar los leads que coincidan con el número de teléfono y la fecha actual
    existencia_lead = leds_chatboot.objects.filter(Q(numero_usr=telefonoClienteChat), Q(date_create=fecha_actual))[:1]
    
    if existencia_lead.count() > 0:
        datoLead = LedsSerializer(existencia_lead, many=True)
        numeroAgente = datoLead.data[0]['numero_agente']

        agente = numeros_ejecutivos_chatboot.objects.filter(Q(es_gerente=False), Q(estatus=1), Q(numero_agente = numeroAgente))
        agenteSer = NumerosSerializer(agente, many=True)
        idAgente = agenteSer.data[0]['id']
        telefonoAgente = agenteSer.data[0]['numero_agente']
        nombreAgente = agenteSer.data[0]['nombre']
        apellidoAgente = agenteSer.data[0]['apellido']

        infoAgente = {"id_agente" : idAgente, 
                        "numero_agente" : telefonoAgente, 
                        "nombre_agente" : nombreAgente, 
                        "apellido_agente" : apellidoAgente,
                        "servicio" : 1,  
                        "nombre_lead" : nombre_contacto,
                        "numero_lead" : telefono_cliente,
                        "nombreServicio": 'Terrestre Nacional',
                        "canal_entrada":'cotizador',
                    }
    else:
        ultimo_lead = leds_chatboot.objects.order_by('-id')[:1]
        uleadSer = LedsSerializer(ultimo_lead, many=True)
        
        numeroAgente = uleadSer.data[0]['numero_agente']

        agente = numeros_ejecutivos_chatboot.objects.filter(Q(es_gerente=False), Q(estatus=1), Q(numero_agente = numeroAgente))
        agenteSer = NumerosSerializer(agente, many=True)
        idAgente = int(agenteSer.data[0]['id']) + 2

        numMax = numeros_ejecutivos_chatboot.objects.filter(Q(es_gerente=False), Q(estatus=1)).aggregate(Max('id'))['id__max']

        if idAgente > numMax:
            idAgente = 1
        
        agenteAsigna = numeros_ejecutivos_chatboot.objects.filter(Q(id=idAgente))
        agenteAsSer = NumerosSerializer(agenteAsigna, many=True)

        idAgente = agenteAsSer.data[0]['id']
        telefonoAgente = agenteAsSer.data[0]['numero_agente']
        nombreAgente = agenteAsSer.data[0]['nombre']
        apellidoAgente = agenteAsSer.data[0]['apellido']

        infoAgente = {"id_agente" : idAgente, 
                        "numero_agente" : telefonoAgente, 
                        "nombre_agente" : nombreAgente, 
                        "apellido_agente" : apellidoAgente,
                        "servicio" : 1,  
                        "nombre_lead" : nombre_contacto,
                        "numero_lead" : telefono_cliente,
                        "nombreServicio": 'Terrestre Nacional',
                        "canal_entrada":'cotizador',
                    }
    
        datos = json.dumps(infoAgente)
    
    print(datos)
    #envia_mensajes(datos)

    if email == '':
        email = 'danielrg847@gmail.com'

    email = 'danielrg847@gmail.com'

    servRes = []
    merchGlob = []
    servGlob = []

    cantidad = 0
    volTot = 0
    pesoVol = 0
    pesoTot = 0

    susbtotalGlob = 0
    porcIvaGlob = 0
    totalServicioGlob = 0
    
    emailD = EmailDatos.objects.filter(idEmail=1)
    emailS = EmailDatosSerializer(emailD, many=True)

    correoInt = 'sisproyect@gmail.com' #emailS.data[0]['correo']
    contraInt = 'ntbl mrgu brvv qmiq' #emailS.data[0]['contra']
    hostInter = 'smtp.gmail.com' #emailS.data[0]['host']
    puerInter = 587 #emailS.data[0]['port']

    mensaje = MIMEMultipart()

    mailServer = smtplib.SMTP(hostInter, puerInter)
        
    mailServer.starttls()

    mailServer.login(correoInt, contraInt)
    email_to=email

    mensaje['From']= correoInt
    mensaje['To']=email_to
    mensaje['Subject'] = "Solicitud de Cotización"

    cotiza = ServicioCotizacion.objects.filter(id=pkC)
    coti = FiltroServicioCotizacion(cotiza, many=True)

    divisa = int(coti.data[0]['divisaFinal'])
    tipoOp = str(coti.data[0]['tipoOperacion'])
    valorDolar = 19.8532

    content = render_to_string('pdf/correoAgente.html', {'nomCli': nombre_contacto, 'motivoAgente': motivo, 'nombreCotizacion': nombre_contacto, 'correoCotizacion': email_cliente, 'numeroCotizacion': telefono_cliente})
    mensaje.attach(MIMEText(content,'html'))

    service = ServiciosAgregadosCotizacion.objects.filter(idcotizacion_id=pkC)
    serv = SerializerServiciosAgregadosCotizacion(service, many=True)

    if divisa == 2:
        for dato in service:

            susbtotalGlob = susbtotalGlob + float(dato.subtotal)
            porcIvaGlob = porcIvaGlob + float(dato.porcIva)
            totalServicioGlob = totalServicioGlob + float(dato.totalServicio)

            subtotal = float(dato.subtotal)
            subtotal = "{:,.2f}".format(subtotal)
            porcIva = float(dato.porcIva)
            porcIva = "{:,.2f}".format(porcIva)
            totalServicio = float(dato.totalServicio)
            totalServicio = "{:,.2f}".format(totalServicio)

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'susbtotal': subtotal,
                'kilometraje': float(dato.kilometraje),
                'porcIva': porcIva,
                'porcNComercial': float(dato.porcNComercial),
                'porcSobrepeso': float(dato.porcSobrepeso),
                'porcSusceptible': float(dato.porcSusceptible),
                'porcZPeligrosa': float(dato.porcZPeligrosa),
                'tarifaKilometraje': float(dato.tarifaKilometraje),
                'totalServicio': totalServicio,
            })
        
        susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
        porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
        totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

        servGlob.append({
            'susbtotalGlob': susbtotalGlob,
            'porcIvaGlob': porcIvaGlob,
            'totalServicioGlob': totalServicioGlob,
        })
    else:
        for dato in service:

            susbtotalGlob = susbtotalGlob + round((float(dato.subtotal) / valorDolar), 2)
            porcIvaGlob = porcIvaGlob + round((float(dato.porcIva) / valorDolar), 2)
            totalServicioGlob = totalServicioGlob + round((float(dato.totalServicio) / valorDolar), 2)

            subtotal = round((float(dato.subtotal) / valorDolar), 2)
            subtotal = "{:,.2f}".format(subtotal)
            porcIva = round((float(dato.porcIva) / valorDolar), 2)
            porcIva = "{:,.2f}".format(porcIva)
            totalServicio = round((float(dato.totalServicio) / valorDolar), 2)
            totalServicio = "{:,.2f}".format(totalServicio)

            servRes.append({
                'id': dato.id,
                'idService': dato.idService,
                'nameService': dato.nameService,
                'susbtotal': subtotal,
                'kilometraje': round((float(dato.kilometraje) / valorDolar), 2),
                'porcIva': porcIva,
                'porcNComercial': round((float(dato.porcNComercial) / valorDolar), 2),
                'porcSobrepeso': round((float(dato.porcSobrepeso) / valorDolar), 2),
                'porcSusceptible': round((float(dato.porcSusceptible) / valorDolar), 2),
                'porcZPeligrosa': round((float(dato.porcZPeligrosa) / valorDolar), 2),
                'tarifaKilometraje': round((float(dato.tarifaKilometraje) / valorDolar), 2),
                'totalServicio': totalServicio,
                    
            })

        susbtotalGlob = "{:,.2f}".format(susbtotalGlob)
        porcIvaGlob = "{:,.2f}".format(porcIvaGlob)
        totalServicioGlob = "{:,.2f}".format(totalServicioGlob)

        servGlob.append({
            'susbtotalGlob': susbtotalGlob,
            'porcIvaGlob': porcIvaGlob,
            'totalServicioGlob': totalServicioGlob,
        })

    contact = ContactoCotizacion.objects.filter(idcotizacion_id=pkC)
    cont = SerializerContactoCotizacion(contact, many=True)

    merch = Mercancias.objects.filter(idCotizacion_id=pkC)
    merc = SerializerMercancias(merch, many=True)

    unidadElegida = UnitBox.objects.filter(id=coti.data[0]['id_unidad'])
    undidadEl = UnitBoxSerializer(unidadElegida, many=True)
    
    direcciones = DireccionCotizacion.objects.filter(idcotizacion_id=pkC).order_by('id')
    dir = SerializerDireccionCotizacion(direcciones, many=True)
    
    
    for dato in merch:
        
        cantidad = cantidad + int(dato.cantidad)
        volTot = volTot + float(dato.volumenTotal)
        pesoVol = pesoVol + float(dato.pesoVolumetricoTotal)
        pesoTot = pesoTot + float(dato.pesoTotal)
    
    merchGlob.append({
        'cantidad': cantidad,
        'volTot': volTot,
        'pesoVol': pesoVol,
        'pesoTotal': pesoTot,
    })

    planes = Planes.objects.filter(idCotizacion_id=pkC).order_by('orden')
    plan = SerializerPlanes(planes, many=True)

    terminos = Terminos_Condiciones.objects.filter(aplica__icontains=tipoOp).order_by('orden')
    term = TerminosCondicionesSerializer(terminos, many=True)

    img_cinta = compress_and_encode_image('cotizaciones/templates/img/Interland-cinta.png', 75)
    img_planes = compress_and_encode_image('cotizaciones/templates/img/delivery-truck.png', 75)
    img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)

    nombre = "Cotizacion-"+coti.data[0]['folioConsecutivo']+".pdf"

    html = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': coti.data, 'ServiciosAgregadosCotizacion': servRes, 'direcciones':dir.data,'ServiciosAgregadosCotizacionGlobal': servGlob, 'ContactoCotizacion': cont.data, 'unidad':undidadEl.data, 'mercancias':  merc.data, 'mercanciasGlob':  merchGlob, "planes":plan.data, "imgCinta":img_cinta, "imgPlanes":img_planes, "imgLogo":img_logo, "disclamers":term.data}) 
    name_file = "media/cotizacion_chatboot/"+nombre

    result_file = open(name_file, "w+b")

    pisa_status = pisa.CreatePDF(html,dest=result_file)

    result_file.close()

    archivoAgente = 'http://sicolog.ifreight.business/media/cotizacion_chatboot/Cotizacion-'+coti.data[0]['folioConsecutivo']+'.pdf'
    #archivoAgente = 'http://127.0.0.1:8000/media/cotizacion_chatboot/Cotizacion-'+coti.data[0]['folioConsecutivo']+'.pdf'

    url = "https://api.botmaker.com/v2.0/chats-actions/send-messages"

    payload = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": telefonoAgente
        },
        "messages": [
            {
                "text": 'Folio: '+coti.data[0]['folioConsecutivo'],
                "media": {
                    "mimeType": "application/pdf",
                    "url": archivoAgente
                }
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoiaW50ZXJsYW5kIiwibmFtZSI6ImRhbmllbC5nb21lekBpbnRlcmxhbmQuYnVzaW5lc3MiLCJhcGkiOnRydWUsImlkIjoiMkQ0eTBiZlZJM2NITzg5anE0TjJiV2ExQ2J1MSIsImV4cCI6MTg4ODUwNzcxMSwianRpIjoiMkQ0eTBiZlZJM2NITzg5anE0TjJiV2ExQ2J1MSJ9.fSRBodIHAFiqqvhq1XW3b17noEiK_DL_ysNV8AMYM_02oduk5g423IyxVlYwweHC-WfbPTidNLvrEegAa5sIyQ"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    with open(name_file, "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename=str(nombre))
    mensaje.attach(attach)

    try:
        # Envía el correo
        #mailServer.sendmail('infor@mx-interland.com', email_to, mensaje.as_string())

        resp = True

        mailServer.quit()

    except SMTPException as e:
        # Maneja la excepción
        resp = e

    os.unlink(name_file)
    return Response({"msg":resp})


def obtenerKM(origen, destino, tipoZona):
    km = 0
    for tz in tipoZona:
        origenValor = origen['pais']+', '+origen['estado']+', '+origen['ciudad']+', '+origen['codigoPostal']
        destinoValor = destino['pais']+', '+destino['estado']+', '+destino['ciudad']+', '+destino['codigoPostal']
        if tz['origen'] == origenValor and tz['destino'] == destinoValor:
          km = float(tz['km'])
    return km

def obtenerValor(unidad, origen, destino, listtipoZona, listPorcentajes, tipoMercancia, listAdicionales):

    precio = float(unidad['precio_kilometraje'])
    resBase = 0
    res = 0
    resDes = 0
    resInc = 0
    tipoCarga = 'Carga General'
    resHaz = 0
    resRef = 0
    resSuc = 0
    resSeg = 0

    porcentajeIMO = 35
    porcentajeRef = 10
    porcentajeSuc = 15
    porcentajeSeg = 85
    porcentajeIncremento = 0
    porcentajeIncrementoZona = 0
    porcentajeDecremento = 0

    for tz in listtipoZona:
        origenValor = origen['pais']+', '+origen['estado']+', '+origen['ciudad']+', '+origen['codigoPostal']
        destinoValor = destino['pais']+', '+destino['estado']+', '+destino['ciudad']+', '+destino['codigoPostal']
        destinoRuta = origen['estado']+' - '+destino['estado']
        if tz['origen'] == origenValor and tz['destino'] == destinoValor:
            tipozona = 'Zona '+tz['tipoZona']
            km = float(tz['km'])
            for porc in listPorcentajes:
                if porc['mercancia'] == tipozona and porc['tipo'] == 'i':
                    porcentajeIncrementoZona = porcentajeIncrementoZona + float(porc['porcentaje'])

                if porc['mercancia'] == tipoCarga and porc['tipo'] == 'i':
                    porcentajeIncremento = porcentajeIncremento + float(porc['porcentaje'])
                    
                if porc['mercancia'] == destinoRuta  and porc['tipo'] == 'd':
                    porcentajeDecremento = porcentajeDecremento + float(porc['porcentaje'])

            res = precio * km
            print(res, 'Precio Normal: Precio ', precio, ' * km ', km)

            if porcentajeIncrementoZona > 0:
                resInc = (res * porcentajeIncrementoZona) / 100
                res = res + resInc;
                print('Incremento de Zona: ', resInc, 'Porcentaje Aplicado: ', porcentajeIncrementoZona, 'Resultado con procentaje aplicado: ',res)
            else:
                print(res, 'Precio Normal')
            
            resBase = res
            print(resBase, 'Precio Base')

            if tipoMercancia == 'h':
                resHaz = (resBase * porcentajeIMO) / 100
                res = resBase + resHaz
                print('Incremento por Carga IMO/Peigrosa: ', resHaz, 'Porcentaje Aplicado: ',porcentajeIMO, 'Resultado con porcentaje aplicado: ', res)
            

            if tipoMercancia == 'r':
                resRef = (resBase * porcentajeRef) / 100
                res = resBase + resRef
                print('Incremento por Carga Refrigerada: ', resRef, 'Porcentaje Aplicado: ',porcentajeRef, 'Resultado con porcentaje aplicado: ', res)
            

            if tipoMercancia == 'sr':
                resSuc = (resBase * porcentajeSuc) / 100
                res = resBase + resSuc
                print('Incremento por Carga Suceptible a Robo: ', resSuc, 'Porcentaje Aplicado: ',porcentajeSuc, 'Resultado con porcentaje aplicado: ', res)
            
            resInc = (resBase * porcentajeIncremento) / 100;
            res = resBase + resInc
            print('Incremento Aplicable: ', resInc, 'Porcentaje Aplicado: ',porcentajeIncremento, 'Resultado con porcentaje aplicado: ', res)

            resDes = (resBase * porcentajeDecremento) / 100;
            res = resBase - resDes
            print('Decremento Aplicable: ', resDes, 'Porcentaje Aplicado: ',porcentajeDecremento, 'Resultado con porcentaje aplicado: ', res)

            ''' SECCION ADICIONALES '''

            for add in listAdicionales:
                if int(unidad['id']) == 1: #Nissan
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 3200
                        print('Incremento por Servicio: ', 3200, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 530
                        print('Incremento por Servicio: ', 530, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 610
                        print('Incremento por Servicio: ', 610, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)
                   
                if int(unidad['id']) == 2: #3 1/2
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 3630
                        print('Incremento por Servicio: ', 3630, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 605
                        print('Incremento por Servicio: ', 605, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 1265
                        print('Incremento por Servicio: ', 1265, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100;
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                if int(unidad['id']) == 3: #rabon
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 4290
                        print('Incremento por Servicio: ', 4290, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 720
                        print('Incremento por Servicio: ', 720, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 2310
                        print('Incremento por Servicio: ', 2310, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100;
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                if int(unidad['id']) == 4: #caja 48
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 6270
                        print('Incremento por Servicio: ', 6270, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 1050
                        print('Incremento por Servicio: ', 1050, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 3780
                        print('Incremento por Servicio: ', 3780, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                if int(unidad['id']) == 5: #caja 53
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 6270
                        print('Incremento por Servicio: ', 6270, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 1050
                        print('Incremento por Servicio: ', 1050, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 3780
                        print('Incremento por Servicio: ', 3780, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)
                    
                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                if int(unidad['id']) == 13: #torton
                    if add['nombreServicio'] == 'ESTADIA POR DÍA':
                        res = res + 4950
                        print('Incremento por Servicio: ', 4950, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'ESTADIA POR HORA':
                        res = res + 820
                        print('Incremento por Servicio: ', 820, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'MANIOBRAS DE CARGA Y DESCARGA':
                        res = res + 2640
                        print('Incremento por Servicio: ', 2640, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

                    if add['nombreServicio'] == 'SEGURO':
                        resSeg = (resBase * porcentajeSeg) / 100
                        res = res + resSeg
                        print('Incremento por Servicio: ', resSeg, 'Servicio:', add['nombreServicio'] ,'Resultado con incremento aplicado: ',res)

            ''' FIN SECCION ADICIONALES '''

            if km > 500 and km < 800 and origen['nombre_corto'] == 'CDMX':
                resDes = (resBase * 30) / 100; #SE RESTA 30% POR EXCEDER 500 KM
                res = resBase - resDes;
                print('Decremento Aplicable: ', resDes, 'Porcentaje Aplicado: ',30, 'Resultado con porcentaje aplicado: ', res)
            

            if km > 800 and origen['nombre_corto'] == 'CDMX':
                resDes = (resBase * 45) / 100; #SE RESTA 45% POR EXCEDER 500 KM
                res = resBase - resDes;
                print('Decremento Aplicable: ', resDes, 'Porcentaje Aplicado: ',45, 'Resultado con porcentaje aplicado: ', res)
            
        
            print('Precio Final: ', res)
            print('-----------------------------------------------------------')

    
    return(res)

def obtenerValorAdicional(listPorcentajes, base):
    porcentajeIncremento = 0
    porcentajeDecremento = 0
    template = ''

    for porc in listPorcentajes:
        if porc['mercancia'] == 'IMO':
            porcentajeIncremento = porcentajeIncremento + float(porc['porcentaje'])
            if porcentajeIncremento > 0:
              resDes = (base * porcentajeIncremento) / 100;
              res = base + resDes;
              template = template +'<h4><span class="badge badge-secondary">Precio por carga IMO: '+formatear_moneda(res)+'</span></h4>';
            else:
              template = template +'<h4><span class="badge badge-secondary">Precio por carga IMO: '+formatear_moneda(base)+'</span></h4>';
            
            porcentajeIncremento = 0
        
        if porc['mercancia'] == 'Refrigerada':
            porcentajeIncremento = porcentajeIncremento + float(porc['porcentaje'])
            if porcentajeIncremento > 0:
                resDes = (base * porcentajeIncremento) / 100;
                res = base + resDes;
                template = template +'<h4><span class="badge badge-secondary">Precio por carga Refrigerada: '+formatear_moneda(res)+'</span></h4>';
            else:
              template = template +'<h4><span class="badge badge-secondary">Precio por carga Refrigerada: '+formatear_moneda(base)+'</span></h4>';
            
            porcentajeIncremento = 0
        
        if porc['mercancia'] == '2 Operadores':
            porcentajeIncremento = porcentajeIncremento + float(porc['porcentaje'])
            if porcentajeIncremento > 0:
                resDes = (base * porcentajeIncremento) / 100;
                res = base + resDes;
                template = template +'<h4><span class="badge badge-secondary">Precio por 2 Operadores: '+formatear_moneda(res)+'</span></h4>';
            else:
                template = template +'<h4><span class="badge badge-secondary">Precio por 2 Operadores: '+formatear_moneda(base)+'</span></h4>';
            
            porcentajeIncremento = 0
    
    return template
          
def formatear_moneda(cifra):
    # Establecer la configuración local para formatear como moneda
    locale.setlocale(locale.LC_ALL, '')

    # Formatear la cifra como moneda utilizando la configuración local
    cifra_formateada = locale.currency(cifra, grouping=True)

    return cifra_formateada

@csrf_exempt 
@api_view(['POST', 'GET'])
def pdf_tarifario_ltl(request):

    listorigenes = request.data.get('origen')
    listdestinos = request.data.get('destino')
    listaOD = request.data.get('listaOD')
    listunidades = request.data.get('unidades')
    listrangos = request.data.get('rangos')
    listtipoZona = request.data.get('tipoZona')
    listPorcentajes = request.data.get('porcentajes')
    tipoMercancia = request.data.get('tipoMercancia')
    listAdicionales = request.data.get('serviciosAdicionales')
    table = ''
    etiquetaOrigen = ''
    etiquetaDestino = ''

    for origen in listorigenes:
        for destino in listdestinos:
            table  += '<table style="width: 100%; border: 1px solid;">'
            table += '  <thead class="text-white">'
            table += '      <tr style="background-color: #2aab5c; color:#ffffff;">'
            table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b>Origen</b></td>'
            table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b>Destino</b></td>'
            table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b>Unidad</b></td>'
            table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b>Costo Kilometraje</b></td>'
            for rango in listrangos:
                km = obtenerKM(origen,destino,listtipoZona)
                km_dato = int(km)
                min = float(rango['min'])
                max = float(rango['max'])
                if km > min:
                    if km > min and km < max:
                        table += '  <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b> de '+ rango['min'] +' km a ' + str(km_dato) +' km</b></td>'
                    else:
                        table += '  <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 1em; "><b> de '+ rango['min'] +' km a ' + rango['max'] +' km</b></td>'


            table += '      </tr>'
            table += '  </thead>'
            table += '  <tbody style="border: 1px solid #edeff1; border-collapse: collapse;">'
            for unidad in listunidades:
                
                table += '      <tr>'
                if int(origen['estatus_geocerca']) == 1:
                    etiquetaOrigen = '<label style="background-color: #2aab5c; color: white; text-align: center; padding: 10px;">Zona Comercial</label>'
                elif int(origen['estatus_geocerca']) == 2:
                    etiquetaOrigen = '<label style="background-color: #f7b84b; color: white; text-align: center; padding: 10px;">Zona No Comercial</label>'
                elif int(origen['estatus_geocerca']) == 3:
                    etiquetaOrigen = '<label style="background-color: #f1556c; color: white; text-align: center; padding: 10px;">Zona Peligrosa</label>'
                
                if int(destino['estatus_geocerca']) == 1:
                    etiquetaDestino = '<label style="background-color: #2aab5c; color: white; text-align: center; padding: 10px;">Zona Comercial</label>'
                elif int(destino['estatus_geocerca']) == 2:
                    etiquetaDestino = '<label style="background-color: #f7b84b; color: white; text-align: center; padding: 10px;">Zona No Comercial</label>'
                elif int(destino['estatus_geocerca']) == 3:
                    etiquetaDestino = '<label style="background-color: #f1556c; color: white; text-align: center; padding: 10px;">Zona Peligrosa</label>'


                table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 1em; "><b>' + origen['estado'] + ', ' + origen['ciudad'] + '<br>'+ etiquetaOrigen +'</b></td>'
                table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 1em; "><b>' + destino['estado'] + ', ' + destino['ciudad'] + '<br>'+ etiquetaDestino +'</b></td>'
                table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 1em; "><b>' + unidad['name'] + '</b></td>'
                table += '          <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 1em; "><b>' + formatear_moneda(float(unidad['precio_kilometraje'])) + '</b></td>'
                
                for rango in listrangos:
                    km = obtenerKM(origen,destino,listtipoZona)
                    km_dato = int(km)
                    min = float(rango['min'])
                    max = float(rango['max'])
                    precio_base = obtenerValor(unidad, rango, origen, destino, listtipoZona, listPorcentajes, tipoMercancia, listAdicionales)
                    adicionales = obtenerValorAdicional(listPorcentajes,precio_base)
                    if km > min:
                        table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 1em; "><b>' + formatear_moneda(precio_base) + '</b> <div class="card">'+adicionales+'</div></td>'
                table += '      </tr>'

            table += '  </tbody>'
            table += '</table> <br>'
 
    img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)
    
    html_content = render_to_string('pdf/tarifarioLTL.html', {"imgLogo": img_logo, "tabla":table})

    # Convertir el HTML a PDF
    result = io.BytesIO()
    pdf = pisa.CreatePDF(html_content, dest=result)

    # Comprobar si la conversión fue exitosa
    if not pdf.err:
        # Devolver el PDF como una respuesta HTTP con el tipo de contenido adecuado
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_pdf.pdf"'  # Para mostrar el PDF en el navegador
        return response

    return HttpResponse('Error al generar el PDF')

@csrf_exempt 
@api_view(['POST', 'GET'])
def pdf_tarifario_ltl_2(request):

    listorigenes = request.data.get('origen')
    listdestinos = request.data.get('destino')
    listaOD = request.data.get('listaOD')
    listunidades = request.data.get('unidades')
    listrangos = request.data.get('rangos')
    listtipoZona = request.data.get('tipoZona')
    listPorcentajes = request.data.get('porcentajes')
    tipoMercancia = request.data.get('tipoMercancia')
    listAdicionales = request.data.get('serviciosAdicionales')
    listMercancias = request.data.get('mercancias')
    listContactos = request.data.get('contacto')
    modalidad = request.data.get('termodalidad')
    tiposervicio = request.data.get('tiposervicio')
    usuario = request.data.get('usuario')
    contacName = request.data.get('contacName')
    contacEmail = request.data.get('contacEmail')
    contacTelefono = request.data.get('contacTelefono')
    contacDescription = request.data.get('contacDescription')
    idCotizacion = request.data.get('idCotizacion')
    table = ''
    tableAdicionales = ''
    tableClausulas = ''
    etiquetaOrigen = ''
    etiquetaDestino = ''

    table  += '<table style="width: 100%; border: 1px solid;">'
    table += '  <thead class="text-white">'
    table += '      <tr style="background-color: #ffffff; color:#000000;">'
    table += '          <td colspan="2" style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; "><b>Ruta</b></td>'
    table += '          <td colspan="'+str(len(listunidades))+'" style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; "><b>Detalles del Servicio</b></td>'
    table += '      </tr>'
    table += '      <tr style="background-color: #2aab5c; color:#ffffff;">'
    table += '          <td style="text-align: center; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Origen</b></td>'
    table += '          <td style="text-align: center; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Destino</b></td>'
    for unidad in listunidades:
                table += '  <td style="text-align: center; vertical-align: center; border: 1px solid #2aab5c; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>'+ unidad['name'] +'</b></td>'    
    table += '      </tr>'
    table += '  </thead>'
    table += '  <tbody style="border: 1px solid #edeff1; border-collapse: collapse;">'
    for origen in listorigenes:
        for destino in listdestinos:
            table += '      <tr>'
            if int(origen['estatus_geocerca']) == 1:
                etiquetaOrigen = '<label style="background-color: #2aab5c; color: white; text-align: center; padding: 10px;">Zona Comercial</label>'
            elif int(origen['estatus_geocerca']) == 2:
                etiquetaOrigen = '<label style="background-color: #f7b84b; color: white; text-align: center; padding: 10px;">Zona No Comercial</label>'
            elif int(origen['estatus_geocerca']) == 3:
                etiquetaOrigen = '<label style="background-color: #f1556c; color: white; text-align: center; padding: 10px;">Zona Peligrosa</label>'
                
            if int(destino['estatus_geocerca']) == 1:
                etiquetaDestino = '<label style="background-color: #2aab5c; color: white; text-align: center; padding: 10px;">Zona Comercial</label>'
            elif int(destino['estatus_geocerca']) == 2:
                etiquetaDestino = '<label style="background-color: #f7b84b; color: white; text-align: center; padding: 10px;">Zona No Comercial</label>'
            elif int(destino['estatus_geocerca']) == 3:
                etiquetaDestino = '<label style="background-color: #f1556c; color: white; text-align: center; padding: 10px;">Zona Peligrosa</label>'

            if origen['nombre_corto'] != '':
                table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>' + origen['nombre_corto'] + '<br>'+ etiquetaOrigen +'</b></td>'
            else:
                table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>' + origen['estado'] + ', ' + origen['ciudad'] + '<br>'+ etiquetaOrigen +'</b></td>'
            
            if destino['nombre_corto'] != '':
                table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>' + destino['nombre_corto'] + '<br>'+ etiquetaDestino +'</b></td>'
            else:
                table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>' + destino['estado'] + ', ' + destino['ciudad'] + '<br>'+ etiquetaDestino +'</b></td>'

            for unidad in listunidades:
                precio_base = obtenerValor(unidad, origen, destino, listtipoZona, listPorcentajes, tipoMercancia, listAdicionales)
                table += '      <td style="text-align: center; width: 25%; vertical-align: center; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>' + formatear_moneda(precio_base) + '</b> </td>'

            table += '      </tr>'

    table += '  </tbody>'
    table += '</table>'

    #table += '<div>&nbsp;</div>'

    tableAdicionales += '<div>&nbsp;</div>'
    tableAdicionales  += '<table style="width: 100%; border: 1px solid;">'
    tableAdicionales += '  <thead class="text-white">'
    tableAdicionales += '      <!--tr style="background-color: #2aab5c; color:#ffffff;">'
    tableAdicionales += '          <td colspan="2" style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>SERVICIOS ADICIONALES</b></td>'   
    tableAdicionales += '      </tr-->'
    tableAdicionales += '      <tr style="background-color: #2aab5c; color:#ffffff;">'
    tableAdicionales += '          <td style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>SERVICIOS</b></td>'   
    tableAdicionales += '          <td style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>DETALLES</b></td>'   
    tableAdicionales += '      </tr>'
    tableAdicionales += '  </thead>'
    tableAdicionales += '  <tbody style="border: 1px solid #000; border-collapse: collapse;">'
    for add in listAdicionales:
        tableAdicionales += '      <tr style="border: 1px solid #000; border-collapse: collapse;">'
        tableAdicionales += '          <td style="text-align: left; width: 30%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">'+add['nombreServicio']+'</td>'
        tableAdicionales += '          <td style="text-align: left; width: 70%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>El precio del servicio adicional ya va incluido en precio mostrado en la seccion de Servicios.</b></td>'
        tableAdicionales += '      </tr>'
    tableAdicionales += '  </tbody>'
    tableAdicionales += '</table>'

    '''table += '<div>&nbsp;</div>'

    table  += '<table style="width: 100%; border: 1px solid;">'
    table += '  <thead class="text-white">'
    table += '      <tr style="background-color: #2aab5c; color:#ffffff;">'
    table += '          <td colspan="2" style="text-align: center; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>ADICIONALES</b></td>'   
    table += '      </tr>'
    table += '  </thead>'
    table += '  <tbody style="border: 1px solid #edeff1; border-collapse: collapse;">'
    table += '      <tr>'
    table += '          <td style="text-align: left; width: 80%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Carga Hazmat, porcentaje de incremento sobre la tarifa general.</td>'
    table += '          <td style="text-align: right; width: 20%; vertical-align: right; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>35%</b></td>'
    table += '      </tr>'
    table += '      <tr>'
    table += '          <td style="text-align: left; width: 80%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Carga Grado alimenticio, porcentaje de incremento sobre tarifa general.</td>'
    table += '          <td style="text-align: right; width: 20%; vertical-align: right; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>10%</b></td>'
    table += '      </tr>'
    table += '      <tr>'
    table += '          <td style="text-align: left; width: 80%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Carga Susceptible a Robo y/o custodiada, porcentaje de incremento sobre tarifa general.</td>'
    table += '          <td style="text-align: right; width: 20%; vertical-align: right; border: 1px solid #000; border-collapse: collapse; padding: 3px; "><b>15%</b></td>'
    table += '      </tr>'
    table += '  </tbody>'
    table += '</table>'

    table += '<div>&nbsp;</div>'

    table  += '<table style="width: 100%; border: 1px solid;">'
    table += '  <thead class="text-white">'
    table += '      <tr style="background-color: #2aab5c; color:#ffffff;">'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Concepto</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Tipo de Cobro</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Tipo de Carga</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Nissan</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>3 1/2</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Rabon</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Torton</b></td>'   
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: center; border: 1px solid #000000; border-collapse: collapse; padding: 3px; font-size: 12px;"><b>Caja de 53</b></td>'   
    table += '      </tr>'
    table += '  </thead>'
    table += '  <tbody style="border: 1px solid #edeff1; border-collapse: collapse;">'
    table += '      <tr>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Maniobras de carga/descarga</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Costo por servicio (2 personas)</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">General</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$610.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$1,265.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$2,310.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$2,640.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$3,780.00</td>'
    table += '      </tr>'
    table += '      <tr>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Hora Extra</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Costo por hora extra*</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">General</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$530.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$605.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$720.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$820.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$1,050.00</td>'
    table += '      </tr>'
    table += '      <tr>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Estadia x dia</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">Cobro máximo x dia*</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">General</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$3,200.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$3,630.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$4,290.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$4,950.00</td>'
    table += '          <td style="text-align: center; width: 12.5%; vertical-align: left; border: 1px solid #000; border-collapse: collapse; padding: 3px; ">$6,270.00</td>'
    table += '      </tr>'
    table += '  </tbody>'
    table += '</table>' '''

    table += '<div>&nbsp;</div>'

    tableClausulas += '<table style="width: 100%;>'
    tableClausulas += '  <tbody>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Mercancía viaja por riesgo y cuenta del cliente. Se puede contratar seguro, cotización independiente.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Solicitud de equipo con 48hrs de anticipación.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Todo flete realizado en falso tendra un costo del 80% sobre el valor del flete.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Otros destinos se cotizan por evento.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Esta tarifa puede tener variacion dependiendo del incremento en el costo del combustible y casetas.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Antes de generarse crédito las tres primeras operaciones deberán ser de contado.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">En pagos de contado se deberá generar el pago antes de entregarse la mercancía.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">En caso de requerirse reparto deberá notificarse previamente y se realizará el movimiento previa autorización y aprobación del costo por parte del cliente.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Tarifa Incluye Pistas.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Tarifa incluye ingreso a aeropuerto.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Tarifa en moneda nacional.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Interland se reserva el derecho de hacer recolecciones/entregas en zonas o ciudades centrales donde existen penalizaciones.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Las maniobras que se realicen fuera de planta/almacén con o sin restricción de tránsito, las multas serán absorbidas por el cliente.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">Cualquier multa/penalización por falta de permiso para circular, ya sea en origen/destino serán a cargo del cliente.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '      <tr>'
    tableClausulas += '          <td style="text-align: left; width: 100%; vertical-align: left;">No incluye servicios de palletizado, etiquetado, flejado, etc., estos servicios se cotizan por evento.</td>'
    tableClausulas += '      </tr>'
    tableClausulas += '  </tbody>'
    tableClausulas += '</table>'
 
    img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)
    
    html_content = render_to_string('pdf/tarifarioLTL.html', {"imgLogo": img_logo, "tabla":table, "tablaAdicionales":tableAdicionales, "tablaClausulas": tableClausulas, "origenes": listorigenes, "ddestinos":listdestinos, "mercancias":listMercancias, "ContactoCotizacion":listContactos, "modalidad":modalidad, "tiposervicio": tiposervicio, "usr":usuario, "contactoNombre": contacName, "contactoEmail": contacEmail, "contactoTelefono": contacTelefono, "contactoDescrip": contacDescription, "idCotizacion": idCotizacion})

    # Convertir el HTML a PDF
    result = io.BytesIO()
    pdf = pisa.CreatePDF(html_content, dest=result)

    # Comprobar si la conversión fue exitosa
    if not pdf.err:
        # Devolver el PDF como una respuesta HTTP con el tipo de contenido adecuado
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_pdf.pdf"'  # Para mostrar el PDF en el navegador
        return response

    return HttpResponse('Error al generar el PDF')

