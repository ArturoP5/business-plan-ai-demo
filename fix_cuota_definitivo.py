#!/usr/bin/env python3
"""
Arreglar definitivamente el campo cuota_mercado
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar y reemplazar toda la definición de cuota_mercado
for i in range(1645, 1665):
    if 'cuota_mercado = st.number_input(' in lines[i]:
        print(f"Reconstruyendo cuota_mercado desde línea {i+1}")
        
        # Buscar donde termina (el paréntesis de cierre)
        end_line = i
        for j in range(i, min(i+15, len(lines))):
            if ')' in lines[j] and 'help=' in lines[j-1]:
                end_line = j
                break
        
        # Crear la definición correcta
        nueva_definicion = '''            cuota_mercado = st.number_input(
                "Cuota de Mercado (%)",
                min_value=0.0,
                max_value=100.0,
                value=datos_excel["info_general"].get("cuota_mercado", 0.0) if datos_excel else 0.0,
                step=0.5,
                key="cuota_mercado_sidebar",
                help="% estimado en su segmento"
            )
'''
        
        # Reemplazar las líneas
        new_lines = lines[:i] + [nueva_definicion] + lines[end_line+1:]
        
        # Guardar
        with open('app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ cuota_mercado reconstruido correctamente")
        break

