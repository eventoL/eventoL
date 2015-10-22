Esta es una guía rápida paso a paso de cómo configurar rápidamente los datos de tu sede para empezar a utilizar el sistema.

## Registrarse como colaborador
Lo primero es registrarse como colaborador de la sede. Para esto:

* Ir a http://flisol.usla.org.ar
* Seleccionar la sede que corresponda
* En el menú superior, desplegar la sección "Colaboradores" y elegir "Registrarme como colaborador" o "Registrarme como instalador", según corresponda. El instalador puede hacer todo lo que puede hacer un colaborador y además, puede cargar instalaciones el día del evento.
* Completar los datos que solicita el formulario y enviarlo.
* Si todo salió bien, debería redirigirte a la página principal de la sede con un mensaje exitoso.
* A partir de este momento, podrás iniciar sesión con el usuario y contraseña creados.

## Administrar los datos principales de la sede
Los datos de la sede se administran desde la página de administración. Para esto:

* Ir a http://flisol.usla.org.ar/admin
* Iniciar sesión con el usuario y contraseña del colaborador.
* Aparecerá una lista de los objetos que se pueden administrar.
* De esta lista, seleccionar "Sedes" y en la siguiente pantalla, aparecerá la sede que corresponda.
* Al seleccionarla, veremos toda la información de la sede. Los datos importantes a modificar son:
  * **Información del evento**: Es un campo con un editor de texto simple. Ahí se puede poner información del evento como el lugar, hora, cómo llegar, etc. A modo de ejemplo, está el de CABA: http://flisol.usla.org.ar/sede/CABA/event. En este campo se puede poner también HTML para hacer cosas más complejas. TIP: Si no hacés cosas muy raras con el HTML, el texto va a heredar el estilo y tipografía de la página y va a quedar más bonito.
  * **Correo Electrónico**: La página tiene un formulario de contacto para cada sede. Lo que la gente mande a través de ese formulario, llegará a la dirección de correo que esté configurada en ese campo. Tiene que ser una cuenta a la que cualquiera pueda escribir (por ejemplo, no podría ser una lista a la que hay que registrarse).
  * **Fecha**: **Esto es MUY importante**. Es la fecha del día en el que se realizará el evento. En la mayoría de los casos, el 25/04. Por defecto, está en una fecha en el pasado. Esto hace que la sede no tenga habilitada la registración. Al poner la fecha correcta (en el futuro), se habilita la registración de asistentes para esa sede.
  * **Fecha límite para Propuestas**: Es la fecha límite hasta la cual se pueden enviar propuestas de charla. Pasada esa fecha, el sistema no permitirá enviar más propuestas. Por defecto, está en el pasado, por lo que hay que poner la fecha correspondiente para que se habilite el envío de propuestas de charla.
  * **Lugar**: No se usa y no es necesario configurar.
  * **URL**: Es la url para la página de la sede. Case-insensitive. Esa es la url específica que se puede distribuir (flisol.usla.org.ar/sede/**{URL}**). Recomendamos NO cambiarla.

## Administrar los contactos de la sección "Seguinos!"
Cada sede puede cargar sus propios links de contacto que aparecen en la sección "Seguinos!" del menú superior.

![seguinos](http://i58.tinypic.com/25kpro3.png)

Por defecto, cada sede tiene un contacto, que es el formulario de la página y que se envía al mail configurado en la sede. Para agregar más:

* Ingresar a la página de administración (http://flisol.usla.org.ar/admin)
* Seleccionar "Contacts".
* Hacer click en el botón "Añadir Contact" en la parte superior derecha.
* Completar el formulario con los datos:
  * **Tipo de contacto**: Por ejemplo, facebook, twitter, IRC, Lista de correos. Hay algunos predefinidos, pero si no está el que buscás, se puede agregar uno nuevo haciendo click en el "+" que tiene al lado. Los datos que pide son "Nombre" (que es por ejemplo "Wiki", "Mail") y "Class para el ícono", que es una clase de font-awesome para mostrar (http://fontawesome.io/icons/). Si tenés dudas con esto, no dudes en contactarnos!
  * **URL**: Es el link correspondiente al contacto (completo). Por ejemplo, si fuera una página de facebook, hay que poner "http://facebook.com/laPaginaDeTuSede".
  * **Texto**: Es le nombre para mostrar en el menú desplegable. Por ejemplo "Página de Facebook" o "@UsuarioDeTwitter".
  * **Sede**: La sede que corresponda.
