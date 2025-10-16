"""
Parámetros para proyección de balance - Método McKinsey
Basados en benchmarks de mercado reales
"""

# Política de dividendos por fase empresarial
POLITICA_DIVIDENDOS = {
    'crecimiento': 0.0,      # 0% payout
    'transicion': 0.25,      # 25% payout
    'madura': 0.50           # 50% payout
}

# Límites de endeudamiento por sector (Deuda Neta / EBITDA)
LIMITES_DEUDA_SECTOR = {
    'Industrial': 3.0,       # Hasta 3.0x EBITDA
    'Tecnología': 2.0,       # Hasta 2.0x EBITDA (más conservador)
    'Retail': 2.5,           # Hasta 2.5x EBITDA
    'Hostelería': 3.5,       # Hasta 3.5x EBITDA
    'Ecommerce': 2.5,        # Similar a Retail
    'Servicios': 2.0,        # Conservador
    'Consultoría': 1.5,      # Muy bajo (poco intensivo en capital)
    'Automoción': 3.0,       # Similar a Industrial
    'Otro': 2.5              # Promedio general
}

# WACC objetivo por sector (%)
WACC_OBJETIVO_SECTOR = {
    'Industrial': 9.0,       # 8-10% rango típico
    'Tecnología': 11.0,      # 10-12% por mayor riesgo
    'Retail': 10.0,          # 9-11% rango
    'Hostelería': 10.0,      # 9-11% rango
    'Ecommerce': 11.0,       # Similar a tech
    'Servicios': 9.0,        # Estable
    'Consultoría': 10.0,     # Medio
    'Automoción': 9.5,       # Similar a Industrial
    'Otro': 10.0             # Promedio
}

# Covenants bancarios típicos
COVENANTS_TIPICOS = {
    'cobertura_intereses_min': 3.0,     # EBITDA / Gastos financieros >= 3.0x
    'deuda_neta_ebitda_max': 4.0,       # Deuda Neta / EBITDA <= 4.0x
    'current_ratio_min': 1.2             # Activo Corriente / Pasivo Corriente >= 1.2
}

# Rating crediticio por nivel de apalancamiento
def obtener_rating_objetivo(deuda_ebitda):
    """Determina el rating crediticio según el ratio Deuda/EBITDA"""
    if deuda_ebitda < 1.5:
        return 'A'
    elif deuda_ebitda < 2.5:
        return 'BBB'
    elif deuda_ebitda < 3.5:
        return 'BB'
    elif deuda_ebitda < 4.5:
        return 'B'
    else:
        return 'CCC'

# Función para determinar la fase empresarial
def determinar_fase_empresa(años_operacion, crecimiento_historico):
    """Determina si la empresa está en crecimiento, transición o madura"""
    if años_operacion < 5 or crecimiento_historico > 20:
        return 'crecimiento'
    elif años_operacion < 15 or crecimiento_historico > 10:
        return 'transicion'
    else:
        return 'madura'

# Inversión en intangibles como % de ingresos por sector
INVERSION_INTANGIBLES_SECTOR = {
    'Tecnología': 3.0,       # Alta inversión en I+D y software
    'Industrial': 0.5,       # Patentes y procesos
    'Retail': 1.0,          # Sistemas y marca
    'Hostelería': 0.3,      # Marca local
    'Ecommerce': 2.0,       # Plataforma y tecnología
    'Servicios': 0.8,       # Sistemas y procesos
    'Consultoría': 2.0,     # Metodologías y conocimiento
    'Automoción': 1.0,      # I+D y procesos
    'Otro': 0.8             # Promedio general
}

# Amortización anual de intangibles
AMORTIZACION_INTANGIBLES_ANUAL = 0.10  # 10% anual (vida útil 10 años)

# Inversiones CP como % de tesorería
INVERSIONES_CP_PCT_TESORERIA = 0.10  # 10% de tesorería en inversiones temporales

# Gastos anticipados como % de gastos operativos
GASTOS_ANTICIPADOS_PCT_GASTOS = 0.02  # 2% de gastos operativos

# Política de tesorería por fase empresarial
TESORERIA_OBJETIVO_MULTIPLE = {
    'crecimiento': 1.2,    # Mínimo colchón, prioridad crecimiento
    'transicion': 1.5,     # Balance entre liquidez y crecimiento
    'madura': 2.0          # Mayor colchón, excesos a inversiones
}

# Política de distribución de excesos de tesorería
def calcular_inversion_lp_adicional(exceso_tesoreria, ingresos, fase_empresa):
    """
    Determina cuánto del exceso de tesorería debe ir a inversiones LP
    Basado en mejores prácticas de gestión financiera
    """
    if exceso_tesoreria <= 0:
        return 0
    
    # Como % de ingresos
    exceso_pct = exceso_tesoreria / ingresos
    
    if fase_empresa == 'crecimiento':
        # Empresas en crecimiento mantienen más liquidez
        if exceso_pct < 0.03:  # Menos del 3%
            return 0
        elif exceso_pct < 0.08:  # 3-8%
            return exceso_tesoreria * 0.3  # 30% a LP
        else:  # Más del 8%
            return exceso_tesoreria * 0.5  # 50% a LP
            
    elif fase_empresa == 'transicion':
        if exceso_pct < 0.05:  # Menos del 5%
            return 0
        elif exceso_pct < 0.10:  # 5-10%
            return exceso_tesoreria * 0.5  # 50% a LP
        else:  # Más del 10%
            return exceso_tesoreria * 0.7  # 70% a LP
            
    else:  # madura
        if exceso_pct < 0.05:  # Menos del 5%
            return exceso_tesoreria * 0.3  # 30% a LP
        elif exceso_pct < 0.10:  # 5-10%
            return exceso_tesoreria * 0.6  # 60% a LP
        else:  # Más del 10%
            return exceso_tesoreria * 0.8  # 80% a LP
    
    return 0
