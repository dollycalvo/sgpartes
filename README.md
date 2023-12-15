# sgpartes
Sistema de control de planillas horarias 

# Correr el comando para agregar agentes
En el proyecto *partes*, en el directorio management/commands encontraremos el archivo *crear_usuarios.py* en el cual se puede manejar la lista de agentes que la base de datos debe contener.
El modo de ejecutar este comando es desde la línea de comandos de la siguiente manera:
```python manage.py crear_usuarios```

# Códigos en la planilla
Para ausencias y motivos especiales, existe un código en la base de datos y otro como etiqueta para el usuario.
En el archivo **/partes/templatetags/filters.py** se encontrará un filtro personalizado que se usa en el template HTML, el cual devuelve la etiqueta para mostrar al usuario a partir del código en la base de datos. Cuando se agregue un nuevo código, además de modificar el template HTML, habrá que modificar este filtro para incluirlo.
A su vez, en el archivo **/partes/helper.py** existe una función que hace también esta conversión pero para ser utilizada en el backend.

# Envío de e-mail al presentar planilla
Para pruebas locales se configuró un servidor con la aplicación de Windows hMailServer (código abierto).
La configuración fue realizada siguiendo este tutorial:
https://medium.com/@coffmans/setup-your-own-simple-smtp-server-how-to-c9159cfc7934
Como domain se utilizó cguimaraenz.com, y como e-mail webmaster@cguimaraenz.com
Éstos han sido hard-codeados en el archivo views.py para las pruebas, y fueron comentadas las líneas en las que debería tomar las direcciones de e-mail de agentes y jefes.
Los e-mails se podrán ver en la carpeta "C:\Program Files (x86)\hMailServer\Data\cguimaraenz.com\webmaster\XX" (según la configuración mencionada anteriormente). Los archivos son de extensión .eml y se puede ver en cualquier editor de texto.