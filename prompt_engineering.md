# Ejercicio 1:
<img width="954" height="501" alt="image" src="https://github.com/user-attachments/assets/2c241b85-51dd-41fe-8dad-c81038356c59" />

#### Resultado prompt simple
```import re

def validar_contraseña(password: str) -> bool:
    """
    Valida si una contraseña cumple con los requisitos de seguridad:
    - Al menos 8 caracteres.
    - Contiene al menos una letra mayúscula.
    - Contiene al menos una letra minúscula.
    - Contiene al menos un número.
    - Contiene al menos un carácter especial.
    
    Retorna True si la contraseña es válida, False en caso contrario.
    """

    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Z]", password):  # al menos una mayúscula
        return False
    
    if not re.search(r"[a-z]", password):  # al menos una minúscula
        return False
    
    if not re.search(r"[0-9]", password):  # al menos un número
        return False
    
    if not re.search(r"[@$!%*?&]", password):  # al menos un caracter especial
        return False
    
    return True

# Ejemplo de uso:
print(validar_contraseña("Hola123!"))  # ✅ True
print(validar_contraseña("hola123"))   # ❌ False
 ```
