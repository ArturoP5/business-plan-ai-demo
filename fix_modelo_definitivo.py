#!/usr/bin/env python3
"""
Corregir definitivamente el selectbox de modelo_negocio
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar el modelo_negocio mal formateado
for i in range(len(lines)):
    if 'modelo_negocio = st.selectbox(' in lines[i]:
        print(f"Encontrado modelo_negocio en línea {i+1}")
        
        # Reemplazar desde esta línea hasta encontrar "with col2_est:"
        j = i
        while j < len(lines) and 'with col2_est:' not in lines[j]:
            j += 1
        
        print(f"Reemplazando líneas {i+1} a {j}")
        
        # Crear el selectbox correcto
        nuevo_codigo = """            modelo_negocio = st.selectbox(
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
            if datos_excel and "modelo_negocio" in datos_excel["info_general"]:
                modelo_negocio = datos_excel["info_general"]["modelo_negocio"]
        
"""
        
        # Reemplazar las líneas problemáticas
        new_lines = lines[:i] + [nuevo_codigo] + lines[j:]
        
        # Guardar
        with open('app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ Corregido modelo_negocio")
        break

