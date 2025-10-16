#!/usr/bin/env python3
"""
Arreglar definitivamente el selectbox de modelo_negocio
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar modelo_negocio alrededor de la línea 1590
for i in range(1585, 1600):
    if 'modelo_negocio = st.selectbox(' in lines[i]:
        print(f"Encontrado modelo_negocio en línea {i+1}")
        
        # Buscar donde termina este selectbox
        end_line = i
        for j in range(i, min(i+20, len(lines))):
            if ')' in lines[j]:
                end_line = j
                break
        
        print(f"Selectbox termina en línea {end_line+1}")
        
        # Ver si hay algo después que intente actualizar modelo_negocio
        for k in range(end_line+1, min(end_line+10, len(lines))):
            if 'modelo_negocio = datos_excel' in lines[k] or 'if datos_excel and "modelo_negocio"' in lines[k]:
                print(f"Eliminando actualización incorrecta en línea {k+1}")
                lines[k] = ""
                if k+1 < len(lines) and 'modelo_negocio = ' in lines[k+1]:
                    lines[k+1] = ""
        
        # Reconstruir el selectbox con índice dinámico
        nuevo_codigo = '''            # Configurar modelo de negocio con índice dinámico
            modelo_negocio_opciones = [
                "B2B - Venta a empresas", 
                "B2C - Venta a consumidores",
                "B2B2C - Mixto",
                "SaaS - Software como servicio",
                "Marketplace - Plataforma",
                "Suscripción - Pagos recurrentes",
                "Freemium - Gratuito con opciones de pago"
            ]
            
            # Determinar el índice basado en datos_excel
            modelo_negocio_index = 0
            if datos_excel and "modelo_negocio" in datos_excel["info_general"]:
                valor_modelo = datos_excel["info_general"]["modelo_negocio"]
                try:
                    modelo_negocio_index = modelo_negocio_opciones.index(valor_modelo)
                except ValueError:
                    # Si el valor no está en la lista, usar el default
                    modelo_negocio_index = 0
            
            modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                modelo_negocio_opciones,
                index=modelo_negocio_index,
                help="Seleccione el modelo de negocio principal"
            )
'''
        
        # Reemplazar las líneas
        new_lines = lines[:i] + [nuevo_codigo] + lines[end_line+1:]
        
        # Guardar
        with open('app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ modelo_negocio arreglado con índice dinámico")
        break

