from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from django.db.models.query_utils import Q
from django.db.models import Count

from django.db.models import F, OuterRef, Subquery

from .models import Envio, Permisos, UnitBox, Customs, ClaveProdServ, ClaveUnidad, Producto, Servicio, Puesto, Responsable, Envio, Modulos, Embalaje, Terminos_Condiciones, Geocercas, tipo_cliente, tipo_persona, tipo_empresa, regimen_fiscal, metodo_pago, forma_pago, Zonas_Tarifas
from .serializers import SerializerUnitBox, UnitBoxSerializer, CustomsSerializer, ClaveProdServSerializer, ClaveUnidadSerializer, ProductoSerializer, ServicioSerializer, PuestoSerializer, ResponsableSerializer, EnvioSerializer, ModulosSerializer, PermisosSerializer, EmbalajeSerializer, TerminosCondicionesSerializer, GeocercasSerializer, tipo_clienteSerializer, tipo_personaSerializer, tipo_empresaSerializer, regimen_fiscalSerializer, metodo_pagoSerializer, forma_pagoSerializer, zona_tarifasSerializer
import json
class UnitBoxtViewSet(viewsets.ModelViewSet):
    queryset = UnitBox.objects.all()
    serializer_class = UnitBoxSerializer

class EmbalajesViewSet(viewsets.ModelViewSet):
    queryset = Embalaje.objects.all().exclude(estatus=4)
    serializer_class = EmbalajeSerializer

class  ClaveProdServViewSet(viewsets.ModelViewSet):
    queryset = ClaveProdServ.objects.all()
    serializer_class = ClaveProdServSerializer

class ClaveUnidadViewSet(viewsets.ModelViewSet):
    queryset = ClaveUnidad.objects.all()
    serializer_class = ClaveUnidadSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer

class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer

class GeocercasViewSet(viewsets.ModelViewSet):
    queryset = Geocercas.objects.all()
    serializer_class = GeocercasSerializer


