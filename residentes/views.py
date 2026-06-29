from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Residente, Vivienda, Visita
from .utils import validar_cedula_ecuador, validar_telefono_ecuador, validar_placa_ecuador
from django.utils import timezone


def login(request):
    error = ""
    usuario = ""

    if request.method == "POST":
        usuario = request.POST.get("usuario")
        contrasena = request.POST.get("contrasena")

        if usuario == "admin" and contrasena == "Admin2026":
            return redirect("dashboard")
        else:
            error = "Usuario o contraseña incorrectos. Verifique sus credenciales e intente nuevamente."

    return render(request, "residentes/login.html", {
        "error": error,
        "usuario": usuario
    })


def dashboard(request):
    total_residentes = Residente.objects.count()
    total_viviendas = Vivienda.objects.count()
    visitas_en_curso = Visita.objects.filter(estado="En curso").count()
    visitas_finalizadas = Visita.objects.filter(estado="Finalizada").count()

    ultimas_visitas = Visita.objects.all().order_by("-id")[:5]

    return render(request, "residentes/dashboard.html", {
        "total_residentes": total_residentes,
        "total_viviendas": total_viviendas,
        "visitas_en_curso": visitas_en_curso,
        "visitas_finalizadas": visitas_finalizadas,
        "ultimas_visitas": ultimas_visitas,
    })


def residentes(request):
    lista_residentes = Residente.objects.all()
    return render(request, "residentes/residentes.html", {
        "residentes": lista_residentes
    })


def nuevo_residente(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos = request.POST
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        estado = request.POST.get("estado") == "True"

        if not validar_telefono_ecuador(telefono):
            errores["telefono"] = "El teléfono debe tener 10 dígitos y empezar con 09."

        if Residente.objects.filter(email=email).exists():
            errores["email"] = "Ya existe un residente registrado con este correo."

        if errores:
            return render(request, "residentes/nuevo_residente.html", {
                "errores": errores,
                "datos": datos
            })

        Residente.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            email=email,
            estado=estado
        )

        messages.success(request, "Residente registrado correctamente.")
        return redirect("residentes")

    return render(request, "residentes/nuevo_residente.html")


def editar_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    errores = {}

    if request.method == "POST":
        datos = request.POST
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")

        if not validar_telefono_ecuador(telefono):
            errores["telefono"] = "El teléfono debe tener 10 dígitos y empezar con 09."

        if Residente.objects.filter(email=email).exclude(id=residente.id).exists():
            errores["email"] = "Ya existe otro residente con este correo."

        if errores:
            return render(request, "residentes/editar_residente.html", {
                "residente": residente,
                "errores": errores,
                "datos": datos
            })

        residente.nombres = request.POST.get("nombres")
        residente.apellidos = request.POST.get("apellidos")
        residente.telefono = telefono
        residente.email = email
        residente.estado = request.POST.get("estado") == "True"
        residente.save()

        messages.success(request, "Residente actualizado correctamente.")
        return redirect("residentes")

    return render(request, "residentes/editar_residente.html", {
        "residente": residente
    })


def eliminar_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    residente.delete()
    messages.success(request, "Residente eliminado correctamente.")
    return redirect("residentes")


def viviendas(request):
    lista_viviendas = Vivienda.objects.all()
    return render(request, "residentes/viviendas.html", {
        "viviendas": lista_viviendas
    })


