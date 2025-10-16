# Ajustar el escalamiento de costos para empresas industriales
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar los porcentajes del escenario base
old_scaling = """                    # Escenario base: fórmulas originales
                    gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)"""

new_scaling = """                    # Escenario base: ajustado para empresas industriales
                    # Mayor proporción variable para reflejar mano de obra directa
                    gastos_personal = self.gastos_personal * (0.25 * inflacion_acum + 0.75 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.60 * inflacion_acum + 0.40 * factor_actividad)"""

content = content.replace(old_scaling, new_scaling)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("Modelo ajustado: ahora 75% de gastos de personal escalan con ventas (realista para industrial)")
