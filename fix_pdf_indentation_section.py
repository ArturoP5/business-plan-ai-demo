#!/usr/bin/env python3
"""
Arreglar la indentación de toda la sección problemática
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Arreglando líneas 1654-1670...")

# Arreglar cada línea con la indentación correcta
corrections = {
    1653: "    pdf.add_page()",  # 4 espacios
    1654: "    # Título de la sección",  # 4 espacios
    1655: "    pdf.set_font(\"Arial\", \"B\", 16)",  # 4 espacios
    1656: "    pdf.cell(0, 10, \"ANÁLISIS ESTRATÉGICO CON INTELIGENCIA ARTIFICIAL\", 0, 1, 'C')",  # 4 espacios
    1657: "    pdf.ln(5)",  # 4 espacios
    1658: "    # SWOT Enriquecido con IA",  # 4 espacios
    1659: "    if 'swot' in ai_analysis:",  # 4 espacios
    1660: "        self._add_enhanced_swot(pdf, ai_analysis['swot'])",  # 8 espacios (dentro del if)
    1661: "    ",  # línea vacía con indentación
    1662: "    # Análisis Financiero IA",  # 4 espacios
    1663: "    if 'analisis_financiero' in ai_analysis:",  # 4 espacios
    1664: "        pdf.add_page()",  # 8 espacios
    1665: "        self._add_financial_analysis_ia(pdf, ai_analysis['analisis_financiero'])",  # 8 espacios
    1666: "    ",  # línea vacía
    1667: "    # Investment Thesis IA",  # 4 espacios
    1668: "    if 'investment_thesis' in ai_analysis:",  # 4 espacios
    1669: "        self._add_investment_thesis_ia(pdf, ai_analysis['investment_thesis'])",  # 8 espacios
}

for line_num, correct_content in corrections.items():
    if line_num < len(lines):
        lines[line_num] = correct_content + "\n"
        print(f"Corregida línea {line_num + 1}")

# Guardar
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Indentación arreglada completamente")