def nueva_vivienda(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos = request.POST
        numero = request.POST.get("numero")
        bloque = request.POST.get("bloque")
        estado = request.POST.get("estado")
        residente_id = request.POST.get("residente")
        residente = get_object_or_404(Residente, id=residente_id)

        if Vivienda.objects.filter(numero=numero, bloque=bloque).exists():
            errores["numero"] = "Ya existe una vivienda registrada con ese número y bloque."

        if Vivienda.objects.filter(residente=residente).exists():
            errores["residente"] = "Este residente ya tiene una vivienda asignada."

        if errores:
            return render(request, "residentes/nueva_vivienda.html", {
                "errores": errores,
                "datos": datos,
                "residentes": Residente.objects.all()
            })

        Vivienda.objects.create(
            numero=numero,
            bloque=bloque,
            estado=estado,
            residente=residente
        )

        messages.success(request, "Vivienda registrada correctamente.")
        return redirect("viviendas")

    return render(request, "residentes/nueva_vivienda.html", {
        "residentes": Residente.objects.all()
    })


def editar_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)
    errores = {}

    if request.method == "POST":
        datos = request.POST
        numero = request.POST.get("numero")
        bloque = request.POST.get("bloque")
        residente_id = request.POST.get("residente")
        residente = get_object_or_404(Residente, id=residente_id)

        if Vivienda.objects.filter(numero=numero, bloque=bloque).exclude(id=vivienda.id).exists():
            errores["numero"] = "Ya existe otra vivienda registrada con ese número y bloque."

        if Vivienda.objects.filter(residente=residente).exclude(id=vivienda.id).exists():
            errores["residente"] = "Este residente ya tiene otra vivienda asignada."

        if errores:
            return render(request, "residentes/editar_vivienda.html", {
                "vivienda": vivienda,
                "errores": errores,
                "datos": datos,
                "residentes": Residente.objects.all()
            })

        vivienda.numero = numero
        vivienda.bloque = bloque
        vivienda.estado = request.POST.get("estado")
        vivienda.residente = residente
        vivienda.save()

        messages.success(request, "Vivienda actualizada correctamente.")
        return redirect("viviendas")

    return render(request, "residentes/editar_vivienda.html", {
        "vivienda": vivienda,
        "residentes": Residente.objects.all()
    })


def eliminar_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)
    vivienda.delete()
    messages.success(request, "Vivienda eliminada correctamente.")
    return redirect("viviendas")


def visitas(request):
    lista_visitas = Visita.objects.all()
    return render(request, "residentes/visitas.html", {
        "visitas": lista_visitas
    })


