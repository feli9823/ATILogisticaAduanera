#Archivo de constantes para estilos y colores


BG_COLOR    = "#121212"   # fondo principal oscuro
TEXT_COLOR  = "#FFFFFF"   # texto blanco    
BTN_BG      = "#FFFFFF"   # fondo del botón
BTN_TEXT    = "#121212"   # texto del botón 



# ─────────────────────────────────────────────
#  Colores internos
# ─────────────────────────────────────────────
tableHeaderBg = "#1A1A2E"
tableRowBg    = "#1E1E2E"
tableRowAlt   = "#252535"
borderColor   = "#2A2A3E"
accentColor   = "#D8C0F5"
btnAddBg      = "#CBA6F7"
btnAddText    = "#121212"




""""
BG_COLOR #121212 — Negro carbón
Fondo de toda la aplicación. Lo ves detrás de cada vista: login, dashboard, productos, etc.

TEXT_COLOR #FFFFFF — Blanco puro
Texto principal en cualquier parte. Títulos de vistas ("Lista de productos"), valores dentro de las celdas de la tabla, nombre de la app en el sidebar.

BTN_BG #FFFFFF — Blanco puro
Fondo del botón "Empezar" en la pantalla de bienvenida y el botón "Iniciar Sesión" en el login. Solo se usa en esas dos vistas de entrada.

BTN_TEXT #121212 — Negro carbón
Texto de esos mismos botones de entrada para que el negro contraste sobre el fondo blanco.

tableHeaderBg #1A1A2E — Azul marino muy oscuro
Fila de encabezado de todas las tablas. La franja donde dice "ID", "Nombre", "Acciones", etc.

tableRowBg #1E1E2E — Azul noche oscuro
Filas pares de las tablas (0, 2, 4…). Ligeramente más claro que el fondo general para que la tabla se distinga.

tableRowAlt #252535 — Azul pizarra oscuro
Filas impares (1, 3, 5…). Alterna con tableRowBg para crear el efecto de rayas zebra y facilitar la lectura fila por fila.

borderColor #2A2A3E — Azul grisáceo oscuro
Bordes de tablas, líneas divisoras entre filas, y el borde de los TextField cuando no están en foco. También el Divider debajo del título en cada vista.

accentColor #D8C0F5 — Lavanda (Mauve)
El color más visible de la interfaz. Se usa en los títulos de columnas de tablas, el ícono y nombre "ATI Logística" en el sidebar, el ítem activo del sidebar, el borde del TextField cuando está en foco, los botones "Cerrar" en diálogos de detalle, y el texto del Costo Total en consultasVentas.

btnAddBg #CBA6F7 — Lavanda (Mauve)
Fondo de los botones de acción principal dentro de las vistas: "Añadir producto", "Añadir país", "Añadir venta", "Enviar al correo" y el botón "Guardar" en los diálogos. Es el mismo valor que accentColor pero semánticamente separado para botones.

btnAddText #121212 — Negro carbón
Texto e íconos dentro de esos botones lavanda, para garantizar contraste legible sobre el fondo claro.






"""