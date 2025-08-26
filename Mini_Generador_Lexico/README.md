# Analizador Léxico Simple

Este proyecto implementa un **analizador léxico básico en Python**.  
El programa identifica y clasifica tokens en las siguientes categorías:

- **Number** → Números enteros válidos.  
- **Float** → Números flotantes válidos (con punto decimal).  
- **String** → Cadenas alfanuméricas.  
- **Error** → Tokens no reconocidos como válidos.  

---

## Funcionamiento

1. El programa solicita al usuario ingresar valores separados por espacios.  
2. Cada valor se analiza y clasifica según su tipo de token.  
3. Finalmente, se muestra una tabla con cada token y su tipo detectado.  

---

## Código Principal

```python
# Ejemplo de ejecución
input_text = input("Enter values separated by spaces: ")
print_token_analysis(input_text)
```

---

## Resultados de Ejecución


![Ejecución del programa](Mini_Generador_Lexico\image.png)C:\Users\leoba\OneDrive\Documentos\GitHub\SEM_Traductores_II\Mini_Generador_Lexico\README.md


---

##  Requisitos

- Python 3.x instalado.  

---

## Ejecución

Ejecuta el programa con:

```bash
python analizador.py
```

