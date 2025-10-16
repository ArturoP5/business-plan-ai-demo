# Ajustar el escalamiento para que sea más realista para Industrial
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# Actualizar solo el escenario base para ser más realista
old_scaling = """                else:
                    # Escenario base: fórmulas originales
                    gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)"""

new_scaling = """                else:
                    # Escenario base: ajustado para mejor reflejar economías de escala
                    # Para empresas industriales, más gastos son variables (mano de obra directa)
                    if self.sector == "Industrial":
                        # Industrial: mayor componente variable (50% personal, 35% generales)
                        gastos_personal = self.gastos_personal * (0.50 * inflacion_acum + 0.50 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    else:
                        # Otros sectores: fórmulas originales
                        gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)"""

content = content.replace(old_scaling, new_scaling)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("Modelo ajustado: Industrial ahora tiene 50% de gastos variables (más realista)")