@csrf_exempt
@api_view(['POST','GET'])
def tipo_clienteViewSet(request):
    
    tc = tipo_cliente.objects.filter(estatus=1).order_by('id_tipo_cliente')
    serializer = tipo_clienteSerializer(tc, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST','GET'])
def tipo_personaViewSet(request):
    
    tp = tipo_persona.objects.filter(estatus=1).order_by('id_tipo_persona')
    serializer = tipo_personaSerializer(tp, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST','GET'])
def tipo_empresaViewSet(request):
    
    te = tipo_empresa.objects.filter(estatus=1).order_by('id_tipo_empresa')
    serializer = tipo_empresaSerializer(te, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST','GET'])
def regimen_fiscalViewSet(request):
    
    rf = regimen_fiscal.objects.filter(estatus=1).order_by('id_regimen_fiscal')
    serializer = regimen_fiscalSerializer(rf, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST','GET'])
def metodo_pagoViewSet(request):
    
    mp = metodo_pago.objects.filter(estatus=1).order_by('id_metodo_pago')
    serializer = metodo_pagoSerializer(mp, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST','GET'])
def forma_pagoViewSet(request):
    
    fp = forma_pago.objects.filter(estatus=1).order_by('id_forma_pago')
    serializer = forma_pagoSerializer(fp, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST','GET'])
def listBox(request):
    dato = request.data.get('data')
    modalidad = request.data.get('modalidad')

    if dato:
        box = UnitBox.objects.filter(servicio_aplica__contains=modalidad).filter(mostrarLista=1).order_by('capacidad_vol')
        serializer = SerializerUnitBox(box, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})


@csrf_exempt 
@api_view(['POST', 'GET'])
def searchAduana(request):
    dato = request.data.get('data')
    if dato:
        aduana = Customs.objects.filter(Q(origen__icontains=dato) | Q(destino__icontains=dato))
        serializer = CustomsSerializer(aduana, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})


@csrf_exempt 
@api_view(['POST', 'GET'])
def getNameAduana(request):
    dato = request.data.get('data')
    if dato:
        aduana = Customs.objects.get(id=dato)
        serializer = CustomsSerializer(aduana)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt
@api_view(['GET'])
def ListProductoFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=Producto.objects.filter(Q(estatus=0))[data_start:data_end]
            count=Producto.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Producto.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(unidad__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count=Producto.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(unidad__icontains=palabra)).filter(Q(estatus=0)).count()

        red = str(goodslist.query)

        goods_ser=ProductoSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListModulosFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=Modulos.objects.filter(Q(estatus=0) | Q(estatus=1)).order_by('nombre')[data_start:data_end]
            count= Modulos.objects.filter(Q(estatus=0) | Q(estatus=1)).order_by('nombre').count()
        else:
            goodslist = Modulos.objects.filter(Q(nombre__icontains=palabra)).filter(Q(estatus=0) | Q(estatus=1)).order_by('nombre')[data_start:data_end]
            count= goodslist.count()

        goods_ser=ModulosSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListServicioFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=Servicio.objects.filter(Q(estatus=0))[data_start:data_end]
            count=Servicio.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Servicio.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(duracion__icontains=palabra) | Q(tiempo__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count=Servicio.objects.filter(Q(nombreProductoServicios__icontains=palabra) | Q(duracion__icontains=palabra) | Q(tiempo__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()

        goods_ser=ServicioSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListClaveFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=ClaveProdServ.objects.filter(Q(estatus=0))[data_start:data_end]
            count=ClaveProdServ.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = ClaveProdServ.objects.filter(Q(clave_prodserv__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count=ClaveProdServ.objects.filter(Q(clave_prodserv__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()

        goods_ser=ClaveProdServSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })
        
@csrf_exempt
@api_view(['GET'])
def ListClaveUnidadFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=ClaveUnidad.objects.filter(Q(estatus=0))[data_start:data_end]
            count=ClaveUnidad.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = ClaveUnidad.objects.filter(Q(claveUnidad__icontains=palabra) | Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra) | Q(nota__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count=ClaveUnidad.objects.filter(Q(claveUnidad__icontains=palabra) | Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra) | Q(nota__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()

        goods_ser=ClaveUnidadSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListPuestoFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist=Puesto.objects.filter(Q(estatus=0))[data_start:data_end]
            count=Puesto.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Puesto.objects.filter(Q(nombre__icontains=palabra) | Q(tipo__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count = Puesto.objects.filter(Q(nombre__icontains=palabra) | Q(tipo__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()
        goods_ser=PuestoSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListResponsableFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Responsable.objects.filter(Q(estatus=0))[data_start:data_end]
            count = Responsable.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Responsable.objects.filter(Q(nombre__icontains=palabra) | Q(apellidos__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count = Responsable.objects.filter(Q(nombre__icontains=palabra) | Q(apellidos__icontains=palabra)).filter(Q(estatus=0)).count()
        goods_ser=ResponsableSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListEnvioFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Envio.objects.filter(Q(estatus=0))[data_start:data_end]
            count = Envio.objects.filter(Q(estatus=0)).count()
        else:
            goodslist = Envio.objects.filter(Q(nombre__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end]
            count = Envio.objects.filter(Q(nombre__icontains=palabra)).filter(Q(estatus=0))[data_start:data_end].count()
        goods_ser = EnvioSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListUnidadFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist=UnitBox.objects.filter(Q(mostrarLista=0) | Q(mostrarLista=1)).order_by('id')[data_start:data_end]
            count=UnitBox.objects.filter(Q(mostrarLista=0) | Q(mostrarLista=1)).count()
        else:
            goodslist = UnitBox.objects.filter(Q(clave_prodserv__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(mostrarLista=0) | Q(mostrarLista=1)).order_by('id')[data_start:data_end]
            count=UnitBox.objects.filter(Q(clave_prodserv__icontains=palabra) | Q(descripcion__icontains=palabra)).filter(Q(mostrarLista=0) | Q(mostrarLista=1))[data_start:data_end].count()

        goods_ser=UnitBoxSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt 
@api_view(['POST', 'GET'])
def searchPS(request):
    dato = request.data.get('data')

    if dato:
        busqueda = ClaveProdServ.objects.filter(descripcion__icontains=dato).annotate(total=Count('descripcion'))
        serializer = ClaveProdServSerializer(busqueda, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST', 'GET'])
def searchUnit(request):
    dato = request.data.get('data')

    if dato:
        busqueda = ClaveUnidad.objects.values('claveUnidad','nombre').filter(claveUnidad__icontains=dato.replace(" ", ""))
        serializer = ClaveUnidadSerializer(busqueda, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

@csrf_exempt 
@api_view(['POST', 'GET'])
def detalleUnit(request):
    dato = request.data.get('data')

    if dato:
        busqueda = ClaveProdServ.objects.values('descripcion').filter(clave_prodserv=dato)
        serializer = ClaveProdServSerializer(busqueda, many=True)
        return Response(serializer.data)
    else:
        return Response({"no result": []})

#INICIA SECCION DE UNIDADES

@csrf_exempt 
@api_view(['POST', 'GET'])
def getUnidad(request, pk):

    unidad = UnitBox.objects.get(id=pk)
    serializer = UnitBoxSerializer(unidad)
    return Response(serializer.data)

@csrf_exempt 
@api_view(['PUT'])
def updateUnidad(request):

    code = request.data.get('code')
    code_name = request.data.get('code_name')
    description = request.data.get('description')
    high = float(request.data.get('high'))
    idS = request.data.get('id')
    long = float(request.data.get('long'))
    modalidad = request.data.get('modalidad')
    mostrarLista = request.data.get('mostrarLista')
    name = request.data.get('name')
    order_cot = request.data.get('order_cot')
    orderg = request.data.get('orderg')
    orderp = request.data.get('orderp')
    peso_bruto_carga = request.data.get('peso_bruto_carga')
    peso_bruto_total = request.data.get('peso_bruto_total')
    width = float(request.data.get('width'))
    capacidadMaxima = int(request.data.get('capacidadMaxima'))
    precio_kilometraje = float(request.data.get('precio_kilometraje'))

    if idS != 0:
        unidad = UnitBox.objects.get(id=idS)
        unidad.code = code
        unidad.code_name = code_name
        unidad.capacidad_vol = width * long * high 
        unidad.description = description
        unidad.high = high
        unidad.long = long
        unidad.modalidad = modalidad
        unidad.mostrarLista = mostrarLista
        unidad.name = name
        unidad.order_cot = order_cot
        unidad.orderg = orderg
        unidad.orderp = orderp
        unidad.peso_bruto_carga = peso_bruto_carga
        unidad.peso_bruto_total = peso_bruto_total
        unidad.width = width
        unidad.capacidadMaxima = capacidadMaxima
        unidad.precio_kilometraje = precio_kilometraje
        unidad.save()
        return Response(True)
    else:
        return Response(False)

@csrf_exempt 
@api_view(['PUT'])
def deleteUnidad(request, pk):
    
    idS = pk
    status = request.data.get('mostrarLista')

    if id != 0:
        unidad = UnitBox.objects.get(id=idS)
        unidad.mostrarLista = status
        unidad.save()
        return Response(True)
    else:
        return Response(False)

#TERMINA SECCION DE UNIDADES

@csrf_exempt 
@api_view(['GET'])
def getModulos(request):

    datosPer = []

    modulos = Modulos.objects.filter(estatus=1).filter(isSubmenu=False)
    mod = ModulosSerializer(modulos, many=True)

    return Response(mod.data)

@csrf_exempt 
@api_view(['POST'])
def getPermisosUsuario(request):

    datosPer = []

    idusuario = request.data.get('id')

    permisos = Permisos.objects.filter(idUsuario_id=idusuario).select_related('idModulo').values('idModulo__id','idModulo__nombre','idModulo__estatus','idModulo__isSubmenu','idModulo__link','idModulo__idMenu','idModulo__icon','lectura','agregar','eliminar','editar','pdf','excel','usuarioAsigna')
    
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
        "permisos_pdf":permiso['pdf'],
        "permisos_excel":permiso['excel'],
        "permisos_usuarioAsigna":permiso['usuarioAsigna'],
    })

    return Response(datosPer)


@csrf_exempt 
@api_view(['POST'])
def asignaPermisos(request):

    idUsr = request.data.get('idUsr')
    idMod = request.data.get('idMod')
    accio = str(request.data.get('accio'))
    res = ''
    usrAs = request.data.get('usrAs')
    idMen = int(request.data.get('idMen'))
    exist = False
    count = 0

    if(accio == 'add'):
        if idMen > 0 :
            exist = Permisos.objects.filter(idModulo_id=idMen).filter(idUsuario_id=idUsr).exists()

            if exist == False:
                Permisos.objects.create(usuarioAsigna=usrAs, idModulo_id = idMen, idUsuario_id = idUsr)
        
        data = Permisos.objects.create(usuarioAsigna=usrAs, idModulo_id = idMod, idUsuario_id = idUsr)
        ser = PermisosSerializer(data)
        res = ser.data
    elif(accio == 'del'):

        if idMen > 0:

            mods = Modulos.objects.filter(idMenu=idMen)
            perm = Permisos.objects.filter(idUsuario_id=idUsr).filter(idModulo_id__in=mods.values('id'))
            count = perm.count()
            if count == 1:
                Permisos.objects.filter(idUsuario_id=idUsr).filter(idModulo_id=idMen).delete()

        res = Permisos.objects.filter(idUsuario_id=idUsr).filter(idModulo_id=idMod).delete()   
    
    return Response({'response':res})

@csrf_exempt 
@api_view(['POST'])
def accionesPermisos(request):

    idUsr = int(request.data.get('idUsr'))
    idMod = int(request.data.get('idMod'))
    accio = str(request.data.get('accio'))
    usrAs = str(request.data.get('usrAs'))
    activ = bool(request.data.get('activ'))
    activar = 0
    res = ''
    exist = False
    count = 0

    if accio == 'Alta':
        if activ:
            activar =  1
        else:
            activar =  0

        agregar = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        agregar.agregar = activar
        res = agregar.save()
    elif accio == 'Baja':
        if activ:
            activar =  1
        else:
            activar =  0

        baja = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        baja.eliminar = activar
        res = baja.save()
    elif accio == 'Editar':
        if activ:
            activar =  1
        else:
            activar =  0

        editar = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        editar.editar = activar
        res = editar.save()
    elif accio == 'Leer':
        if activ:
            activar =  1
        else:
            activar =  0

        leer = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        leer.lectura = activar
        res = leer.save()
    elif accio == 'Pdf':
        if activ:
            activar =  1
        else:
            activar =  0

        pdf = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        pdf.pdf = activar
        res = pdf.save()
    elif accio == 'Excel':
        if activ:
            activar =  1
        else:
            activar =  0

        excel = Permisos.objects.get(idUsuario_id=idUsr, idModulo_id=idMod)
        excel.excel = activar
        res = excel.save()

    return Response({'response':res})

@csrf_exempt 
@api_view(['GET'])
def getModulo(request, pk):

    idMod = pk

    modulo = Modulos.objects.filter(id=idMod)
    modser = ModulosSerializer(modulo, many=True)

    return Response(modser.data)


@csrf_exempt 
@api_view(['POST'])
def newModulo(request):

    nombre = str(request.data.get('nombre'))
    icon = str(request.data.get('icon'))
    link = str(request.data.get('link'))
    estatus = bool(request.data.get('estatus'))
    isSubmenu = bool(request.data.get('isSubmenu'))
    usuario = str(request.data.get('usuario'))

    res = Modulos.objects.create(nombre = nombre, estatus = estatus, icon = icon, idMenu = 0, isSubmenu = isSubmenu, link = link, usuario = usuario)
    resSer = ModulosSerializer(res)
    return Response(resSer.data)

@csrf_exempt 
@api_view(['POST'])
def perModUsr(request):

    idUsr = int(request.data.get('id'))
    idModulo = int(request.data.get('idModulo'))

    datosPer = []

    permisos = Permisos.objects.filter(idUsuario_id=idUsr).filter(idModulo=idModulo).select_related('idModulo').values('idModulo__id','idModulo__nombre','idModulo__estatus','idModulo__isSubmenu','idModulo__link','idModulo__idMenu','idModulo__icon','lectura','agregar','eliminar','editar','pdf','excel','usuarioAsigna')
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
        "permisos_pdf":permiso['pdf'],
        "permisos_excel":permiso['excel'],
        "permisos_usuarioAsigna":permiso['usuarioAsigna'],
    })
    
    return Response(datosPer)

@csrf_exempt
@api_view(['GET'])
def ListaModulos(request):
    
    goodslist=Modulos.objects.all().order_by('id')
        
    goods_ser=ModulosSerializer(goodslist,many=True)

    return Response(goods_ser.data)


@csrf_exempt
@api_view(['GET'])
def ListEmbalajeFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Embalaje.objects.exclude(estatus=4)[data_start:data_end]
            count = Embalaje.objects.exclude(estatus=4).count()
        else:
            goodslist = Embalaje.objects.filter(Q(nombre__icontains=palabra)).exclude(estatus=4)[data_start:data_end]
            count = Embalaje.objects.filter(Q(nombre__icontains=palabra)).exclude(estatus=4).count()
        goods_ser=EmbalajeSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt 
@api_view(['POST'])
def newEmbalaje(request):

    nombre = str(request.data.get('nombre'))
    estatus = str(request.data.get('estatus'))
    largo = float(request.data.get('largo'))
    alto = float(request.data.get('alto'))
    ancho = float(request.data.get('ancho'))
    cantidadMaxima = int(request.data.get('cantidadMaxima'))
    usuario = str(request.data.get('usuario'))

    if estatus == 'false':
        estatus = 0
    else:
        estatus = 1

    res = Embalaje.objects.create(nombre = nombre, estatus = estatus, largo = largo, alto = alto, ancho = ancho, cantidadMaxima = cantidadMaxima, usuario = usuario)
    resSer = EmbalajeSerializer(res)
    return Response(resSer.data)

@csrf_exempt 
@api_view(['POST'])
def getEmbalaje(request, pk):

    id = pk

    embalaje = Embalaje.objects.filter(idEmbalaje=id)
    emb = EmbalajeSerializer(embalaje, many=True)

    return Response(emb.data)

@csrf_exempt 
@api_view(['PUT'])
def updateEmbalaje(request):

    id = int(request.data.get('id'))
    nombre = request.data.get('nombre')
    estatus = request.data.get('estatus')
    if estatus == 'true':
        estatus = 1
    else: 
        estatus = 0
    largo = float(request.data.get('largo'))
    alto = float(request.data.get('alto'))
    ancho = float(request.data.get('ancho'))
    cantidadMaxima = int(request.data.get('cantMax'))
    usuario = request.data.get('usuario')

    if id != 0:
        embalaje = Embalaje.objects.get(idEmbalaje=id)
        embalaje.nombre = nombre
        embalaje.largo = largo
        embalaje.alto = alto
        embalaje.ancho = ancho
        embalaje.cantidadMaxima = cantidadMaxima
        embalaje.usuario = usuario
        embalaje.save()
        return Response(True)
    else:
        return Response(False)
    
@csrf_exempt 
@api_view(['PUT'])
def deleteEmbalaje(request, pk):
    
    idS = pk
    
    if id != 0:
        unidad = Embalaje.objects.get(idEmbalaje=idS)
        unidad.estatus = 4
        unidad.save()
        return Response(True)
    else:
        return Response(False)

@csrf_exempt
@api_view(['GET'])
def ListTerminosFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Terminos_Condiciones.objects.filter(aplica__icontains='LTL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(aplica__icontains='LTL').count()
        else:
            goodslist = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='LTL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='LTL').count()
        goods_ser=TerminosCondicionesSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListTerminosFTLFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Terminos_Condiciones.objects.filter(aplica__icontains='FTL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(aplica__icontains='FTL').count()
        else:
            goodslist = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='FTL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='FTL').count()
        goods_ser=TerminosCondicionesSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListTerminosFCLFiltro(request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra = str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size
        if (palabra == ""):
            goodslist = Terminos_Condiciones.objects.filter(aplica__icontains='FCL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(aplica__icontains='FCL').count()
        else:
            goodslist = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='FCL')[data_start:data_end]
            count = Terminos_Condiciones.objects.filter(Q(nombre__icontains=palabra)).filter(aplica__icontains='FCL').count()
        goods_ser=TerminosCondicionesSerializer(goodslist,many=True)
        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt
@api_view(['GET'])
def ListGeocercas(request):

    estado = request.GET.get('estado')
    cp = request.GET.get('cp')

    datosPoligGen = []
    datosPolig = []

    inner_subquery = Geocercas.objects.filter(estatus=1, estado=estado, codigoPostal=cp).values(
        'codigoPostal', 'orden', 'poligono', 'lat', 'lng'
    ).annotate().distinct('codigoPostal', 'orden', 'poligono', 'lat', 'lng')

    queryset = Geocercas.objects.filter(
        codigoPostal__in=inner_subquery.values('codigoPostal')
    ).order_by('codigoPostal', 'poligono', 'orden')

    result = queryset.annotate(
        geo_codigoPostal=F('codigoPostal'),
        geo_orden=F('orden'),
        geo_poligono=F('poligono'),
        geo_lat=F('lat'),
        geo_lng=F('lng')
    ).order_by('geo_codigoPostal', 'geo_poligono', 'geo_orden')

    #serialized_results = list(result)

    poligono_a = 0
    poligono_n = 0
    #for data in serialized_results:
    for data in result:
        poligono_n = int(data.poligono)

        if poligono_a != poligono_n:
            if len(datosPolig) > 0:
                datosPoligGen.append(datosPolig)
                datosPolig = []

        dato = {"cp": data.codigoPostal, "orden": data.orden, "poligono":data.poligono, "lat":float(data.lat), "lng":float(data.lng)}
        datosPolig.append(dato)
        poligono_a = int(data.poligono)
    
    datosPoligGen.append(datosPolig)

    return Response({'data':datosPoligGen})

@csrf_exempt
@api_view(['GET'])
def geocercasEstados(request):

    estatusGeo = request.GET.get('dato')

    distinct_estados = Geocercas.objects.filter(estatus=1).filter(estatus_geocerca=estatusGeo).values_list('estado', flat=True).distinct().order_by('estado')

    return Response({'data':distinct_estados})

@csrf_exempt
@api_view(['GET'])
def geocercasCP(request):

    estado = request.GET.get('estado')
    estatusGeo = request.GET.get('estatus')

    #distinct_codigos_postales = Geocercas.objects.filter(estatus=1, estado=estado).values_list('codigoPostal', flat=True).distinct()
    distinct_codigos_postales = Geocercas.objects.filter(estatus=1, estado=estado, estatus_geocerca = estatusGeo).values('codigoPostal', 'ciudad', 'nombre_corto', 'colonia').distinct().order_by('ciudad')

    valores = [item for item in distinct_codigos_postales]

    return Response({'data':valores})

@csrf_exempt
@api_view(['GET'])
def geocercasCentro(request):

    estado = request.GET.get('estado')
    codigoPostal = request.GET.get('cp')

    distinct_codigos_postales = Geocercas.objects.filter(estatus=1, estado=estado, codigoPostal=codigoPostal).values('codigoPostal', 'lat_centro', 'lng_centro', 'kilometros_redonda').distinct()

    return Response({'data':distinct_codigos_postales})

@csrf_exempt
@api_view(['GET'])
def geocercasElimina(request):

    estado = request.GET.get('estado')
    codigoPostal = request.GET.get('cp')
    tg = int(request.GET.get('tg'))


    geo_elimina = Geocercas.objects.filter(estatus=1, estado=estado, codigoPostal=codigoPostal, estatus_geocerca=tg)

    # Elimina el objeto
    geo_elimina.delete()

    return Response({'data':True})


@csrf_exempt
@api_view(['GET'])
def geocercasEstaados(request):
    
    datos = []

    #distinct_estados = Geocercas.objects.filter(estatus=1).values('estado').distinct().order_by('estado')
    distinct_estados = Geocercas.objects.filter(estatus=1).order_by('estado','ciudad', 'colonia')

    for ds in distinct_estados:
        if ds.nombre_corto != '':
            datos.append({
                "name":ds.nombre_corto,
                "idGeocerca":ds.idGeocerca,
            })
        else:

            datos.append({
                "name":ds.estado + ', ' + ds.ciudad + ', ' + ds.colonia  +', ' + ds.codigoPostal,
                "idGeocerca":ds.idGeocerca,
            })
    #estados_ser = GeocercasSerializer(distinct_estados, many=True)

    return JsonResponse({'datos': datos})

@csrf_exempt
@api_view(['POST', 'GET'])
def getInfoEstados(request):

    id_o = request.GET.get('idGeocerca_o')
    id_d = request.GET.get('idGeocerca_d')
    
    estados_o = Geocercas.objects.filter(idGeocerca=id_o)
    estados_ser_o = GeocercasSerializer(estados_o, many=True)

    estados_d = Geocercas.objects.filter(idGeocerca=id_d)
    estados_ser_d = GeocercasSerializer(estados_d, many=True)

    return Response({"origen":estados_ser_o.data,"destino":estados_ser_d.data})

@csrf_exempt
@api_view(['POST', 'GET'])
def getInfoEstadosGeo(request):

    id = request.GET.get('idGeocerca')
    
    estados = Geocercas.objects.filter(idGeocerca=id)
    estados_ser = GeocercasSerializer(estados, many=True)

    return Response(estados_ser.data)

@csrf_exempt
@api_view(['POST', 'GET'])
def getInfoEstadosCotizacion(request):

    id = request.GET.get('idGeocerca')
    
    #distinct_estados = Geocercas.objects.filter(estatus=1).values('estado').distinct().order_by('estado')
    estados_o = Geocercas.objects.filter(idGeocerca=id)
    estados_ser = GeocercasSerializer(estados_o, many=True)

    return Response(estados_ser.data)

@csrf_exempt
@api_view(['GET'])
def ListZonasTarifasFiltro(request):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 1))
        palabra=str(request.GET.get('palabra', 1))
        data_start = (page - 1) * size
        data_end = page * size

        if (palabra == ""):
            goodslist = Zonas_Tarifas.objects.filter(Q(clasificacion__icontains=palabra) | Q(estado_origen__icontains=palabra)).filter(Q(estatus=0) | Q(estatus = 1)).order_by('id_zona_tarifa')[data_start:data_end]
            count = Zonas_Tarifas.objects.filter(Q(clasificacion__icontains=palabra) | Q(estado_origen__icontains=palabra)).filter(Q(estatus=0) | Q(estatus = 1)).count()
        else:
            goodslist = Zonas_Tarifas.objects.filter(Q(clasificacion__icontains=palabra) | Q(estado_origen__icontains=palabra)).filter(Q(estatus=0) | Q(estatus = 1)).order_by('id_zona_tarifa')[data_start:data_end]
            count = Zonas_Tarifas.objects.filter(Q(clasificacion__icontains=palabra) | Q(estado_origen__icontains=palabra)).filter(Q(estatus=0) | Q(estatus = 1))[data_start:data_end].count()

        goods_ser=zona_tarifasSerializer(goodslist,many=True)

        return Response({
            'total':count,
            'data':goods_ser.data
        })

@csrf_exempt 
@api_view(['POST'])
def newZonaTarifa(request):

    resSer = []
    data = request.data.get('info')

    for d in data:
        print(d)
        geoO = Geocercas.objects.filter(idGeocerca=int(d['id_geocerca_o']))
        geoDataO = GeocercasSerializer(geoO, many=True)

        pais_o = str(geoDataO.data[0]['pais'])
        estado_o = str(geoDataO.data[0]['estado'])
        ciudad_o = str(geoDataO.data[0]['ciudad'])
        cp_o = str(geoDataO.data[0]['codigoPostal'])
        estatus_geo_o = int(geoDataO.data[0]['estatus_geocerca'])

        geoD = Geocercas.objects.filter(idGeocerca=int(d['id_geocerca_d']))
        geoDataD = GeocercasSerializer(geoD, many=True)

        pais_d = str(geoDataD.data[0]['pais'])
        estado_d = str(geoDataD.data[0]['estado'])
        ciudad_d = str(geoDataD.data[0]['ciudad'])
        cp_d = str(geoDataD.data[0]['codigoPostal'])
        estatus_geo_d = int(geoDataD.data[0]['estatus_geocerca'])

        km = d['km']
        km = km.replace(",","")

        count = Zonas_Tarifas.objects.filter(pais_origen = pais_o, estado_origen = estado_o, ciudad_origen = ciudad_o, cp_origen = cp_o, pais_destino = pais_d, estado_destino = estado_d, ciudad_destino = ciudad_d, cp_destino = cp_d).count()
        if count > 0:
            res = Zonas_Tarifas.objects.filter(pais_origen = pais_o, estado_origen = estado_o, ciudad_origen = ciudad_o, cp_origen = cp_o, pais_destino = pais_d, estado_destino = estado_d, ciudad_destino = ciudad_d, cp_destino = cp_d)
        else:
            res = Zonas_Tarifas.objects.create(clasificacion = d['tipoGeocerca'], km = km, pais_origen = pais_o, estado_origen = estado_o, ciudad_origen = ciudad_o, cp_origen = cp_o, pais_destino = pais_d, estado_destino = estado_d, ciudad_destino = ciudad_d, cp_destino = cp_d, estatus = 1, usuario_alta = d['tipoUsuario'], date_create = datetime.now())
        
        resSer = zona_tarifasSerializer(res)


    return Response(resSer.data)


@csrf_exempt 
@api_view(['POST'])
def ValidaZonasTarifas(request):

    info = request.data.get('data')
    respuesta = []
    tipoZonaClass = ''

    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
    trans = str.maketrans(a,b)
    
    for dataInfo in info:
        
        pais_origen = dataInfo['pais_o']
        estado_origen = dataInfo['estado_o']
        ciudad_origen = dataInfo['ciudad_o']
        colonia_origen = dataInfo['colonia_o']
        if colonia_origen is None:
            colonia_origen = ''
        cp_origen = dataInfo['cp_o']
        pais_destino = dataInfo['pais_d']
        estado_destino = dataInfo['estado_d']
        ciudad_destino = dataInfo['ciudad_d']
        colonia_destino = dataInfo['colonia_d']
        cp_destino = dataInfo['cp_d']
        
        pais_origen = pais_origen.translate(trans)
        estado_origen = estado_origen.translate(trans)
        ciudad_origen = ciudad_origen.translate(trans)
        colonia_origen = colonia_origen.translate(trans)
        if colonia_destino is None:
            colonia_destino = ''
        cp_origen = cp_origen.translate(trans)
        pais_destino = pais_destino.translate(trans)
        estado_destino = estado_destino.translate(trans)
        ciudad_destino = ciudad_destino.translate(trans)
        colonia_destino = colonia_destino.translate(trans)
        cp_destino = cp_destino.translate(trans)

        res = Zonas_Tarifas.objects.filter(pais_origen = pais_origen, estado_origen = estado_origen, ciudad_origen = ciudad_origen, pais_destino = pais_destino, estado_destino = estado_destino, ciudad_destino = ciudad_destino)
        print(res.count())
        if res.count() == 0:
            print(res.query, 'n1')
            res = Zonas_Tarifas.objects.filter(pais_origen = pais_origen, estado_origen = estado_origen, ciudad_origen__icontains = colonia_origen, pais_destino = pais_destino, estado_destino = estado_destino, ciudad_destino = ciudad_destino)
            if res.count() == 0:
                print(res.query, 'n2')
                res = Zonas_Tarifas.objects.filter(pais_origen = pais_origen, estado_origen = estado_origen, ciudad_origen = ciudad_origen, pais_destino = pais_destino, estado_destino = estado_destino, ciudad_destino__icontains = colonia_destino)
                if res.count():
                    print(res.query, 'n3')
                    res = Zonas_Tarifas.objects.filter(pais_origen = pais_origen, estado_origen = estado_origen, ciudad_origen__icontains = colonia_origen, pais_destino = pais_destino, estado_destino = estado_destino, ciudad_destino__icontains = colonia_destino)
                    
        resSer = zona_tarifasSerializer(res, many=True)

        if res.count() == 0:
            tipoZona = 0
            km = 0
            tipoZonaText =  'Sin Clasificación'
        else:
            tipoZona = resSer.data[0]['clasificacion']
            km = resSer.data[0]['km']
            tipoZonaText =  ''

        if tipoZona == 1:
            tipoZonaText = 'Zona Comercial'
            tipoZonaClass = 'success'
        elif tipoZona == 2:
            tipoZonaText = 'Zona No Comercial'
            tipoZonaClass = 'warning'
        elif tipoZona == 3:
            tipoZonaText = 'Zona Peligrosa'
            tipoZonaClass = 'danger'
        elif tipoZona == 4:
            tipoZonaText = 'Zona Comercial - Zona Peligrosa'
            tipoZonaClass = 'danger'
        elif tipoZona == 5:
            tipoZonaText = 'Zona Comercial - Zona No Comercial'
            tipoZonaClass = 'warning'
        elif tipoZona == 6:
            tipoZonaText = 'Zona No Comercial - Zona Comercial'
            tipoZonaClass = 'warning'
        elif tipoZona == 7:
            tipoZonaText = 'Zona No Comercial - Zona Peligrosa'
            tipoZonaClass = 'danger'
        elif tipoZona == 8:
            tipoZonaText = 'Zona Peligrosa - Zona Comercial'
            tipoZonaClass = 'danger'
        elif tipoZona == 9:
            tipoZonaText = 'Zona Peligrosa - Zona No Comercial'
            tipoZonaClass = 'danger'
        elif tipoZona == 0:
            tipoZonaText = 'Sin Clasificación'
            tipoZonaClass = 'secondary'

        ciudad_origen = dataInfo['ciudad_o']
        ciudad_destino = dataInfo['ciudad_d']
        
        ##nodo = {"origen":pais_origen+', '+estado_origen+', '+ciudad_origen+', '+cp_origen,"destino":pais_destino+', '+estado_destino+', '+ciudad_destino+', '+cp_destino, "tipoZona":tipoZona, "km":km }
        nodo = {"origen":pais_origen+', '+estado_origen+', '+ciudad_origen,"destino":pais_destino+', '+estado_destino+', '+ciudad_destino, "tipoZonaText":tipoZonaText, "tipoZona":tipoZona,  "km":km, "tipoZonaClass":tipoZonaClass }
        respuesta.append(nodo)

    return Response(respuesta)


@csrf_exempt
@api_view(['POST', 'GET'])
def getDistanciasMaps(request):

    org = request.GET.get('org')
    des = request.GET.get('des')


    '''params = {
                    "destinations": des,
                    "origins": org,
                    "units": "metric",
                    "avoid":"Highways",
                    "key": "AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y"
                } 
        
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params)
        
    data = json.loads(response.text)'''

    API_KEY = 'AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y'

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={org}&destination={des}&mode=driving&avoid=tolls&key={API_KEY}"

    # Realizar la solicitud GET
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        # Obtener las instrucciones de navegación
        dato = data['routes'][0]['legs'][0]['distance']['text']
        dato = dato.split(" ")
        data = dato[0]
    
    return Response(data)

@csrf_exempt
@api_view(['POST', 'GET'])
def getDistanciasMapsCordenadas(request):

    org = request.data.get('org')
    des = request.data.get('des')

    print(org)

    API_KEY = 'AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y'

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={org}&destination={des}&mode=driving&avoid=tolls&key={API_KEY}"

    # Realizar la solicitud GET
    response = requests.get(url)

    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()
        #print(data)
        # Obtener las instrucciones de navegación
        dato = data['routes'][0]['legs'][0]['distance']['text']
        dato = dato.split(" ")
        data = dato[0]
    
    return Response(data)


@csrf_exempt
@api_view(['POST', 'GET'])
def obtener_direccion_gmaps(request):
    api_key = 'AIzaSyADhOxfxQ9u-0_4FuHs8sVMHnyw0TnI11Y'
    latitud = 0
    longitud = 0

    geo = Geocercas.objects.filter(pais = 'Mexico', estado = 'Queretaro').filter(~Q(idGeocerca__in='2616')).order_by('idGeocerca')
    #geo = Geocercas.objects.filter(idGeocerca = 2616).order_by('idGeocerca')
    
    geo_ser = GeocercasSerializer(geo, many=True)

    for g in geo_ser.data:

        latitud = float(g['lat'])
        longitud = float(g['lng'])
        
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitud},{longitud}&key={api_key}"

        # Realiza la solicitud GET a la API de Google Maps
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                resultados = data['results']
                if resultados:
                    # Obtiene la dirección más específica (normalmente la primera)
                    direccion = resultados[0]
                
                    # Inicializa variables para colonia y código postal
                    colonia = ''
                    codigo_postal = ''
                    ciudad = ''

                    print(direccion)
                    # Itera sobre los componentes de la dirección para extraer la colonia y el código postal
                    for componente in direccion['address_components']:
                        if 'locality' in componente['types']:
                            ciudad = componente['long_name']
                        
                        if 'sublocality' in componente['types']:
                            colonia = componente['long_name']
                        
                        if 'postal_code' in componente['types']:
                            codigo_postal = componente['long_name']

                        geo = Geocercas.objects.get(idGeocerca=int(g['idGeocerca']))
                        geo.ciudad = ciudad
                        geo.colonia = colonia
                        geo.codigoPostal = codigo_postal
                        geo.save()
                else:
                    return None, None
            else:
                print("Error en la respuesta de la API:", data['status'])
        else:
            print("Error al realizar la solicitud a la API:", response.status_code)
    
    return Response(data)


