:fire: 
# transcribe_mp3 
:fire:
 

**-Contexto**:clipboard:


Proyecto para transcripcion y analisis de sentimientos de archivos mp3


**-Se desarrolla la solución usando:**

**Lenguaje:** :snake: Python 3.8.10

Framework para endpoint Api : Flask


**Data Storage :floppy_disk:** Firebase

**Requests :satellite:**

**/** [POST]-> No nesecita Login solo para verificar disponibilidad de la API

**/login** [POST]-> Logearse en la api para acceder al token y usar las rutas de la funcionalidad que solicitan autenticacion con token, se puede usar como prueba de acceso los parametros: user = user1,pass=pass1

**/verify** [POST]-> Verificar token

**/new_user** [POST]-> Crear usuario: nesecita token | Parametros: user = 'nombre usuario' , pass = 'password de usuario'

**/transcode** [POST]-> Enviar ruta de archivo mp3 para generar el analisis de sentimientos y las palabras a buscar en este archivo| Parametros: route = ruta absoluta de el archivo mp3 a analisar , words = lista de palabras a buscar separadas por coma

**/history** [GET]-> Traer el historial de analisis realizados




