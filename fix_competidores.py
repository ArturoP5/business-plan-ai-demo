#!/usr/bin/env python3
"""
Corregir el campo competidores_principales mal formateado
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar y corregir competidores_principales
for i in range(len(lines)):
    if 'competidores_principales = st.text_area(' in lines[i]:
        print(f"Encontrado competidores_principales en línea {i+1}")
        
        # Buscar hasta donde debería terminar (siguiente campo st. o línea vacía significativa)
        j = i + 1
        while j < len(lines) and not ('= st.' in lines[j] or 'vision_corto' in lines[j]):
            j += 1
        
        print(f"Reemplazando líneas {i+1} a {j}")
        
        # Crear el campo correcto
        nuevo_campo = """        competidores_principales = st.text_area(
            "Top 3 Competidores Principales",
            placeholder="Ej: Competidor A (40% mercado), Competidor B (25%), Competidor C (20%)",
            value=datos_excel["info_general"].get("competidores_principales", "") if datos_excel else "",
            height=70,
            help="Identifique sus principales competidores y su participación de mercado"
        )
        
"""
        
        # Reemplazar
        new_lines = lines[:i] + [nuevo_campo] + lines[j:]
        
        # Guardar
        with open('app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ Corregido competidores_principales")
        break

