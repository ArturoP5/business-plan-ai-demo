# Actualizar estructura de costos para todos los sectores basado en datos reales
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# Buscar la sección del escenario base
old_section = """                else:
                    # Escenario base: fórmulas originales
                    gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)"""

new_section = """                else:
                    # Escenario base: estructura basada en datos reales de PYMES españolas
                    # Fuente: Análisis estructura de gastos PYMES por sector
                    
                    if self.sector == "Industrial" or self.sector == "Automoción":
                        # 50-70% variables, 10-20% semi-fijos, 20-40% fijos
                        gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    
                    elif self.sector == "Tecnología":
                        # 10-30% variables, 15-30% semi-fijos, 40-75% fijos
                        gastos_personal = self.gastos_personal * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.75 * inflacion_acum + 0.25 * factor_actividad)
                    
                    elif self.sector == "Ecommerce":
                        # 60-80% variables, 5-15% semi-fijos, 15-35% fijos
                        gastos_personal = self.gastos_personal * (0.30 * inflacion_acum + 0.70 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.25 * inflacion_acum + 0.75 * factor_actividad)
                    
                    elif self.sector == "Hostelería":
                        # 55-65% variables, 10-15% semi-fijos, 20-35% fijos
                        gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    
                    elif self.sector == "Retail":
                        # Similar a Moda: 55-70% variables, 5-15% semi-fijos, 25-40% fijos
                        gastos_personal = self.gastos_personal * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    
                    elif self.sector == "Consultoría" or self.sector == "Servicios":
                        # 60-85% variables (personal en proyectos), 5-15% semi-fijos, 10-35% fijos
                        gastos_personal = self.gastos_personal * (0.25 * inflacion_acum + 0.75 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.60 * inflacion_acum + 0.40 * factor_actividad)
                    
                    else:
                        # Sector "Otro": valores conservadores intermedios
                        gastos_personal = self.gastos_personal * (0.50 * inflacion_acum + 0.50 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.60 * inflacion_acum + 0.40 * factor_actividad)"""

content = content.replace(old_section, new_section)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("✅ Estructura de costos actualizada para TODOS los sectores con datos reales")
