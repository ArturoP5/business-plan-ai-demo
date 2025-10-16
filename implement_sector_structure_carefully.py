# Implementar estructura de costos sectorial con mucho cuidado
with open('models/modelo_financiero.py', 'r') as f:
    content = f.read()

# CAMBIO 1: Para empresas maduras - reemplazar factor_eficiencia con lógica sectorial
old_mature = """                factor_eficiencia_personal = 1 + (factor_actividad - 1) * eficiencias['personal'] * ajuste_escenario
                gastos_personal = self.gastos_personal * factor_eficiencia_personal * inflacion_acum
                factor_eficiencia_general = 1 + (factor_actividad - 1) * eficiencias['general'] * ajuste_escenario
                gastos_generales = self.gastos_generales * factor_eficiencia_general * inflacion_acum
                factor_eficiencia_marketing = 1 + (factor_actividad - 1) * eficiencias['marketing'] * ajuste_escenario
                gastos_marketing = self.gastos_marketing * factor_eficiencia_marketing * inflacion_acum"""

new_mature = """                # Aplicar estructura sectorial para empresas maduras
                if self.sector == "Industrial" or self.sector == "Automoción":
                    # 50-70% variables (media: 60%)
                    gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                elif self.sector == "Tecnología":
                    # 10-30% variables (media: 20%)
                    gastos_personal = self.gastos_personal * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.75 * inflacion_acum + 0.25 * factor_actividad)
                elif self.sector == "Ecommerce":
                    # 60-80% variables (media: 70%)
                    gastos_personal = self.gastos_personal * (0.30 * inflacion_acum + 0.70 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.25 * inflacion_acum + 0.75 * factor_actividad)
                elif self.sector == "Hostelería":
                    # 55-65% variables (media: 60%)
                    gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                elif self.sector == "Retail":
                    # 55-70% variables (media: 62%)
                    gastos_personal = self.gastos_personal * (0.38 * inflacion_acum + 0.62 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                elif self.sector == "Consultoría" or self.sector == "Servicios":
                    # 60-85% variables (media: 72%)
                    gastos_personal = self.gastos_personal * (0.28 * inflacion_acum + 0.72 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.60 * inflacion_acum + 0.40 * factor_actividad)
                else:
                    # Sector "Otro": usar factor_eficiencia original
                    factor_eficiencia_personal = 1 + (factor_actividad - 1) * eficiencias['personal'] * ajuste_escenario
                    gastos_personal = self.gastos_personal * factor_eficiencia_personal * inflacion_acum
                    factor_eficiencia_general = 1 + (factor_actividad - 1) * eficiencias['general'] * ajuste_escenario
                    gastos_generales = self.gastos_generales * factor_eficiencia_general * inflacion_acum
                
                # Marketing siempre es más variable
                factor_eficiencia_marketing = 1 + (factor_actividad - 1) * eficiencias['marketing'] * ajuste_escenario
                gastos_marketing = self.gastos_marketing * factor_eficiencia_marketing * inflacion_acum"""

content = content.replace(old_mature, new_mature)

# CAMBIO 2: Para empresas jóvenes en escenario base - aplicar misma lógica sectorial
old_young = """                else:
                    # Escenario base: fórmulas originales
                    gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                    gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                    gastos_marketing = self.gastos_marketing * (0.40 * inflacion_acum + 0.60 * factor_actividad)"""

new_young = """                else:
                    # Escenario base: aplicar estructura sectorial también a empresas jóvenes
                    if self.sector == "Industrial" or self.sector == "Automoción":
                        gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    elif self.sector == "Tecnología":
                        gastos_personal = self.gastos_personal * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.75 * inflacion_acum + 0.25 * factor_actividad)
                    elif self.sector == "Ecommerce":
                        gastos_personal = self.gastos_personal * (0.30 * inflacion_acum + 0.70 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.25 * inflacion_acum + 0.75 * factor_actividad)
                    elif self.sector == "Hostelería":
                        gastos_personal = self.gastos_personal * (0.40 * inflacion_acum + 0.60 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    elif self.sector == "Retail":
                        gastos_personal = self.gastos_personal * (0.38 * inflacion_acum + 0.62 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.35 * inflacion_acum + 0.65 * factor_actividad)
                    elif self.sector == "Consultoría" or self.sector == "Servicios":
                        gastos_personal = self.gastos_personal * (0.28 * inflacion_acum + 0.72 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.60 * inflacion_acum + 0.40 * factor_actividad)
                    else:
                        # Sector "Otro": valores conservadores
                        gastos_personal = self.gastos_personal * (0.65 * inflacion_acum + 0.35 * factor_actividad)
                        gastos_generales = self.gastos_generales * (0.80 * inflacion_acum + 0.20 * factor_actividad)
                    
                    # Marketing más variable
                    gastos_marketing = self.gastos_marketing * (0.40 * inflacion_acum + 0.60 * factor_actividad)"""

content = content.replace(old_young, new_young)

with open('models/modelo_financiero.py', 'w') as f:
    f.write(content)

print("✅ Estructura sectorial implementada cuidadosamente para todos los sectores")
