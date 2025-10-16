#!/usr/bin/env python3
"""
Agrega defaults y values a TODOS los campos estratégicos
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Agregar ALL defaults después de default_productos (alrededor de línea 1373)
for i in range(1370, 1380):
    if "default_productos = datos_excel['info_general'].get('productos_servicios', '')" in lines[i]:
        new_defaults = """        default_modelo_negocio = datos_excel['info_general'].get('modelo_negocio', 'B2C - Venta a consumidores')
        default_competidores = datos_excel['info_general'].get('competidores_principales', '')
        default_vision_corto = datos_excel['info_general'].get('vision_corto_plazo', '')
        default_vision_medio = datos_excel['info_general'].get('vision_medio_plazo', '')
        default_vision_largo = datos_excel['info_general'].get('vision_largo_plazo', '')
        default_ventaja_competitiva = datos_excel['info_general'].get('ventaja_competitiva_principal', '')
        default_principales_riesgos = datos_excel['info_general'].get('principales_riesgos', '')
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults para campos estratégicos cuando hay datos")
        break

# 2. Agregar defaults vacíos en el else (alrededor de línea 1468)
for i in range(1465, 1475):
    if 'default_productos = ""' in lines[i]:
        new_defaults = """        default_modelo_negocio = "B2C - Venta a consumidores"
        default_competidores = ""
        default_vision_corto = ""
        default_vision_medio = ""
        default_vision_largo = ""
        default_ventaja_competitiva = ""
        default_principales_riesgos = ""
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults vacíos para campos estratégicos")
        break

# 3. Agregar value a modelo_negocio selectbox (línea ~1580)
for i in range(1578, 1595):
    if 'modelo_negocio = st.selectbox(' in lines[i]:
        # Buscar el cierre del selectbox
        for j in range(i+1, i+15):
            if '"Otro"],' in lines[j]:
                # Agregar el value después de la lista
                lines[j] = lines[j].replace(
                    '"Otro"],',
                    '"Otro"],\n                index=["B2B - Venta a empresas", "B2C - Venta a consumidores", "B2B2C - Mixto", "SaaS - Software como servicio", "Marketplace - Plataforma", "Fabricación - Producción propia", "Servicios - Consultoría/Profesional", "Retail - Venta minorista", "Otro"].index(default_modelo_negocio) if "default_modelo_negocio" in locals() and default_modelo_negocio in ["B2B - Venta a empresas", "B2C - Venta a consumidores", "B2B2C - Mixto", "SaaS - Software como servicio", "Marketplace - Plataforma", "Fabricación - Producción propia", "Servicios - Consultoría/Profesional", "Retail - Venta minorista", "Otro"] else 0,'
                )
                print("✅ Agregado value a modelo_negocio")
                break
        break

# 4. Agregar value a competidores (línea ~1605)
for i in range(1603, 1610):
    if 'competidores_principales = st.text_area(' in lines[i]:
        # Buscar el placeholder
        for j in range(i+1, i+5):
            if 'placeholder=' in lines[j]:
                lines.insert(j, '            value=default_competidores if "default_competidores" in locals() else "",\n')
                print("✅ Agregado value a competidores")
                break
        break

# 5. Agregar value a vision_corto (línea ~1614)  
for i in range(1612, 1620):
    if 'vision_corto = st.text_area(' in lines[i]:
        for j in range(i+1, i+5):
            if 'placeholder=' in lines[j]:
                lines.insert(j, '            value=default_vision_corto if "default_vision_corto" in locals() else "",\n')
                print("✅ Agregado value a vision_corto")
                break
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Campos estratégicos configurados para cargar desde demos")
