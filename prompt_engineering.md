# Ejercicio 1:
* Prompt simple link: https://chatgpt.com/share/68bdc6d3-b3b8-8008-9e86-004d4f57137f
* Prompt avanzado link: https://chatgpt.com/share/68bdc67f-d324-8008-a29d-3b36fea8f449

#### Resultado prompt simple
```
import re

def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si una contraseña cumple con los siguientes criterios:
    1. Longitud mínima de 8 caracteres.
    2. Contiene al menos una letra mayúscula.
    3. Contiene al menos una letra minúscula.
    4. Contiene al menos un número.
    5. Contiene al menos un carácter especial (!@#$%^&*()-_+=<>?/).

    Retorna:
        True si cumple todos los criterios, False en caso contrario.
    """
    if len(contrasena) < 8:
        return False
    
    if not re.search(r"[A-Z]", contrasena):
        return False
    
    if not re.search(r"[a-z]", contrasena):
        return False
    
    if not re.search(r"[0-9]", contrasena):
        return False
    
    if not re.search(r"[!@#$%^&*()\-\_=+<>?/]", contrasena):
        return False
    
    return True


# Ejemplo de uso
print(validar_contrasena("Hola123!"))   # True
print(validar_contrasena("hola123"))    # False

```

### Resultado prompt avanzado 
 ```
def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si una contraseña cumple con los criterios de seguridad definidos.

    Reglas de validación:
    1. Longitud mínima de 12 caracteres.
    2. Debe contener al menos una letra mayúscula (A-Z).
    3. Debe contener al menos una letra minúscula (a-z).
    4. Debe contener al menos un número (0-9).
    5. Debe contener al menos un carácter especial (@, #, $, %, &, !).

    Parámetros:
        contrasena (str): La contraseña a validar.

    Retorna:
        bool: True si cumple con todos los criterios de seguridad, 
              False en caso contrario.
    """
    if len(contrasena) < 12:
        return False

    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    caracteres_especiales = "@#$%&!"
    tiene_especial = any(c in caracteres_especiales for c in contrasena)

    return all([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])


# Ejemplos de uso:

# Ejemplo válido
print(validar_contrasena("ContrasenaFuerte123!"))  
# True → cumple todos los criterios

# Ejemplo inválido (menos de 12 caracteres)
print(validar_contrasena("Abc123!"))  
# False → falla por longitud insuficiente

# Ejemplo inválido (sin caracteres especiales)
print(validar_contrasena("PasswordSegura123"))  
# False → falla por no contener un carácter especial
 ```

### 1.C: Evaluación Comparativa
* Completitud: ¿La función del prompt simple incluyó todas las reglas?
    * Si incluyo todas las reglas al igual que el prompt avanzado.
* Claridad: ¿El código está bien documentado? ¿Es fácil de entender?
    * Si, ambos codigos estan documentados, pero la documentacion del prompt avanzado es más detallada.
* Utilidad: ¿El prompt avanzado proporcionó ejemplos de uso que facilitan la prueba y la integración?
    * Si, el prompt avanzado proporcionó estas pruebas
* Robustez: ¿La función maneja casos borde que el prompt simple podría haber ignorado?
    * Si, el prompt avanzado incluye casos que el prompt simple no incluyó.

# Ejercicio 2: 
* Prompt simple link: https://chatgpt.com/share/68bdd7e3-98b8-8008-8dc2-d6434139c6f3
* Prompt avanzado link: https://chatgpt.com/share/68bdd851-ac30-8008-b02a-3cebd00caecb

#### Resultado prompt simple

```
{
  "evento": "Reunión de lanzamiento",
  "proyecto": "Proyecto Fénix",
  "fecha": "2024-10-15",
  "hora": "10:30 AM",
  "lugar": "Sala Júpiter",
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ],
  "presupuesto": {
    "monto": 25000,
    "moneda": "USD"
  }
}
 ```
### Resultado prompt avanzado 

 ```
{
  "proyecto": {
    "nombre": "Proyecto Fénix",
    "presupuesto": {
      "monto": 25000,
      "moneda": "USD"
    }
  },
  "reunion": {
    "fecha": "2024-10-15",
    "hora": "10:30",
    "ubicacion": "Sala Júpiter"
  },
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ]
}
 ```

#### 2.C: Evaluación Comparativa

* Estructura: ¿El JSON del prompt simple tiene una estructura lógica y predecible?
    * Si, tiene una estructura bastante clara que es oportuna con la información del texto, pero es menos simple y estructurada que la del prompt avanzado donde se agrupan mejor las cosas.     
* Precisión: ¿Los tipos de datos son correctos (números vs. strings)?
    * Si, son correctos 
