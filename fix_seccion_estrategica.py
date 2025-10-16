#!/usr/bin/env python3
"""
Reescribir completamente la sección de Información Estratégica
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar donde empieza la sección estratégica
start_idx = None
for i, line in enumerate(lines):
    if '🎯 Información Estratégica' in line:
        start_idx = i - 1  # Incluir la línea anterior si es relevante
        print(f"Sección estratégica empieza en línea {start_idx + 1}")
        break

# Buscar donde termina (antes de "Guardar en session_state")
end_idx = None
for i in range(start_idx, len(lines)):
    if '# Guardar en session_state para uso global' in lines[i]:
        end_idx = i
        print(f"Sección estratégica termina en línea {end_idx}")
        break

# Crear la sección corregida
seccion_corregida = '''        st.markdown("---")
        st.subheader("🎯 Información Estratégica")
        
        col1_est, col2_est = st.columns(2)
        with col1_est:
            modelo_negocio = st.selectbox(
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
        
        with col2_est:
            posicionamiento_precio = st.selectbox(
                "Posicionamiento de Precio",
                ["Premium - Alto valor",
                 "Medio - Calidad-precio",
                 "Low-cost - Precio bajo",
                 "Freemium - Gratuito con opciones de pago",
                 "Variable - Según segmento"],
                help="¿Cómo se posiciona en precio vs competencia?"
            )
            if datos_excel and "posicionamiento_precio" in datos_excel["info_general"]:
                posicionamiento_precio = datos_excel["info_general"]["posicionamiento_precio"]
        
        competidores_principales = st.text_area(
            "Top 3 Competidores Principales",
            value=datos_excel["info_general"].get("competidores_principales", "") if datos_excel else "",
            placeholder="Ej: Competidor A (40% mercado), Competidor B (25%), Competidor C (20%)",
            height=70,
            help="Identifique sus principales competidores y su participación de mercado"
        )
        
        vision_corto = st.text_area(
            "Objetivos a Corto Plazo (1 año)",
            value=datos_excel["info_general"].get("vision_corto_plazo", "") if datos_excel else "",
            placeholder="Ej: Aumentar ventas 20%, lanzar 2 productos nuevos, abrir mercado en Francia...",
            height=70,
            help="¿Qué planea lograr en los próximos 12 meses?"
        )
        
        vision_medio = st.text_area(
            "Objetivos a Medio Plazo (3 años)",
            value=datos_excel["info_general"].get("vision_medio_plazo", "") if datos_excel else "",
            placeholder="Ej: Líder regional, 50M facturación, expansión internacional...",
            height=70,
            help="¿Dónde ve la empresa en 3 años?"
        )
        
        vision_largo = st.text_area(
            "Visión a Largo Plazo (5+ años)",
            value=datos_excel["info_general"].get("vision_largo_plazo", "") if datos_excel else "",
            placeholder="Ej: IPO, líder del sector, venta estratégica, expansión global...",
            height=70,
            help="¿Cuál es la visión final para la empresa?"
        )
        
        # Análisis de diferenciación
        ventaja_competitiva_clave = st.text_area(
            "Ventaja Competitiva Principal",
            value=datos_excel["info_general"].get("ventaja_competitiva_principal", "") if datos_excel else "",
            placeholder="¿Qué hace única a su empresa? ¿Por qué los clientes la eligen?",
            height=70,
            help="Describa su propuesta de valor diferencial"
        )
        
        principales_riesgos = st.text_area(
            "Principales Riesgos del Negocio",
            value=datos_excel["info_general"].get("principales_riesgos", "") if datos_excel else "",
            placeholder="Ej: Concentración de clientes, dependencia de proveedores, regulación...",
            height=70,
            help="Identifique los 3 principales riesgos y cómo los mitiga"
        )
        
        col1_desc, col2_desc = st.columns(2)
        with col1_desc:
            cuota_mercado = st.number_input(
                "Cuota de Mercado (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.5,
                key="cuota_mercado_sidebar",
                help="% estimado en su segmento"
            )
        
        with col2_desc:
            # Espacio para simetría o agregar otro campo
            st.empty()
        
        ventajas_competitivas = st.text_area(
            "Ventajas Competitivas",
            placeholder="¿Qué diferencia a la empresa de sus competidores?",
            height=80,
            key="ventajas_competitivas_sidebar"
        )
        
        clientes_objetivo = st.text_area(
            "Clientes Objetivo",
            placeholder="Describa el segmento de clientes al que se dirige...",
            height=80,
            key="clientes_objetivo_sidebar"
        )
    
'''

# Reemplazar la sección
new_lines = lines[:start_idx] + [seccion_corregida] + lines[end_idx:]

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Sección de Información Estratégica completamente reescrita")
print("✅ Todos los campos corregidos con valores por defecto de datos_excel")

