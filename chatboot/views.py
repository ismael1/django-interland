from datetime import datetime, date
import json
from urllib.parse import urlparse
from django.db.models.query_utils import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

import requests
import locale
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os
from django.http import FileResponse

from .models import usuarios_chatboot, leds_chatboot, numeros_ejecutivos_chatboot
from .serializers import ChatbootSerializer, LedsSerializer, NumerosSerializer
from cotizaciones.models import Consecutivo, Tarifario
from cotizaciones.serializers import SerializerConsecutivo, SerializerTarifario

from catalogos.models import UnitBox, Terminos_Condiciones
from catalogos.serializers import UnitBoxSerializer, TerminosCondicionesSerializer

from inland_django.utils import compress_and_encode_image


class reporteLeads(viewsets.ModelViewSet):
    queryset = leds_chatboot.objects.all()
    serializer_class = LedsSerializer

class numerosAgentes(viewsets.ModelViewSet):
    queryset = numeros_ejecutivos_chatboot.objects.all()
    serializer_class = NumerosSerializer

@csrf_exempt
@api_view(['GET'])
def ListLeadsFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=leds_chatboot.objects.all().order_by('id')[data_start:data_end]
            count=leds_chatboot.objects.all().count()
        else:
            goodslist = leds_chatboot.objects.filter(Q(numero_agente__icontains=palabra) | Q(numero_usr__icontains=palabra) | Q(nombre_agente__icontains=palabra) | Q(nombre_usr__icontains=palabra)).order_by('id')[data_start:data_end]
            count=leds_chatboot.objects.filter(Q(numero_agente__icontains=palabra) | Q(numero_usr__icontains=palabra) | Q(nombre_agente__icontains=palabra) | Q(nombre_usr__icontains=palabra))[data_start:data_end].count()

        goods_ser=LedsSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListNumerosFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=numeros_ejecutivos_chatboot.objects.all().order_by('id')[data_start:data_end]
            count=numeros_ejecutivos_chatboot.objects.all().count()
        else:
            goodslist = numeros_ejecutivos_chatboot.objects.filter(Q(nombre__icontains=palabra) | Q(apellido__icontains=palabra) | Q(numero_agente__icontains=palabra) | Q(servicio__icontains=palabra)).order_by('id')[data_start:data_end]
            count=numeros_ejecutivos_chatboot.objects.filter(Q(nombre__icontains=palabra) | Q(apellido__icontains=palabra) | Q(numero_agente__icontains=palabra) | Q(servicio__icontains=palabra))[data_start:data_end].count()

        goods_ser=NumerosSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt 
@api_view(['POST','GET'])
def numerosAgentesAlta(request):
    data = json.loads(request.body)
    
    nombre = data['datos']['nombre']
    apellido = data['datos']['apellido']
    numero_agente = data['datos']['numero_agente']
    servicio = int(data['datos']['servicio'])
    es_gerente = bool(data['datos']['es_gerente'])
    usuario_alta = data['datos']['usuario_alta']
    resp = {}
    
    valida = numeros_ejecutivos_chatboot.objects.filter(Q(numero_agente=numero_agente) & Q(es_gerente=es_gerente) & Q(servicio=servicio)).count()

    if valida > 0:
        resp = {'insert':False,'msg':'El Ejecutivo que intentas agregar ya esta dado de alta, verifícalo por favor.'}
    else:

        create = numeros_ejecutivos_chatboot.objects.create(nombre = nombre, apellido=apellido, numero_agente=numero_agente, servicio=servicio,es_gerente=es_gerente,usuario_alta=usuario_alta)
        
        resp = {'insert':True,'msg':'Ejecutivo cargado correctamente'}

    return Response(resp)

