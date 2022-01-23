## Contribuyendo

Primero, gracias por considerar contribuir a EventoL. Por gente
como tú, es que EventoL es una gran herramienta.

### 1. ¿A dónde voy desde aquí?

Si ha notado un error o tiene una pregunta primero busca en
[grupo de soporte](https://t.me/eventol_soporte) o [Stack Overflow](https://es.stackoverflow.com/) y [issues](https://github.com/eventoL/eventoL/issues) para ver si
alguien más en la comunidad ya ha creado un issue.
Si no, adelante y [crea un issue](https://github.com/eventoL/eventoL/issues/new/choose)!

### 2. Fork y crea una rama

Si esto es algo que cree que puede solucionar, entonces crea un [fork Eventol](https://github.com/eventoL/eventoL) y
crea una rama con un nombre descriptivo.

Un buen nombre de rama sería (el número de la issue en el que está trabajando y algun texto):

```sh
# Example issue: 325 Add japanese trasnlations
git checkout -b 325-add-japanese-translations
```

### 3. Configure el entorno de desarrollo y pruebas

Asegúrate de estar usando un python reciente (3.5 o mayor) y tener instalado npm.
También hay una forma de tener el entorno solamente con docker para eso mira en la [documentación de intalación](http://eventol.github.io/eventoL/#/es/installation).

### 4. ¿Encontraste un error?

* **Asegúrese de que el error no haya sido informado** en las [issues](https://github.com/eventoL/eventoL/issues).

* Si no puede encontrar una issue abierta que aborde el problema,
  [abri uno nuevo](https://github.com/eventoL/eventoL/issues/new/choose).
  Para poder tener una issue correctamente informada, siga la instrucciones indicadas en la template seleccionada.

### 5. Implementa tu corrección o funcionalidad

En este punto, ¡estás listo para hacer tus cambios! Siéntase libre de pedir ayuda;
todos son principiantes al principio.

### 6. Visualiza tus cambios en una aplicación

Es importante que antes de enviar tu codigo lo pruebes bien localmente.
Para lograr eso podes seguir los pasos de [guia de instalación](http://eventol.github.io/eventoL/#/es/installation)

### 7. Obtener el estilo correcto

Su parche debe seguir las mismas convenciones y pasar la misma calidad de código
que el resto del proyecto. *Pylint* y *Eslint* te darán
retroalimentación al respecto.
Puedes verificar y corregir los comentarios ejecutandolo
localmente usando el [script de test](http://eventol.github.io/eventoL/#/es/test_script).

### 8. Hacer una Pull request

En este punto, debe volver a la rama principal y asegurarse de que sea compatible con la rama principal en este momento:

```sh
git remote add upstream git@github.com:eventoL/eventoL.git
git checkout master
git pull upstream master
```

Luego actualice su rama desde su copia local de master, ¡y subilo!

```sh
git checkout 325-add-japanese-translations
git rebase master
git push - origin set-upstream 325-add-japanese-translations
```

Finalmente, ve a GitHub y [crea un pull request](https://github.com/eventoL/eventoL/compare):

Travis CI ejecutará nuestro conjunto de pruebas.
Su PR no se fusionará hasta que todas las pruebas pasen.
También gitlab va a correr los linters (tanto de python como de react) y los tests de python y react.

### 8. Mantene actualizado su pull request

Siempre que el master tenga un cambio es recomendable que actualice el pull request.

```sh
git checkout 325-add-japanese-translations
git pull --rebase upstream master
git push --force-with-lease 325-add-japanese-translations
```

### 10. Fusión de un RP (solo administradores)

Un RP solo puede fusionarse en master por un administrador si:

* Está pasando CI.
* Está pasando cada linter.
* No tiene cambios solicitados.
* Está actualizado con el master actual.

Cualquier administrador puede fusionar un PR si todas estas condiciones se cumplen.

### 11. Envío de una publicación (solo adminstradores)

Los adminstradores deben hacer lo siguiente para lanzar una versión:

* Asegúrese de que todos los pull requests estén dentro y que el registro de cambios esté actualizado
* Actualice el archivo de changelog con el nuevo número de versión
* Crear un tag para esa versión (este tag tiene que estar firmado)

### 12. Links importantes

* **Documentación oficial**: http://eventol.github.io/eventoL/#/
* **Grupo de telegram de soporte**: https://t.me/eventol_soporte
* **Repositorio oficial**: https://github.com/eventoL/eventoL
* **Issues**: https://github.com/eventoL/eventoL/issues
* **Pull requests**: https://github.com/eventoL/eventoL/pulls
* **Repositorio mirror de gitlab para pipelines**: https://gitlab.com/eventol/eventoL
* **Pipelines de gitlab**: https://gitlab.com/eventol/eventoL/pipelines
* **Reporte de Coveralls**: https://coveralls.io/github/eventoL/eventoL?branch=master
* **Issue dashboard**: https://waffle.io/eventoL/eventoL
* **Traducciones en weblate**: https://hosted.weblate.org/projects/eventol/
* **Build de travis**: https://travis-ci.org/eventoL/eventoL