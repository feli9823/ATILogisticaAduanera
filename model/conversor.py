# ─────────────────────────────────────────────
#  Tasas de cambio base en CRC (Colones)
#  1 unidad de cada moneda = X colones
#  Fuente: referencia fija, actualizar según necesidad
# ─────────────────────────────────────────────
_TASAS_EN_CRC = {
    "CRC": 1.0,
    "USD": 520.0,
    "EUR": 560.0,
    "BRL": 100.0,
}


class conversor:

    def convertir(self, monto: float, moneda_origen: str, moneda_destino: str) -> float:
        """
        Convierte un monto de moneda_origen a moneda_destino.
        Estrategia: origen → CRC → destino.

        Parámetros:
            monto          : float — valor a convertir
            moneda_origen  : str   — moneda actual del monto ("CRC","USD","EUR","BRL")
            moneda_destino : str   — moneda a la que se quiere convertir

        Retorna:
            float — monto convertido a moneda_destino
        """
        if moneda_origen == moneda_destino:
            return monto

        tasa_origen  = _TASAS_EN_CRC.get(moneda_origen)
        tasa_destino = _TASAS_EN_CRC.get(moneda_destino)

        if tasa_origen is None or tasa_destino is None:
            raise ValueError(
                f"Moneda no soportada. "
                f"Origen: '{moneda_origen}', Destino: '{moneda_destino}'. "
                f"Monedas válidas: {list(_TASAS_EN_CRC.keys())}"
            )

        # monto en CRC → monto en moneda destino
        monto_en_crc    = monto * tasa_origen
        monto_convertido = monto_en_crc / tasa_destino

        return round(monto_convertido, 2)

    def obtenerTasas(self) -> dict:
        """Retorna las tasas actuales para referencia."""
        return dict(_TASAS_EN_CRC)
