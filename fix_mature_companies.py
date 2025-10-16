# Actualizar la lógica de empresas maduras con estructura sectorial
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# Buscar la sección de empresas maduras
old_section = """                factor_eficiencia_personal = 1 + (factor_actividad - 1) * eficiencias['personal'] * ajuste_escenario
                gastos_personal = self.gastos_personal * factor_eficiencia_personal * inflacion_acum
                factor_eficiencia_general = 1 + (factor_actividad - 1) * eficiencias['general'] * ajuste_escenario
                gastos_generales = self.gastos_generales * factor_eficiencia_general * inflacion_acum"""

new_section = """                # Aplicar estructura de costos sectorial para empresas maduras
                if self.sector == "Industrial" or self.sector == "Automoción":
                    # 60% variable, 40% fijo para Industrial
                    gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                elif self.sector == "Tecnología":
                    # 20% variable, 80% fijo para Tecnología
                    gastos_personal = self.gastos_personal * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.75 * inflacion_acum + 0.25 * factor_actividad)
                else:
                    # Lógica original con factor_eficiencia para otros sectores
                    factor_eficiencia_personal = 1 + (factor_actividad - 1) * eficiencias['personal'] * ajuste_escenario
                    gastos_personal = self.gastos_personal * factor_eficiencia_personal * inflacion_acum
                    factor_eficiencia_general = 1 + (factor_actividad - 1) * eficiencias['general'] * ajuste_escenario
                    gastos_generales = self.gastos_generales * factor_eficiencia_general * inflacion_acum"""

content = content.replace(old_section, new_section)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("✅ Lógica de empresas maduras actualizada con estructura sectorial")
