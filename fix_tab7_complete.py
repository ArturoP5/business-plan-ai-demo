#!/usr/bin/env python3
"""
Reescribir completamente la sección de generación de PDF en tab7
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde empieza tab7
tab7_start = -1
for i, line in enumerate(lines):
    if "with tab7:" in line:
        tab7_start = i
        print(f"Encontrado tab7 en línea {i+1}")
        break

if tab7_start > 0:
    # Buscar donde empieza el try problemático (alrededor de línea 5331)
    for i in range(tab7_start, min(tab7_start + 100, len(lines))):
        if "try:" in lines[i] and i > 5320 and i < 5340:
            print(f"Encontrado try en línea {i+1}")
            
            # Buscar el except correspondiente
            except_line = -1
            for j in range(i+1, min(i+100, len(lines))):
                if "except" in lines[j] and len(lines[j]) - len(lines[j].lstrip()) == len(lines[i]) - len(lines[i].lstrip()):
                    except_line = j
                    print(f"Encontrado except en línea {j+1}")
                    break
            
            if except_line > 0:
                # Reemplazar todo el bloque try-except
                indent = " " * (len(lines[i]) - len(lines[i].lstrip()))
                
                new_block = f'''{indent}try:
{indent}    # Recopilar análisis IA si existe
{indent}    ai_analysis = {{}}
{indent}    if 'ai_swot' in st.session_state:
{indent}        ai_analysis['swot'] = st.session_state['ai_swot']
{indent}    if 'ai_financial_analysis' in st.session_state:
{indent}        ai_analysis['analisis_financiero'] = st.session_state['ai_financial_analysis']
{indent}    if 'ai_investment_thesis' in st.session_state:
{indent}        ai_analysis['investment_thesis'] = st.session_state['ai_investment_thesis']
{indent}    
{indent}    # Importar el generador de PDF
{indent}    from utils.pdf_mckinsey_generator import generar_pdf_mckinsey
{indent}    
{indent}    # Preparar datos para el PDF
{indent}    datos = {{
{indent}        'datos_empresa': {{
{indent}            'nombre': nombre_empresa,
{indent}            'sector': sector,
{indent}            'año_fundacion': año_fundacion,
{indent}            'empleados': num_empleados,
{indent}            'descripcion': descripcion_actividad if 'descripcion_actividad' in locals() else ''
{indent}        }},
{indent}        'proyecciones': st.session_state.get('proyecciones', {{}}),
{indent}        'valoracion': st.session_state.get('valoracion_dcf', {{}})
{indent}    }}
{indent}    
{indent}    # Generar el PDF
{indent}    pdf_bytes = generar_pdf_mckinsey(
{indent}        datos_empresa=datos['datos_empresa'],
{indent}        resultado_mckinsey=datos['valoracion'],
{indent}        pyl_df=pd.DataFrame() if 'pyl_df' not in locals() else pyl_df,
{indent}        balance_df=pd.DataFrame() if 'balance_df' not in locals() else balance_df,
{indent}        fcf_df=pd.DataFrame() if 'fcf_df' not in locals() else fcf_df,
{indent}        analisis_ia=ai_analysis,
{indent}        metricas={{}}
{indent}    )
{indent}    
{indent}    # Botón de descarga
{indent}    st.download_button(
{indent}        label="📥 Descargar PDF de Valoración",
{indent}        data=pdf_bytes,
{indent}        file_name=f"Valoracion_DCF_{{datos['datos_empresa']['nombre'].replace(' ', '_')}}_{{datetime.now().strftime('%Y%m%d')}}.pdf",
{indent}        mime="application/pdf",
{indent}        help="Descarga el informe completo de valoración en PDF"
{indent}    )
{indent}    
{indent}    st.success("✅ PDF generado exitosamente")
'''
                
                # Eliminar el bloque viejo y poner el nuevo
                del lines[i:except_line]
                lines.insert(i, new_block)
                
                print("✅ Bloque try-except reescrito completamente")
                break
            break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Sección de generación de PDF en tab7 completamente arreglada")

