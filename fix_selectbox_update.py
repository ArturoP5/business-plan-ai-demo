#!/usr/bin/env python3
"""
Arreglar la actualización de los selectbox cuando se carga una empresa demo
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar la sección de modelo_negocio y cambiar cómo se maneja
for i, line in enumerate(lines):
    if 'modelo_negocio = st.selectbox(' in line and i > 1560 and i < 1580:
        print(f"Encontrado modelo_negocio en línea {i+1}")
        
        # Buscar donde termina el selectbox
        for j in range(i, min(i+15, len(lines))):
            if ')' in lines[j] and 'help=' in lines[j-1]:
                
                # Buscar las líneas después del selectbox donde se actualiza con datos_excel
                for k in range(j+1, min(j+5, len(lines))):
                    if 'if datos_excel and "modelo_negocio"' in lines[k]:
                        print(f"  Encontrada actualización en línea {k+1}")
                        # Eliminar esta línea y la siguiente (que hace la asignación incorrecta)
                        lines[k] = ""
                        if k+1 < len(lines) and 'modelo_negocio = datos_excel' in lines[k+1]:
                            lines[k+1] = ""
                        break
                
                # Ahora vamos a reconstruir el selectbox correctamente
                # Necesitamos que use el índice correcto basado en datos_excel
                opciones_modelo = [
                    "B2B - Venta a empresas",
                    "B2C - Venta a consumidores",
                    "B2B2C - Mixto",
                    "SaaS - Software como servicio",
                    "Marketplace - Plataforma",
                    "Suscripción - Pagos recurrentes",
                    "Freemium - Gratuito con opciones de pago"
                ]
                
                # Crear el nuevo código del selectbox con index dinámico
                nuevo_selectbox = f'''            # Determinar el índice para modelo_negocio
            modelo_negocio_opciones = {opciones_modelo}
            modelo_negocio_index = 0
            if datos_excel and "modelo_negocio" in datos_excel["info_general"]:
                valor_excel = datos_excel["info_general"]["modelo_negocio"]
                if valor_excel in modelo_negocio_opciones:
                    modelo_negocio_index = modelo_negocio_opciones.index(valor_excel)
            
            modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                modelo_negocio_opciones,
                index=modelo_negocio_index,
                help="Seleccione el modelo de negocio principal"
            )
'''
                
                # Reemplazar el selectbox actual
                # Primero eliminar el actual
                lines_to_replace = []
                for idx in range(i, j+1):
                    lines_to_replace.append(idx)
                
                # Insertar el nuevo
                new_lines = lines[:i] + [nuevo_selectbox] + lines[j+1:]
                lines = new_lines
                break
        break

# Hacer lo mismo para posicionamiento_precio
for i, line in enumerate(lines):
    if 'posicionamiento_precio = st.selectbox(' in line and i > 1570 and i < 1620:
        print(f"Encontrado posicionamiento_precio en línea {i+1}")
        
        # Similar al anterior, agregar manejo de índice
        for j in range(i, min(i+15, len(lines))):
            if ')' in lines[j] and 'help=' in lines[j-1]:
                
                # Eliminar actualización incorrecta si existe
                for k in range(j+1, min(j+5, len(lines))):
                    if 'if datos_excel and "posicionamiento_precio"' in lines[k]:
                        lines[k] = ""
                        if k+1 < len(lines):
                            lines[k+1] = ""
                        break
                
                opciones_precio = [
                    "Premium - Alto valor",
                    "Medio - Calidad-precio",
                    "Low-cost - Precio bajo",
                    "Freemium - Gratuito con opciones de pago",
                    "Variable - Según segmento"
                ]
                
                nuevo_selectbox = f'''            # Determinar el índice para posicionamiento_precio
            posicionamiento_opciones = {opciones_precio}
            posicionamiento_index = 0
            if datos_excel and "posicionamiento_precio" in datos_excel["info_general"]:
                valor_excel = datos_excel["info_general"]["posicionamiento_precio"]
                if valor_excel in posicionamiento_opciones:
                    posicionamiento_index = posicionamiento_opciones.index(valor_excel)
            
            posicionamiento_precio = st.selectbox(
                "Posicionamiento de Precio",
                posicionamiento_opciones,
                index=posicionamiento_index,
                help="¿Cómo se posiciona en precio vs competencia?"
            )
'''
                
                new_lines = lines[:i] + [nuevo_selectbox] + lines[j+1:]
                lines = new_lines
                break
        break

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Selectboxes arreglados para usar índices dinámicos")
print("Ahora los valores se mostrarán correctamente al cargar empresas demo")

