# sgpartes
Sistema de control de planillas horarias 

# Correr el comando para agregar agentes
En el proyecto *partes*, en el directorio management/commands encontraremos el archivo *crear_usuarios.py* en el cual se puede manejar la lista de agentes que la base de datos debe contener.
El modo de ejecutar este comando es desde la línea de comandos de la siguiente manera:
```python manage.py crear_usuarios```

# Códigos en la planilla
Para ausencias y motivos especiales, existe un código en la base de datos y otro como etiqueta para el usuario.
En el archivo **/partes/templatetags/filters.py** se encontrará un filtro personalizado que se usa en el template HTML, el cual devuelve la etiqueta para mostrar al usuario a partir del código en la base de datos. Cuando se agregue un nuevo código, además de modificar el template HTML, habrá que modificar este filtro para incluirlo.