@csrf_exempt 
@api_view(['POST','GET'])
def leadAlta(request):
    data = json.loads(request.body)
    print(data['datos'][0])
    nombre_agente = str(data['datos'][0]['nombre_agente'])
    numero_agente = str(data['datos'][0]['numero_agente'])
    mensaje_boot = str(data['datos'][0]['mensaje_boot'])
    numero_usr = str(data['datos'][0]['numero_usr'])
    nombre_usr = str(data['datos'][0]['nombre_usr'])
    usuario_alta = str(data['datos'][0]['usuario_alta'])
    resp = {}
    
    conteo = leds_chatboot.objects.filter(Q(numero_agente=numero_agente)).filter(Q(fecha=date.today())).aggregate(Max('conteo'))['conteo__max']
    print(conteo)
    if(conteo is None):
        conteo = 0
    conteo = conteo +1


    create = leds_chatboot.objects.create(conteo = conteo, mensaje_boot=mensaje_boot, numero_agente=numero_agente, nombre_usr=nombre_usr,numero_usr=numero_usr,nombre_agente=nombre_agente, usuario_alta=usuario_alta)
        
    resp = {'insert':True,'msg':'Lead cargado correctamente'}

    return Response(resp)

@csrf_exempt 
@api_view(['POST','GET'])
def leadsReporte(request):
    data = json.loads(request.body)
    
    fecha_ini = data['datos']['fecha_ini']
    fecha_fin = data['datos']['fecha_fin']
    indice = 0
    result = []
    
    resp = leds_chatboot.objects.filter(Q(fecha__range=(fecha_ini, fecha_fin))).order_by('fecha')
    re = LedsSerializer(resp, many=True)
    for r in re.data:
        indice = indice + 1
        obj = {'No.':indice, 'Número de Agente':r['numero_agente'],'Nombre de Agente':r['nombre_agente'],'Conteo de Leads':r['conteo'],'Nombre de Cliente':r['nombre_usr'],'Número de Cliente':r['numero_usr'], 'Canal de Entrada':r['canal_entrada'], 'Fecha del Lead':r['fecha']}
        result.append(obj)

    return Response(result)

@csrf_exempt
@api_view(['GET'])
def listNumeros(request):

        
    goodslist=numeros_ejecutivos_chatboot.objects.filter(Q(es_gerente=False)).order_by('id')
    goods_ser=NumerosSerializer(goodslist,many=True)

    return Response(goods_ser.data)

@csrf_exempt 
@api_view(['POST'])
def validaUsuarioChatboot(request):

    resp = {}
    data = json.loads(request.body)
    # Recuperar el dato telefono
    telefono = data.get('telefono')
    #telefono = request.POST.get('telefono')
    print(telefono)
    
    if telefono != '':
        count = usuarios_chatboot.objects.filter(Q(telefono=telefono)).count()
        if count == 0:
            usuarios_chatboot.objects.create(telefono = telefono, primera_vez = 0)
            resp = {"mensaje": 0}

            actualiza = usuarios_chatboot.objects.get(telefono=telefono)
            actualiza.primera_vez = 1
            actualiza.save()
        else:
            datos = usuarios_chatboot.objects.values('primera_vez', 'date_inicio').filter(telefono=telefono)
            serializer = ChatbootSerializer(datos, many=True)

            fecha_actual = datetime.now().date()
            fecha_bd = serializer.data[0]['date_inicio']

            if isinstance(fecha_bd, str):
                fecha_bd = datetime.strptime(fecha_bd, '%Y-%m-%d').date()
            
            print(fecha_actual, 'Fecha Actual')
            print(fecha_bd, 'Fecha Base')

            if fecha_actual == fecha_bd:
                resp = {"mensaje": serializer.data[0]['primera_vez']}
            elif fecha_actual > fecha_bd:
                resp = {"mensaje": 0}

            actualiza = usuarios_chatboot.objects.get(telefono=telefono)
            actualiza.primera_vez = 1
            actualiza.date_inicio = fecha_actual
            actualiza.save()

    else:
        resp = {"mensaje": 1}

    
    return Response(resp)