def nueva_visita(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos = request.POST

        documento = request.POST.get("documento")
        telefono = request.POST.get("telefono")
        placa = request.POST.get("placa", "").upper().strip()
        fecha_ingreso = request.POST.get("fecha_ingreso")
        fecha_salida = request.POST.get("fecha_salida")
        estado = request.POST.get("estado")
        verificacion_identidad = request.POST.get("verificacion_identidad")

        if not validar_cedula_ecuador(documento):
            errores["documento"] = "La cédula ingresada no es válida."

        if not validar_telefono_ecuador(telefono):
            errores["telefono"] = "El teléfono debe tener 10 dígitos y empezar con 09."

        if not validar_placa_ecuador(placa):
            errores["placa"] = "La placa debe tener un formato válido. Ejemplo: ABC-1234."

        if not verificacion_identidad:
            errores["verificacion_identidad"] = "Debe confirmar que verificó físicamente la identidad del visitante."

        if Visita.objects.filter(documento=documento, estado="En curso").exists():
            errores["documento"] = "Este visitante ya tiene una visita en curso."

        if estado == "Finalizada" and not fecha_salida:
            errores["fecha_salida"] = "Debe registrar la fecha de salida para finalizar la visita."

        if fecha_salida and fecha_salida < fecha_ingreso:
            errores["fecha_salida"] = "La fecha de salida no puede ser menor que la fecha de ingreso."

        if errores:
            return render(request, "residentes/nueva_visita.html", {
                "errores": errores,
                "datos": datos,
                "viviendas": Vivienda.objects.all()
            })

        vivienda = get_object_or_404(Vivienda, id=request.POST.get("vivienda"))

        Visita.objects.create(
            nombre_visitante=request.POST.get("nombre_visitante"),
            documento=documento,
            telefono=telefono,
            placa=placa,
            motivo=request.POST.get("motivo"),
            observaciones=request.POST.get("observaciones"),
            fecha_ingreso=fecha_ingreso,
            fecha_salida=fecha_salida if fecha_salida else None,
            estado=estado,
            vivienda=vivienda
        )

        messages.success(request, "Visita registrada correctamente.")
        return redirect("visitas")

    return render(request, "residentes/nueva_visita.html", {
        "viviendas": Vivienda.objects.all()
    })


def editar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    errores = {}

    if request.method == "POST":
        datos = request.POST

        documento = request.POST.get("documento")
        telefono = request.POST.get("telefono")
        placa = request.POST.get("placa", "").upper().strip()
        fecha_ingreso = request.POST.get("fecha_ingreso")
        fecha_salida = request.POST.get("fecha_salida")
        estado = request.POST.get("estado")
        verificacion_identidad = request.POST.get("verificacion_identidad")

        if not validar_cedula_ecuador(documento):
            errores["documento"] = "La cédula ingresada no es válida."

        if not validar_telefono_ecuador(telefono):
            errores["telefono"] = "El teléfono debe tener 10 dígitos y empezar con 09."

        if not validar_placa_ecuador(placa):
            errores["placa"] = "La placa debe tener un formato válido. Ejemplo: ABC-1234."

        if not verificacion_identidad:
            errores["verificacion_identidad"] = "Debe confirmar que verificó físicamente la identidad del visitante."

        if Visita.objects.filter(documento=documento, estado="En curso").exclude(id=visita.id).exists():
            errores["documento"] = "Este visitante ya tiene otra visita en curso."

        if estado == "Finalizada" and not fecha_salida:
            errores["fecha_salida"] = "Debe registrar la fecha de salida para finalizar la visita."

        if fecha_salida and fecha_salida < fecha_ingreso:
            errores["fecha_salida"] = "La fecha de salida no puede ser menor que la fecha de ingreso."

        if errores:
            return render(request, "residentes/editar_visita.html", {
                "visita": visita,
                "errores": errores,
                "datos": datos,
                "viviendas": Vivienda.objects.all()
            })

        vivienda = get_object_or_404(Vivienda, id=request.POST.get("vivienda"))

        visita.nombre_visitante = request.POST.get("nombre_visitante")
        visita.documento = documento
        visita.telefono = telefono
        visita.placa = placa
        visita.motivo = request.POST.get("motivo")
        visita.observaciones = request.POST.get("observaciones")
        visita.fecha_ingreso = fecha_ingreso
        visita.fecha_salida = fecha_salida if fecha_salida else None
        visita.estado = estado
        visita.vivienda = vivienda
        visita.save()

        messages.success(request, "Visita actualizada correctamente.")
        return redirect("visitas")

    return render(request, "residentes/editar_visita.html", {
        "visita": visita,
        "viviendas": Vivienda.objects.all()
    })


def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.delete()
    messages.success(request, "Visita eliminada correctamente.")
    return redirect("visitas")
    return redirect("visitas")

def reportes(request):
    total_residentes = Residente.objects.count()
    total_viviendas = Vivienda.objects.count()

    viviendas_ocupadas = Vivienda.objects.filter(estado="Ocupada").count()
    viviendas_disponibles = Vivienda.objects.filter(estado="Disponible").count()
    viviendas_mantenimiento = Vivienda.objects.filter(estado="Mantenimiento").count()

    total_visitas = Visita.objects.count()
    visitas_en_curso = Visita.objects.filter(estado="En curso").count()
    visitas_finalizadas = Visita.objects.filter(estado="Finalizada").count()
    visitas_canceladas = Visita.objects.filter(estado="Cancelada").count()

    fecha_reporte = timezone.now()

    return render(request, "residentes/reportes.html", {
        "total_residentes": total_residentes,
        "total_viviendas": total_viviendas,
        "viviendas_ocupadas": viviendas_ocupadas,
        "viviendas_disponibles": viviendas_disponibles,
        "viviendas_mantenimiento": viviendas_mantenimiento,
        "total_visitas": total_visitas,
        "visitas_en_curso": visitas_en_curso,
        "visitas_finalizadas": visitas_finalizadas,
        "visitas_canceladas": visitas_canceladas,
        "fecha_reporte": fecha_reporte,
    })