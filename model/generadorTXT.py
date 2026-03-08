import os

# ─────────────────────────────────────────────
#  os.path.abspath(__file__) PRIMERO garantiza
#  que la ruta sea absoluta sin importar desde
#  dónde ejecute Flet la aplicación.
#
#  model/generadorTXT.py
#    └── ../documentos → ATILogisticaAduanera/documentos/ ✅
# ─────────────────────────────────────────────
_directorioActual = os.path.dirname(os.path.abspath(__file__))
_rutaBase = os.path.normpath(os.path.join(_directorioActual, "..", "documentos"))


def _asegurarCarpeta():
    """Crea documentos/ en la raíz del proyecto si no existe."""
    if not os.path.exists(_rutaBase):
        os.makedirs(_rutaBase)
        print(f"[generadorTXT] Carpeta creada en: {_rutaBase}")


class generadorTXT:

    @staticmethod
    def cargarDesdeTXT(nombreArchivo: str, parser) -> list:
        """
        Lee un TXT línea por línea y aplica el parser a cada una.

        Parámetros:
            nombreArchivo : str      — nombre del archivo en documentos/
            parser        : callable — función (linea: str) -> dict | None
                            Retorna un dict con los datos parseados,
                            o None para saltar la línea (vacía o inválida).

        Retorna:
            list[dict] — lista de registros parseados correctamente.

        Uso en cada model:
            registros = generadorTXT.cargarDesdeTXT("paises.txt", self._parsearLinea)
        """
        rutaArchivo = os.path.join(_rutaBase, nombreArchivo)
        if not os.path.exists(rutaArchivo):
            return []
        registros = []
        try:
            with open(rutaArchivo, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    resultado = parser(linea)
                    if resultado is not None:
                        registros.append(resultado)
        except Exception as e:
            print(f"[generadorTXT] Error al cargar {nombreArchivo}: {e}")
        return registros


    
    @staticmethod
    def registrarTXT(item,nombreArchivo):
        """
        Agrega un producto al archivo productos.txt
        en ATILogisticaAduanera/documentos/
        """
        try:
            _asegurarCarpeta()
            rutaArchivo = os.path.join(_rutaBase, nombreArchivo)
            with open(rutaArchivo, "a", encoding="utf-8") as archivo:
                archivo.write(f"{item}\n")
            print(f"[generadorTXT] Guardado en: {rutaArchivo}")
            return True
        except Exception as e:
            print(f"[generadorTXT] Error: {e}")
            return False
        



    @staticmethod
    def eliminarDelTXT(item,nombreArchivo):
        """
        Elimina un producto del archivo productos.txt
        en ATILogisticaAduanera/documentos/
        """
        try:
            _asegurarCarpeta()
            rutaArchivo = os.path.join(_rutaBase, nombreArchivo)
            if not os.path.exists(rutaArchivo):
                print(f"[generadorTXT] Archivo no encontrado: {rutaArchivo}")
                return False

            with open(rutaArchivo, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

            with open(rutaArchivo, "w", encoding="utf-8") as archivo:
                for linea in lineas:
                   if linea.strip() != item.strip():
                        archivo.write(linea)
            print(f"[generadorTXT] Eliminado del: {rutaArchivo}")
            return True
        except Exception as e:
            print(f"[generadorTXT] Error: {e}")
            return False
    
    
    
    @staticmethod
    def modificarEnTXT(id, nuevoItem, nombreArchivo):
        
        try:
            _asegurarCarpeta()
            rutaArchivo = os.path.join(_rutaBase, nombreArchivo)

            if not os.path.exists(rutaArchivo):
                print(f"[generadorTXT] Archivo no encontrado: {rutaArchivo}")
                return False

            # ── Prefijo único por el que se identifica la línea ──
            prefijo = f"ID: {id} |"

            with open(rutaArchivo, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

            encontrado = False
            with open(rutaArchivo, "w", encoding="utf-8") as archivo:
                for linea in lineas:
                    if linea.strip().startswith(prefijo):
                        archivo.write(f"{nuevoItem}\n")  # ← reemplaza
                        encontrado = True
                        print(f"[generadorTXT] ID {id} modificado en: {rutaArchivo}")
                    else:
                        archivo.write(linea)             # ← mantiene el resto

            if not encontrado:
                print(f"[generadorTXT] ID {id} no encontrado en {rutaArchivo}")
                return False

            return True
        except Exception as e:
            print(f"[generadorTXT] Error: {e}")
            return False
        
    @staticmethod
    def generarArchivo( nombreArchivo: str, contenido: str = ""):
        """
        Crea o sobreescribe un archivo en documentos/.
        """
        try:
            _asegurarCarpeta()
            rutaArchivo = os.path.join(_rutaBase, nombreArchivo)
            with open(rutaArchivo, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"[generadorTXT] Error: {e}")
            return False


        