@csrf_exempt 
@api_view(['POST'])
def generaCotizacionChatboot(request):

    resp = {}
    data = json.loads(request.body)
    # Recuperar el dato telefono
    telefono = data.get('telefono')
    origen = data.get('origen')
    destino = data.get('destino')
    transporte = data.get('transporte')
    serv = str(data.get('servicio'))
    servicios = serv.upper()
    peso = float(data.get('peso'))
    volumen = float(data.get('volumen'))
    mercancia = data.get('mercancia')
    cliente = data.get('cliente')

    km = ''
    direccionCompletaOrigen = ''
    direccionCompletaDestino = ''
    estadoOrigen = ''
    estadoDestino = ''
    API_KEY = 'AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y'
    tablaServ = ''
    tablaClausulas = ''
    unidades = []
    idUnidad = 0
    unidadSeleccionada = ''
    precioUnidad = 0.0

    numeroBoot = '5215541708682'
    numeroAgente = ''
    mensajeAgente = ''
    archivoAgente = ''

    '''if transporte == 'Aereo' or transporte == 'Aéreo' or transporte == 'aer':
        numeroAgente = '5215636580608'
        transporte = 'Aéreo'
    elif transporte == 'Marítimo' or transporte == 'Maritimo' or transporte == 'mar':
        numeroAgente = '5215636580608'
        transporte = 'Marítimo'
    elif transporte == 'Terrestre' or transporte == 'ter':
        numeroAgente = '5215636580608'
        transporte = 'Terrestre'''

    consecutivo = Consecutivo.objects.all().order_by("-id")[:1]
    cons = SerializerConsecutivo(consecutivo, many=True)

    idConsecutivo = cons.data[0]['id']
    numConsecutivo = int(cons.data[0]['numero']) + 1
    controlConse = cons.data[0]['control']
    fc = cons.data[0]['fecha']
    fechaConsecutivo = datetime.strptime(fc, "%Y-%m-%d")
    ultimosDg = fechaConsecutivo.strftime("%y")

    folioCotizacion = controlConse+str(ultimosDg)+str(numConsecutivo).zfill(6)
    
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origen}&destination={destino}&mode=driving&avoid=tolls&key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        dato = data['routes'][0]['legs'][0]['distance']['text']
        dato = dato.split(" ")
        km = dato[0]
        km = float(km.replace(",",""))

    print(km) #Obtenemos km
    direccion_codificada_origen = requests.utils.quote(origen)
    response_origen = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion_codificada_origen}&key={API_KEY}")
    # Verificar si la solicitud fue exitosa
    if response_origen.status_code == 200:
        data = response_origen.json()
        # Verificar si se encontró una ubicación
        if data.get('results') and len(data['results']) > 0:
            # Obtener la dirección completa
            direccion_completa = data['results'][0]['formatted_address']
            for estado in data['results'][0]['address_components']:
                for tipo in estado['types']:
                    if tipo == 'administrative_area_level_1':
                        if estado['long_name'] == 'Ciudad de México':
                            estadoOrigen = estado['short_name']
                        else:
                            estadoOrigen = estado['long_name']
            #print(data['results'][0],'datosO')
            direccionCompletaOrigen = direccion_completa
            
        else:
            print("No se pudo encontrar una dirección para la ubicación proporcionada.")
    else:
        print("Error al realizar la solicitud:", response_origen.status_code)

    print(direccionCompletaOrigen) #Obtenemos Direccion completa Origen

    direccion_codificada_destino = requests.utils.quote(destino)
    response_destino = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion_codificada_destino}&key={API_KEY}")
    # Verificar si la solicitud fue exitosa
    if response_destino.status_code == 200:
        data = response_destino.json()
        # Verificar si se encontró una ubicación
        if data.get('results') and len(data['results']) > 0:
            # Obtener la dirección completa
            direccion_completa = data['results'][0]['formatted_address']
            for estado in data['results'][0]['address_components']:
                for tipo in estado['types']:
                    if tipo == 'administrative_area_level_1':
                        if estado['long_name'] == 'Ciudad de México':
                            estadoDestino = estado['short_name']
                        else:
                            estadoDestino = estado['long_name']
            #print(data['results'][0],'datosD')
            direccionCompletaDestino = direccion_completa
            
        else:
            print("No se pudo encontrar una dirección para la ubicación proporcionada.")
    else:
        print("Error al realizar la solicitud:", response_destino.status_code)

    print(direccionCompletaDestino) #Obtenemos Direccion completa Destino

    units = UnitBox.objects.filter(mostrarLista=1).order_by('peso_bruto_total')
    unidades = UnitBoxSerializer(units, many=True)
    unidades = unidades.data

    for un in unidades:
        # Acceder a los campos de la unidad serializada
        pesTotUn = float(un['peso_bruto_total'])
        volTotUn = float(un['capacidad_vol'])

        if pesTotUn >= peso and volTotUn >= volumen:
            print(pesTotUn, '>=', peso, 'and', volTotUn, '>=', volumen)
            idUnidad = int(un['id'])
            unidadSeleccionada = un['name']
            precioUnidad = float(un['precio_kilometraje'])
            break

    print(unidadSeleccionada, precioUnidad) #Obtenemos el tipo de unidad segun su peso y volumen

    if servicios == 'LTL':

        tarifaFlete = 0.0
        tarifario = Tarifario.objects.filter(origen__icontains=estadoOrigen).filter(destino__icontains=estadoDestino).filter(aplica='LTL')
        tarifarioSer = SerializerTarifario(tarifario,many=True)
        tarifarioSer = tarifarioSer.data

        for tarifa in tarifarioSer:
            tarifaFlete = float(tarifa['flete_nacional'])

        pesoVolumetrico = peso/350

        if pesoVolumetrico >= volumen:
            precioFlete = pesoVolumetrico * tarifaFlete
        else:
            precioFlete = volumen * tarifaFlete
        
        precioIva = precioFlete * 0.16
        precioTotal = precioFlete + precioIva

    elif servicios == 'FTL':
        precioFlete = precioUnidad * km
        precioIva = precioFlete * 0.16
        precioTotal = precioFlete + precioIva

    elif servicios == 'FCL':
        precioFlete = precioUnidad * km
        precioIva = precioFlete * 0.16
        precioTotal = precioFlete + precioIva

    tablaServ = ''
    tablaServ +='<table class="tg">'
    tablaServ +='    <thead></thead>'
    tablaServ +='    <tbody>'
    tablaServ +='        <tr>'
    tablaServ +='        <td class="seccion" colspan="4" style="text-align: left;">Servicios</td>'
    tablaServ +='    </tr>'
    tablaServ +='    <tr>'
    tablaServ +='        <td class="espacio" colspan="4"></td>'
    tablaServ +='    </tr>'
    tablaServ +='    <tr>'
    tablaServ +='        <td class="" colspan="4">'
    tablaServ +='            <table>'
    tablaServ +='                <tr>'
    tablaServ +='                    <th>CONCEPTO</th>'
    tablaServ +='                    <th>SUBTOTAL</th>'
    tablaServ +='                    <th>IVA</th>'
    tablaServ +='                    <th>TOTAL</th>'
    tablaServ +='                </tr>'
    tablaServ +='                    <tr>'
    tablaServ +='                        <td style="text-align: center;">FLETE NACIONAL</td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioFlete)+'</td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioIva)+'</td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioTotal)+'</td>'
    tablaServ +='                    </tr>'
    tablaServ +='                    <tr>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: right;"><b>SUBTOTAL:</b></td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioFlete)+'</td>'
    tablaServ +='                    </tr>'
    tablaServ +='                    <tr>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: right;"><b>I.V.A.:</b></td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioIva)+'</td>'
    tablaServ +='                    </tr>'
    tablaServ +='                    <tr>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: center;"></td>'
    tablaServ +='                        <td style="text-align: right;"><b>TOTAL:</b></td>'
    tablaServ +='                        <td style="text-align: center;">'+formatear_moneda(precioTotal)+'</td>'
    tablaServ +='                    </tr>'
    tablaServ +='            </table>'
    tablaServ +='        </td>'
    tablaServ +='    </tr>'
    tablaServ +='</tbody>'
    tablaServ +='</table>'

    terminos = Terminos_Condiciones.objects.filter(aplica__icontains=servicios).order_by('orden')
    term = TerminosCondicionesSerializer(terminos, many=True)
    term = term.data

    tablaClausulas = ''
    tablaClausulas +='<table class="tg">'
    tablaClausulas +='    <thead></thead>'
    tablaClausulas +='    <tbody>'
    tablaClausulas +='        <tr>'
    tablaClausulas +='        <td class="seccion" colspan="4" style="text-align: left;">Clausulas</td>'
    tablaClausulas +='    </tr>'
    tablaClausulas +='    <tr>'
    tablaClausulas +='        <td class="espacio" colspan="4"></td>'
    tablaClausulas +='    </tr>'
    tablaClausulas +='    <tr>'
    tablaClausulas +='        <td class="" colspan="4">'
    tablaClausulas +='          <ol type="A">'
    for t in term:
        tablaClausulas +='        <li>'+t['condicion']+'</li>'
    tablaClausulas +='          </ol>'
    tablaClausulas +='        </td>'
    tablaClausulas +='    </tr>'
    tablaClausulas +='</tbody>'
    tablaClausulas +='</table>'

    img_logo = compress_and_encode_image('cotizaciones/templates/img/logo_i.png', 75)
    img_cinta = compress_and_encode_image('cotizaciones/templates/img/Interland-cinta.png', 75)
    nombre = "Cotizacion-"+folioCotizacion+".pdf"

    html_content = render_to_string('pdf/cotizacion_chatboot.html', {"folio":folioCotizacion, "imgCinta": img_cinta,"imgLogo": img_logo, "origen": direccionCompletaOrigen, "destino":direccionCompletaDestino, "transporte": transporte, "transporte": transporte, "servicios":servicios, "peso":peso, "volumen":volumen, "mercancia": mercancia, "cliente":cliente, "telefono":telefono, "listaServ":tablaServ, "listaClau":tablaClausulas})

    name_file = "media/cotizacion_chatboot/"+nombre

    result_file = open(name_file, "w+b")

    pisa_status = pisa.CreatePDF(html_content,dest=result_file)

    result_file.close()

    '''INICIA PROCESO PARA ENVIAR MENSAJE A AGENTES'''

    array_palabras_usa = ["USA", "usa", "Estados Unidos", "estados unidos", "united states", "United States"]
    array_palabras_cenam = ["Mexico", "México", "mexico", "méxico"]

    for palabra in array_palabras_usa:
        if palabra in origen and transporte == 'Terrestre' or palabra in destino and transporte == 'Terrestre':
            numeroAgente = '5215532235754' #Sergio

    if transporte == 'Aéreo' or transporte == 'aéreo' or transporte == 'Aereo' or transporte == 'aereo' or transporte == 'Marítimo' or transporte == 'marítimo' or transporte == 'Maritimo' or transporte == 'maritimo':
        numeroAgente = '5215539673033' #Mario

    
    for palabra in array_palabras_cenam:
        if palabra in origen or palabra in destino:

            if float(telefono) % 2 == 0:
                numeroAgente = '5215545985480' #Juan V
            else:
                numeroAgente = '5215545309087' #Patricia
    

    mensajeAgente = 'Hola, el usuario *'+cliente+'* con número telefónico: '+telefono+' acaba de realizar una cotización de tipo: *'+transporte+'* su origen es: *'+origen+'*, su destino es: *'+destino+'*, el servicio solicitado es: *'+servicios+'*, el peso total de su mercancia es: *'+str(peso)+'kg*, el volumen total es de: *'+str(volumen)+'m3*, y desea transportar: *'+mercancia+'*.'
    archivoAgente = 'http://sicolog.ifreight.business/media/cotizacion_chatboot/Cotizacion-'+folioCotizacion+'.pdf'

    url = "https://api.botmaker.com/v2.0/chats-actions/send-messages"

    payload = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": numeroAgente
        },
        "messages": [
            {
                "text": 'Folio: '+folioCotizacion,
                "media": {
                    "mimeType": "application/pdf",
                    "url": archivoAgente
                }
            }
        ]
    }

    payload2 = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": numeroAgente
        },
        "messages": [
            {
                "text": mensajeAgente
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoiaW50ZXJsYW5kIiwibmFtZSI6Ik1pZ3VlbCIsImFwaSI6dHJ1ZSwiaWQiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIiwiZXhwIjoxODYwMjYxNzA5LCJqdGkiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIn0.g4Etrxyv_5jyG_iF2GJ6_rU0Ta16Hos0h8g1CApKfgtCwgygM4ePN5nPZrAofCL_JHONuhIFGZ9v2vWQ4VtL8w"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response2 = requests.request("POST", url, json=payload2, headers=headers)

    print(response.text, 'Envio mensaje Whatsapp FILE')
    print(response2.text, 'Envio mensaje Whatsapp TEXT')

    if os.path.exists(name_file):
        resp = {"mensaje": 1, "folio":folioCotizacion}
        #with open(name_file, 'rb') as archivo_pdf:
            #return FileResponse(archivo_pdf, as_attachment=True, filename=os.path.basename(name_file))
    else:
        #return Response({"mensaje": 'Se encontro un error al generar tu cotizacion, se te enlazará con un agente, espera un momento'})
        resp = {"mensaje": 0, "folio":folioCotizacion}

    return Response(resp)

def formatear_moneda(cifra):
    # Establecer la configuración local para formatear como moneda
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    # Formatear la cifra como moneda utilizando la configuración local
    cifra_formateada = locale.currency(cifra, grouping=True)

    return cifra_formateada

@csrf_exempt 
@api_view(['POST'])
def eliminaPDF(request):

    resp = {}
    data = json.loads(request.body)
    # Recuperar el dato telefono
    telefono = data.get('telefono')
    folio = data.get('folio')
    
    nombre = "Cotizacion-"+folio+".pdf"
    name_file = "media/cotizacion_chatboot/"+nombre

    if os.path.exists(name_file):
        # Eliminar el archivo
        os.remove(name_file)
    

    consecutivo = Consecutivo.objects.all().order_by("-id")[:1]
    cons = SerializerConsecutivo(consecutivo, many=True)

    idConsecutivo = cons.data[0]['id']
    numConsecutivo = int(cons.data[0]['numero']) + 1

    consecutivo = Consecutivo.objects.get(id=idConsecutivo)
    consecutivo.numero = numConsecutivo
    consecutivo.save()
    
    resp = {"mensaje": 1}

    return Response(resp)

@csrf_exempt 
@api_view(['POST'])
def validaCurriculumChatboot(request):

    resp = {}
    data = json.loads(request.body)
    # Recuperar el dato telefono
    telefono = data.get('telefono')
    document = data.get('document')
    print(document)
    print(telefono)
    
        
    resp = {"mensaje": 1}

    
    return Response(resp)

@csrf_exempt 
@api_view(['POST'])
def enviaDatosAgenteChatboot(request):

    data = json.loads(request.body)
    # Recuperar el dato telefono
    telefono = data.get('telefono')
    cliente = data.get('cliente')
    tipoPuesto = int(data.get('tipoPuesto'))
    puesto = ''
    documento = data.get('documento')

    numeroBoot = '5215541708682'
    numeroAgente = '5215543281619'
    mensajeAgente = ''
    archivoAgente = ''
    mimeType = ''


    if tipoPuesto == 1:
        puesto = 'Auxiliar de Almacén y Maniobras'
    elif tipoPuesto == 2:
        puesto = 'Pricing Analyst'
    elif tipoPuesto == 3:
        puesto = 'Community Manager'
    else:
        puesto = 'que se adecue a su CV'


    mensajeAgente = 'Hola Damaris! El interesado *'+cliente+'* con número telefónico: '+telefono+' acaba de '
    archivoAgente = documento

    parsed_url = urlparse(archivoAgente)
    path = parsed_url.path
    filename = os.path.basename(path)
    file_name_parts = filename.split('.')
    if len(file_name_parts) > 1:
        extension = file_name_parts[-1].lower()
    else:
        print("No se pudo determinar la extensión del archivo desde la URL.")

    # Validar la extensión
    allowed_extensions = ['pdf', 'docx', 'doc', 'png', 'jpeg', 'jpg']
    if extension in allowed_extensions:
        if extension == 'pdf':
            mimeType = 'application/pdf'
        elif extension == 'docx':
            mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif extension == 'docx':
            mimeType = 'application/msword'
        elif extension == 'png':
            mimeType = 'image/png'
        elif extension == 'jpeg' or extension == 'jpg':
            mimeType = 'image/jpeg'

    url = "https://api.botmaker.com/v2.0/chats-actions/send-messages"

    payload = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": numeroAgente
        },
        "messages": [
            {
                "text": 'CV-'+cliente,
                "media": {
                    "mimeType": mimeType,
                    "url": archivoAgente
                }
            }
        ]
    }

    payload2 = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": numeroAgente
        },
        "messages": [
            {
                "text": mensajeAgente
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoiaW50ZXJsYW5kIiwibmFtZSI6Ik1pZ3VlbCIsImFwaSI6dHJ1ZSwiaWQiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIiwiZXhwIjoxODYwMjYxNzA5LCJqdGkiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIn0.g4Etrxyv_5jyG_iF2GJ6_rU0Ta16Hos0h8g1CApKfgtCwgygM4ePN5nPZrAofCL_JHONuhIFGZ9v2vWQ4VtL8w"
    }

    response2 = requests.request("POST", url, json=payload2, headers=headers)
    response = requests.request("POST", url, json=payload, headers=headers)    

    print(response.text, 'Envio mensaje Whatsapp FILE')
    print(response2.text, 'Envio mensaje Whatsapp TEXT')
    
    if response.text.webhookNotificationId != '' and response2.text.webhookNotificationId != '':
        resp = {"mensaje": 1}
    else:
        resp = {"mensaje": 0}
    
    return Response(resp)


def envia_mensajes(datos):
    data = json.loads(datos)
    #DATOS AGENTE Y CLIENTE
    
    id_age= data.get("id_agente")
    telefonoAgente = data.get("numero_agente")
    nombreAgente =data.get("nombre_agente")
    apellidoAgente = data.get("apellido_agente")
    tipoServicio =data.get("servicio")
    cliente =data.get("nombre_lead")
    telefono =data.get("numero_lead")
    nombreServicio = data.get("nombreServicio")
    canal_entrada = data.get("canal_entrada")
    numeroBoot = '5215541708682'
    url = "https://api.botmaker.com/v2.0/chats-actions/send-messages"
    headers = {
        "Content-Type": "application/json",
        "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoiaW50ZXJsYW5kIiwibmFtZSI6Ik1pZ3VlbCIsImFwaSI6dHJ1ZSwiaWQiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIiwiZXhwIjoxODgxMTY5OTk0LCJqdGkiOiJTSUFsUG1Ea0JOVDBBQWtubVVlWGMzOWkxWHMyIn0.Uhs-HEsh_Reu5bBwhFy6v9sVbWLA6k1dUDs0tHOvzn_UQhbEfEU4E63iHjoTl4vSr8fG_jlMd5Z8Ja3BN0f_gw"
    }

    conteo_numero_valida = numeros_ejecutivos_chatboot.objects.filter(Q(numero_agente=telefono)).count()

    agente = numeros_ejecutivos_chatboot.objects.filter(Q(servicio=tipoServicio)).filter(Q(es_gerente=False))
    age = NumerosSerializer(agente, many=True)
    gerente = numeros_ejecutivos_chatboot.objects.filter(Q(servicio=tipoServicio)).filter(Q(es_gerente=True))
    ger = NumerosSerializer(gerente, many=True)

    telefonoAgente = telefonoAgente
    nombreAgente = nombreAgente + ' ' + apellidoAgente
    telefonoGerente = ger.data[0]['numero_agente']
    nombreGerente = ger.data[0]['nombre'] + ' ' + ger.data[0]['apellido']

    fecha_actual = date.today()

    conteo = leds_chatboot.objects.filter(Q(numero_agente=telefonoAgente)).filter(Q(fecha=fecha_actual)).aggregate(Max('conteo'))['conteo__max']
    print(conteo, 'valida conteo agente')
    if(conteo is None):
        conteo = 0
    conteo = conteo +1

    #mensajeAgente = 'Hola '+nombreAgente+'! El cliente *'+cliente+'* con número telefónico: +'+telefono+' acaba de solicitar informacion de un servicio '+nombreServicio
    #mensajeGerente = 'Hola '+nombreGerente+'! Te informamos que el cliente *'+cliente+'* con número telefónico: +'+telefono+' acaba de solicitar informacion de un servicio '+nombreServicio+'. Este cliente ya esta siendo atendido por '+nombreAgente
    mensajeAgente = '*'+nombreAgente+'*: ¡Bien hecho! acabas de recibir un nuevo lead No. *'+str(conteo)+'*, Nombre del cliente: *'+cliente+'*, Número Telefónico: '+telefono+'. Recuerda registrar tus leads por día o semana para no perder tu progreso.'
    mensajeGerente = '*'+nombreGerente+'*: ¡Nuevo cliente! hemos recibido una nueva solicitud de información para un servicio '+nombreServicio+' el nombre del cliente es *'+cliente+'* con numero telefónico: '+telefono+', este cliente está siendo atendido por: *'+nombreAgente+'*'


    payload1 = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": telefonoAgente
        },
        "messages": [
            {
                "text": mensajeAgente
            }
        ]
    }

    response1 = requests.request("POST", url, json=payload1, headers=headers)
    print(response1)
    
    payload2 = {
        "chat": {
            "channelId": numeroBoot,
            "contactId": telefonoGerente
        },
        "messages": [
            {
                "text": mensajeGerente
            }
        ]
    }

    response2 = requests.request("POST", url, json=payload2, headers=headers)  
    print(response2)

    if conteo_numero_valida == 0:
        leds_chatboot.objects.create(conteo = conteo, numero_agente = telefonoAgente, nombre_agente=nombreAgente, mensaje_boot = mensajeAgente, numero_usr = telefono, nombre_usr = cliente, canal_entrada = canal_entrada)

    return Response({"info": True})

@csrf_exempt 
@api_view(['POST','GET'])
def obtener_agente_rotativo(request):
    data = json.loads(request.body)
    telefono = data.get('telefono')
    cliente = data.get('nombreCliente')
    tipoServicio = int(data.get('tipoServicio'))
    nombreServicio = data.get('nombreServicio')
    canal_entrada = data.get('canal_entrada')
    telefonoAgente = ''
    nombreAgente = ''
    infoAgente = {}
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    # Filtrar los leads que coincidan con el número de teléfono y la fecha actual
    existencia_lead = leds_chatboot.objects.filter(Q(numero_usr=telefono), Q(date_create=fecha_actual))[:1]
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
                        "servicio" : tipoServicio,  
                        "nombre_lead" : cliente,
                        "numero_lead" : telefono,
                        "nombreServicio": nombreServicio,
                        "canal_entrada":canal_entrada,
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
                        "servicio" : tipoServicio,  
                        "nombre_lead" : cliente,
                        "numero_lead" : telefono,
                        "nombreServicio": nombreServicio,
                        "canal_entrada":canal_entrada,
                    }


    datos = json.dumps(infoAgente)
    envia_mensajes(datos)
    return Response(datos)
