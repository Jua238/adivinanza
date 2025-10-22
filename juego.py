"""Juego de adivinanza numérica sencillo.

Permite al jugador seleccionar un rango de números y un número máximo de
intentos antes de comenzar la partida. Durante el juego se proporcionan pistas
para acercarse al número secreto.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class ConfiguracionJuego:
    """Configuración inicial para el juego.

    Attributes:
        minimo: Límite inferior del rango de números válidos.
        maximo: Límite superior del rango de números válidos.
        intentos: Número máximo de intentos permitidos.
    """

    minimo: int
    maximo: int
    intentos: int

    def __post_init__(self) -> None:
        if self.minimo >= self.maximo:
            raise ValueError("El mínimo debe ser menor que el máximo.")
        if self.intentos <= 0:
            raise ValueError("El número de intentos debe ser positivo.")


class JuegoAdivinanza:
    """Encapsula la lógica de un juego de adivinanza."""

    def __init__(self, configuracion: ConfiguracionJuego) -> None:
        self.configuracion = configuracion
        self.numero_secreto = random.randint(
            configuracion.minimo, configuracion.maximo
        )
        self.intentos_restantes = configuracion.intentos

    def jugar(self) -> None:
        """Inicia el bucle principal del juego."""

        print(
            "\n¡Bienvenido al juego de adivinanza!\n"
            f"Estoy pensando en un número entre {self.configuracion.minimo} y "
            f"{self.configuracion.maximo}."
        )

        while self.intentos_restantes > 0:
            intento = self._pedir_intento()
            if intento == self.numero_secreto:
                print("🎉 ¡Correcto! Has adivinado el número.")
                return

            self.intentos_restantes -= 1
            self._mostrar_pista(intento)

        print(
            "😢 Te quedaste sin intentos. "
            f"El número secreto era {self.numero_secreto}."
        )

    def _pedir_intento(self) -> int:
        """Solicita un intento y valida que sea un entero dentro del rango."""

        while True:
            try:
                valor = int(
                    input(
                        f"Ingresa un número entre {self.configuracion.minimo} y "
                        f"{self.configuracion.maximo}: "
                    )
                )
            except ValueError:
                print("❌ Debes escribir un número entero. Intenta nuevamente.")
                continue

            if self.configuracion.minimo <= valor <= self.configuracion.maximo:
                return valor

            print(
                "⚠️ El número está fuera del rango permitido. "
                "Intenta nuevamente."
            )

    def _mostrar_pista(self, intento: int) -> None:
        """Muestra una pista basada en cuán lejos estuvo el intento."""

        diferencia = abs(self.numero_secreto - intento)
        if intento < self.numero_secreto:
            orientacion = "mayor"
        else:
            orientacion = "menor"

        if diferencia <= 2:
            proximidad = "¡Estuviste muy cerca!"
        elif diferencia <= 5:
            proximidad = "Vas por buen camino."
        else:
            proximidad = "Aún estás lejos."

        print(
            f"❌ No es el número. Pista: prueba un número {orientacion}. "
            f"{proximidad}"
        )


def solicitar_configuracion() -> ConfiguracionJuego:
    """Recopila la configuración inicial del usuario con validaciones básicas."""

    print("Configura tu partida:\n")
    minimo = _solicitar_entero("Número mínimo: ")
    while True:
        maximo = _solicitar_entero("Número máximo: ")
        if maximo > minimo:
            break
        print("El número máximo debe ser mayor que el mínimo.")

    while True:
        intentos = _solicitar_entero("Cantidad de intentos: ")
        if intentos > 0:
            break
        print("La cantidad de intentos debe ser positiva.")

    return ConfiguracionJuego(minimo, maximo, intentos)


def _solicitar_entero(mensaje: str) -> int:
    """Solicita un entero al usuario manejando errores comunes."""

    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingresa un número entero válido, por favor.")


if __name__ == "__main__":
    configuracion = solicitar_configuracion()
    juego = JuegoAdivinanza(configuracion)
    juego.jugar()
