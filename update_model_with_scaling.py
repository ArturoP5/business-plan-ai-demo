# Actualizar el modelo para usar el parámetro de escalamiento
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# Primero, agregar el parámetro al __init__
old_init = "        self.gastos_marketing = params_operativos.get('gastos_marketing', 0)"
new_init = """        self.gastos_marketing = params_operativos.get('gastos_marketing', 0)
        self.porcentaje_gastos_variables = params_operativos.get('porcentaje_gastos_variables', 35)"""

content = content.replace(old_init, new_init)

# Ahora actualizar la lógica de escalamiento en el escenario base
old_scaling = """                else:
                    # Escenario base: fórmulas originales
                    gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)"""

new_scaling = """                else:
                    # Escenario base: usar el porcentaje configurado por el usuario
                    factor_variable = self.porcentaje_gastos_variables / 100
                    factor_fijo = 1 - factor_variable
                    
                    gastos_personal = self.gastos_personal * (factor_fijo * inflacion_acum + factor_variable * factor_actividad)
                    gastos_generales = self.gastos_generales * ((factor_fijo * 0.8) * inflacion_acum + (factor_variable * 0.8) * factor_actividad)"""

content = content.replace(old_scaling, new_scaling)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("Modelo actualizado para usar el parámetro de escalamiento dinámico")
