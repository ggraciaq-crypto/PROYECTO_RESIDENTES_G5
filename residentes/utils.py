import re


def validar_telefono_ecuador(telefono):
    return telefono.isdigit() and len(telefono) == 10 and telefono.startswith("09")


def validar_cedula_ecuador(cedula):
    if not cedula.isdigit() or len(cedula) != 10:
        return False

    provincia = int(cedula[:2])

    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(cedula[2])

    if tercer_digito >= 6:
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]

        if valor >= 10:
            valor -= 9

        suma += valor

    digito_verificador = 10 - (suma % 10)

    if digito_verificador == 10:
        digito_verificador = 0

    return digito_verificador == int(cedula[9])


def validar_placa_ecuador(placa):
    if not placa:
        return False

    placa = placa.upper().strip()

    patron = r"^[A-Z]{3}-[0-9]{4}$"

    return re.match(patron, placa) is not None