#!/usr/bin/env python3
"""
Arreglar la pérdida de datos en el PDF cuando se incluye análisis IA
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde se llama a generar_pdf_mckinsey
found = False
for i in range(len(lines)):
    if "pdf_bytes = generar_pdf_mckinsey(" in lines[i]:
        print(f"Encontrada llamada a generar_pdf_mckinsey en línea {i+1}")
        
        # Buscar hacia atrás para encontrar la preparación de datos
        for j in range(max(0, i-50), i):
            if "'proyecciones'" in lines[j] or "'valoracion'" in lines[j]:
                print(f"Encontrada preparación de datos en línea {j+1}")
                break
        
        # Reemplazar la sección problemática
        # Buscar la línea específica con pd.DataFrame()
        for k in range(i-10, i+5):
            if "pd.DataFrame()" in lines[k]:
                print(f"Encontrado pd.DataFrame() vacío en línea {k+1}")
                
                # Cambiar para que use los datos reales si existen
                lines[k] = lines[k].replace(
                    "pd.DataFrame() if 'pyl_df' not in locals() else pyl_df",
                    "st.session_state.get('pyl_df', pd.DataFrame())"
                )
                lines[k] = lines[k].replace(
                    "pd.DataFrame() if 'balance_df' not in locals() else balance_df",
                    "st.session_state.get('balance_df', pd.DataFrame())"
                )
                lines[k] = lines[k].replace(
                    "pd.DataFrame() if 'fcf_df' not in locals() else fcf_df",
                    "st.session_state.get('fcf_df', pd.DataFrame())"
                )
        
        # Asegurar que los DataFrames se guarden en session_state cuando se generan
        # Buscar donde se generan las proyecciones
        for m in range(2000, min(4000, len(lines))):
            if "pyl_df = pd.DataFrame" in lines[m] and "st.session_state['pyl_df']" not in lines[m+1]:
                lines.insert(m+1, "            st.session_state['pyl_df'] = pyl_df\n")
                print(f"Agregado guardado de pyl_df en línea {m+2}")
            if "balance_df = pd.DataFrame" in lines[m] and "st.session_state['balance_df']" not in lines[m+1]:
                lines.insert(m+1, "            st.session_state['balance_df'] = balance_df\n")
                print(f"Agregado guardado de balance_df en línea {m+2}")
            if "fcf_df = pd.DataFrame" in lines[m] and "st.session_state['fcf_df']" not in lines[m+1]:
                lines.insert(m+1, "            st.session_state['fcf_df'] = fcf_df\n")
                print(f"Agregado guardado de fcf_df en línea {m+2}")
        
        found = True
        break

# Ahora buscar específicamente la sección donde se genera el PDF con análisis IA
for i in range(5000, min(6000, len(lines))):
    if "generar_pdf_mckinsey(" in lines[i]:
        print(f"Encontrada otra llamada a generar_pdf_mckinsey en línea {i+1}")
        
        # Verificar que esté pasando los DataFrames correctamente
        # Buscar las líneas alrededor
        start = max(0, i-20)
        end = min(len(lines), i+10)
        
        # Reemplazar la llamada para usar los datos de session_state
        for j in range(start, end):
            if "pyl_df=pd.DataFrame()" in lines[j]:
                lines[j] = "                            pyl_df=st.session_state.get('pyl_df', pd.DataFrame()),\n"
                print(f"Corregido pyl_df en línea {j+1}")
            if "balance_df=pd.DataFrame()" in lines[j]:
                lines[j] = "                            balance_df=st.session_state.get('balance_df', pd.DataFrame()),\n"
                print(f"Corregido balance_df en línea {j+1}")
            if "fcf_df=pd.DataFrame()" in lines[j]:
                lines[j] = "                            fcf_df=st.session_state.get('fcf_df', pd.DataFrame()),\n"
                print(f"Corregido fcf_df en línea {j+1}")

if found:
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("\n✅ Arreglado el problema de pérdida de datos en el PDF")
else:
    print("⚠️ No se encontró la sección a modificar")

