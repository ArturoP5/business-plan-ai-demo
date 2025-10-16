# Modificar el botón McKinsey para que sea rojo con texto en dos líneas
with open('app.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar el botón actual
old_button = """    with col_btn1:
        generar_proyeccion_mckinsey = st.button(
            "🏆 Proyección McKinsey", 
            type="secondary", 
            use_container_width=True,
            help="Valoración DCF pura con metodología McKinsey (NOPLAT, ROIC, Beta sectorial)"
        )"""

new_button = """    with col_btn1:
        # CSS personalizado para botón rojo
        st.markdown('''
            <style>
            div[data-testid="column"]:nth-of-type(1) button {
                background-color: #DC143C;
                color: white;
                font-weight: bold;
                border: none;
                padding: 0.5rem;
                line-height: 1.2;
            }
            div[data-testid="column"]:nth-of-type(1) button:hover {
                background-color: #B22222;
                border: none;
            }
            </style>
        ''', unsafe_allow_html=True)
        
        generar_proyeccion_mckinsey = st.button(
            "📊 EJECUTAR PROYECCIÓN DCF\n" + 
            "ᵇᵃˢᵃᵈᵒ ᵉⁿ ᵐᵉ́ᵗᵒᵈᵒ ᴹᶜᴷⁱⁿˢᵉʸ", 
            type="primary", 
            use_container_width=True,
            help="Valoración DCF pura con metodología McKinsey (NOPLAT, ROIC, Beta sectorial)"
        )"""

content = content.replace(old_button, new_button)

with open('app.py', 'w') as f:
    f.write(content)

print("Botón McKinsey actualizado a rojo con texto en dos líneas")
