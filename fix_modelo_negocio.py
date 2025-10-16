#!/usr/bin/env python3
"""
Arreglar el selectbox de modelo_negocio de forma más simple
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar la línea del modelo_negocio
for i, line in enumerate(lines):
    if 'modelo_negocio = st.selectbox(' in line:
        print(f"Encontrado modelo_negocio en línea {i+1}")
        
        # Buscar las siguientes 15 líneas para ver la estructura completa
        print("\nEstructura actual:")
        for j in range(i, min(i+15, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        
        # Buscar dónde termina este selectbox (donde está el paréntesis de cierre)
        paren_count = 0
        end_line = i
        for j in range(i, min(i+20, len(lines))):
            paren_count += lines[j].count('(') - lines[j].count(')')
            if paren_count == 0 and j > i:
                end_line = j
                break
        
        print(f"\nSelectbox termina en línea {end_line+1}")
        
        # Ahora vamos a reconstruir este selectbox correctamente
        # Primero, extraer las opciones
        opciones_modelo = [
            "B2B - Venta a empresas",
            "B2C - Venta a consumidores", 
            "B2B2C - Mixto",
            "SaaS - Software como servicio",
            "Marketplace - Plataforma",
            "Suscripción - Pagos recurrentes",
            "Freemium - Gratuito con opciones de pago"
        ]
        
        # Crear el nuevo selectbox
        nuevo_selectbox = '''            modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                ["B2B - Venta a empresas", 
                 "B2C - Venta a consumidores",
                 "B2B2C - Mixto",
                 "SaaS - Software como servicio",
                 "Marketplace - Plataforma",
                 "Suscripción - Pagos recurrentes",
                 "Freemium - Gratuito con opciones de pago"],
                help="Seleccione el modelo de negocio principal"
            )
            # Si hay datos de excel, actualizar el valor
            if datos_excel and "modelo_negocio" in datos_excel["info_general"]:
                modelo_negocio = datos_excel["info_general"]["modelo_negocio"]
'''
        
        # Reemplazar las líneas
        new_lines = lines[:i] + [nuevo_selectbox] + lines[end_line+1:]
        
        # Guardar
        with open('app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("\n✅ modelo_negocio arreglado")
        break

