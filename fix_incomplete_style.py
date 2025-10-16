#!/usr/bin/env python3
"""
Arreglar definición incompleta de ParagraphStyle
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("🔍 Buscando definición incompleta...")

# Buscar alrededor de línea 60
if len(lines) > 65:
    # Las líneas 60-65 parecen ser parte de un ParagraphStyle sin inicio
    if "parent=styles" in lines[59] and "styles.add(ParagraphStyle" not in lines[58]:
        print("❌ Encontrada definición de estilo incompleta en líneas 60-65")
        
        # Verificar si hay un comentario que indica qué estilo es
        style_name = None
        if "# Estilo para" in lines[58]:
            # El comentario puede indicar el nombre
            style_name = "TituloPrincipal"
        
        # Arreglar agregando el inicio de la definición
        if style_name:
            # Insertar el inicio de la definición
            new_line = f"    styles.add(ParagraphStyle(name='{style_name}',\n"
            lines[59] = new_line + "    " + lines[59].lstrip()
            
            # Asegurar que termina con ))
            # Buscar dónde termina
            for i in range(60, min(70, len(lines))):
                if "fontName=" in lines[i]:
                    # Esta es probablemente la última línea
                    if not lines[i].rstrip().endswith('))'):
                        lines[i] = lines[i].rstrip() + '))\n'
                    break
            
            print(f"✅ Arreglada definición de estilo '{style_name}'")
        else:
            # Si no podemos determinar el nombre, eliminar las líneas problemáticas
            print("⚠️ No se puede determinar el nombre del estilo, eliminando líneas problemáticas")
            del lines[59:65]
    
    # Guardar cambios
    with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("✅ Archivo corregido")

