# Arreglar el string del botón
with open('app.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar el string mal formado
old_text = '''        generar_proyeccion_mckinsey = st.button(
            "📊 EJECUTAR PROYECCIÓN DCF\n" + 
            "ᵇᵃˢᵃᵈᵒ ᵉⁿ ᵐᵉ́ᵗᵒᵈᵒ ᴹᶜᴷⁱⁿˢᵉʸ",'''

new_text = '''        generar_proyeccion_mckinsey = st.button(
            "📊 EJECUTAR PROYECCIÓN DCF",'''

content = content.replace(old_text, new_text)

with open('app.py', 'w') as f:
    f.write(content)

print("Texto del botón simplificado - solo una línea")
