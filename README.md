curl -X POST "http://127.0.0.1:4999/oauth2/token/" -d "grant_type=password&username=admin&password=admin&client_id=aplicacion&client_secret=aplicacion_secret"
curl -X POST "http://127.0.0.1:4999/oauth2/token/" -d "grant_type=password&username=luisvljl564562&password=Asqwzx12&client_id=Huerto&client_secret=Huerto_secret"

Gabriela: vista Recomendacion plantas por estacion
    Creo y uso el campo epoca_siembra, accedo al mes para ver la estacion con un if en la template y hacer que se muetre el nombre de las plantas que tienen esa fecha establecida
    Hecha: he creado 4 url uno para cada estación y cada uno devuelve las plantas de esa estación


Manuel: diferenciar  huertos disponibles y no y poner una lista con los huertos disponibles
    Creo un atributo de tipo booleanfield para el modelo Huerto con el nombre "disponible" si es true se mostrará y si no no. El filtro para mostrar si sí o no se pone en la template con |yesno:"Sí,No"


Irene: en un huerto que aparezca cuando recolectar cada planta
    en el modelo planta tengo el campo recoleccion como datefield. Accedo a las plantas de un huerto en concreto y comparo las fechas del campo y la actual, si coinciden con una diferencia de más menos x días, se considerarán recolectables y se mostrarán, si no no.
Alvaro:Imagenes de las plantas 
    No funciona

Alberto: Aviso de cuando regar con alert
    acceder a la tabla intermedia de planta_regada, ver la fecha de riego, ver la fecha actual, si pasa de X tiempo, que salte el alert. 
    Para cada usuario, comprueba las plantas que tiene y la última fecha en las que fueron regadas. Al entrar en la funcionalidad, si hace más de x días que fueron regadas (comparando la fecha actual con la del registro), saltará un alert diciendo que alguna planta debe ser regada, y en el html se mostrarán en rojo las plantas que deben regarse
Ivan: plagas posibles de un huerto en funcion de sus plantas
    Tengo que modificar la relacion planta-plaga para que sea n-m, crear una intermedia y en esa poner el total de plagas por planta, acceder a ella desde huerto para ver el total de plagas que puede tener ese huerto. El calculo de las plagas diferentes por huerto lo hago en la api con un conjunto 

Elvis: Hacer login de Google
No funciona