* Parseabilidad: ¿El JSON generado por el prompt avanzado es directamente utilizable por una aplicación sin necesidad de limpieza o conversión?
    * Si, este prompt avanzado y el simple ambos son utilizables sin necesidad de conversión     
* Manejo de Nulos: ¿Cómo manejaría cada uno un texto donde, por ejemplo, el presupuesto no se menciona?
    * En el caso de este ejemplo no se ve la extracción de un valor nulo, pero para el caso del prompt avanzado seguramente lo pondría como nulo, y en el prompt simple posiblemente no lo colocaría.
   
# Ejercicio 3: 
* Prompt simple link: https://chatgpt.com/share/68bde864-a4c0-8008-a25a-956d4a1936ce
* Prompt avanzado link: https://chatgpt.com/share/68bde8af-c15c-8008-9ff5-41bcf6038c6a

#### Resultado prompt simple

 ```
Los **agujeros negros** son uno de los fenómenos más fascinantes y enigmáticos del universo. Se forman cuando una gran cantidad de materia se concentra en un espacio extremadamente pequeño, generando una gravedad tan intensa que ni siquiera la luz puede escapar de su atracción. Este límite a partir del cual nada puede salir se conoce como el **horizonte de sucesos**.

Existen diferentes tipos de agujeros negros, clasificados principalmente por su tamaño y origen. Los **agujeros negros estelares** se forman tras el colapso gravitatorio de estrellas muy masivas al final de su vida. Por otro lado, los **agujeros negros supermasivos**, que pueden tener millones o incluso miles de millones de veces la masa del Sol, se encuentran en el centro de la mayoría de las galaxias, incluida la Vía Láctea. También se han propuesto agujeros negros de tamaño intermedio e incluso primordiales, que podrían haberse originado poco después del Big Bang.

A pesar de su fama como “devoradores cósmicos”, los agujeros negros no funcionan como aspiradoras espaciales que succionan todo indiscriminadamente. Los objetos que orbitan a una distancia segura pueden hacerlo de manera estable, tal como los planetas orbitan alrededor del Sol. Sin embargo, si un objeto cruza el horizonte de sucesos, ya no podrá escapar.

Uno de los grandes avances en el estudio de los agujeros negros fue la predicción de **Stephen Hawking** en la década de 1970, conocida como la **radiación de Hawking**. Según esta teoría, los agujeros negros no son completamente “negros”, sino que emiten una leve radiación debido a efectos cuánticos. Esto implicaría que, con el tiempo, podrían evaporarse.

Hoy en día, los astrónomos han podido observar indirectamente a los agujeros negros mediante la detección de ondas gravitacionales, producidas cuando dos de ellos se fusionan, y a través de imágenes como la obtenida en 2019 por el Telescopio del Horizonte de Sucesos, que mostró por primera vez la “sombra” de un agujero negro.

👉 En resumen, los agujeros negros no solo son laboratorios naturales para entender la gravedad y la física extrema, sino también piezas clave para comprender la evolución de las estrellas, las galaxias y quizá, el destino mismo del universo.

¿Quieres que lo organice en un **ensayo corto** (introducción, desarrollo y conclusión) o prefieres un **texto más divulgativo con curiosidades**?
 ```
### Resultado prompt avanzado 

 ```
Imagina un lugar en el universo donde la gravedad es tan fuerte que nada, ni siquiera la luz, puede escapar: eso es un agujero negro. Es como un aspirador cósmico escondido en la oscuridad, invisible a nuestros ojos, pero detectable por cómo hace bailar a las estrellas cercanas y por la luz que engulle sin devolver. No es un monstruo que persigue, sino más bien una puerta misteriosa que guarda secretos del espacio y del tiempo. Al estudiarlos, los científicos descubren cómo funciona el universo en sus rincones más extremos, como si fueran guardianes silenciosos de un gran enigma.
 ```

#### 3.C: Evaluación Comparativa

* Adecuación a la Audiencia: ¿Qué respuesta es más apropiada y comprensible para un niño?
    *  La del prompt avanzado, ya que aunque es más extensa y detallada la respuesta del prompt simple, al ser tan extenso y detallado, puede no ser la respuesta más apropiada para un niño.
* Tono: ¿Logró el prompt simple capturar el tono de asombro solicitado?
    * Si, tiene un cierto tono de misterio que se mantiene a lo largo del texto.      
* Creatividad: ¿Qué respuesta es más original y memorable?
    * La respuesta del prompt simple es más original, en el sentido de que la IA lo hice sin tener en cuenta tantas restricciones, solo la solicitud del usuario, pero en terminos practicas, es más memorable y más util la respuesta del prompt avanzado ya que encapsula la información de forma más resumida
* Cumplimiento de Restricciones: ¿El prompt avanzado logró evitar la jerga técnica como se le pidió?
    * Si, si lo logró como le fue solicitado.         
