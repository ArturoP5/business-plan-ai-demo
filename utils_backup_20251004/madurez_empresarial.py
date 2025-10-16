"""
Módulo para calcular el factor de madurez empresarial
y ajustar las proyecciones según la fase de la empresa
"""

from datetime import datetime
from typing import Dict, List, Tuple

def calcular_factor_madurez(empresa_info: dict) -> dict:
    """
    Calcula un factor de ajuste basado en la madurez de la empresa
    Factor: 0.5 (muy madura) a 1.0 (startup)
    """
    # Extraer datos relevantes
    año_fundacion = empresa_info.get('año_fundacion', datetime.now().year - 5)
    años_operacion = datetime.now().year - año_fundacion
    
    # Obtener facturación del último año
    if 'ventas' in empresa_info and isinstance(empresa_info['ventas'], list):
        facturacion = empresa_info['ventas'][-1] if empresa_info['ventas'] else 10_000_000
    else:
        facturacion = empresa_info.get('ventas', 10_000_000)
    
    # Calcular crecimiento histórico
    if 'ventas' in empresa_info and isinstance(empresa_info['ventas'], list) and len(empresa_info['ventas']) >= 2:
        ventas = empresa_info['ventas']
        if ventas[0] > 0:
            crecimiento_historico = ((ventas[-1] / ventas[0]) ** (1 / (len(ventas) - 1)) - 1) * 100
        else:
            crecimiento_historico = 10
    else:
        crecimiento_historico = 10
    
    # Factor por años de operación
    if años_operacion < 3:
        factor_años = 1.0
    elif años_operacion < 10:
        factor_años = 0.9
    elif años_operacion < 25:
        factor_años = 0.75
    else:
        factor_años = 0.6
    
    # Factor por tamaño (facturación)
    if facturacion < 10_000_000:
        factor_tamaño = 1.0
    elif facturacion < 50_000_000:
        factor_tamaño = 0.85
    elif facturacion < 250_000_000:
        factor_tamaño = 0.7
    else:
        factor_tamaño = 0.5
    
    # Factor por crecimiento histórico
    if crecimiento_historico > 15:
        factor_crecimiento = 1.0
    elif crecimiento_historico > 5:
        factor_crecimiento = 0.85
    else:
        factor_crecimiento = 0.7
    
    # Calcular factor combinado
    factor_madurez = (factor_años + factor_tamaño + factor_crecimiento) / 3
    
    return {
        'factor': factor_madurez,
        'años_operacion': años_operacion,
        'facturacion': facturacion,
        'crecimiento_historico': round(crecimiento_historico, 1),
        'clasificacion': _clasificar_empresa(años_operacion, facturacion, crecimiento_historico)
    }

def _clasificar_empresa(años: int, facturacion: float, crecimiento: float) -> str:
    """Clasifica la empresa según su fase"""
    if años < 3:
        return "Startup"
    elif años < 10 and crecimiento > 15:
        return "Crecimiento rápido"
    elif años < 25 and facturacion < 50_000_000:
        return "En consolidación"
    elif años >= 25 or facturacion >= 250_000_000:
        return "Madura"
    else:
        return "Establecida"

def ajustar_proyecciones_por_madurez(tasas_originales: List[float], factor_madurez: dict) -> List[float]:
    """
    Ajusta las tasas de crecimiento según el factor de madurez
    """
    # Si es una empresa muy madura, aplicar ajuste más fuerte
    if factor_madurez['factor'] < 0.7:
        # Aplicar ajuste con sesgo hacia la baja para empresas maduras
        tasas_ajustadas = []
        for i, tasa in enumerate(tasas_originales):
            # Mayor ajuste en años posteriores (más incertidumbre)
            factor_año = 1 - (i * 0.05)  # -5% adicional por año
            tasa_ajustada = tasa * factor_madurez['factor'] * factor_año
            tasas_ajustadas.append(round(tasa_ajustada, 1))
    else:
        # Ajuste moderado para empresas en crecimiento
        tasas_ajustadas = [round(tasa * factor_madurez['factor'], 1) for tasa in tasas_originales]
    
    return tasas_ajustadas
