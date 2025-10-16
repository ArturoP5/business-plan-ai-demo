#!/usr/bin/env python3
"""
AI Prompts Especializados para Informe de Valoración
Cada función genera un prompt optimizado para análisis profundo
"""

from typing import Dict, Any

def generar_prompt_executive_summary(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para Executive Summary con Investment Thesis
    """
    info = datos['info_basica']
    metricas = datos['metricas_valoracion']
    kpis = datos['kpis_financieros']
    desc = datos['descripcion_negocio']
    info_empresa = datos.get('info_empresa', {})
    vision = datos.get('vision_estrategica', {})
    
    prompt = f"""
Eres un analista financiero senior de banca de inversión. Genera un EXECUTIVE SUMMARY profesional y conciso para el siguiente caso:

EMPRESA: {info['nombre_empresa']}
SECTOR: {info['sector']}
ESCENARIO: {info['escenario_seleccionado']}

MÉTRICAS CLAVE:
- Enterprise Value: €{metricas['enterprise_value']:,.0f}
- Equity Value: €{metricas['equity_value']:,.0f}
- WACC: {metricas['wacc']:.1f}%
- TIR: {metricas['tir']:.1f}%
- ROIC Promedio: {metricas['roic_promedio']:.1f}%
- Deuda Neta: €{metricas['deuda_neta']:,.0f}
- CAGR Ventas: {kpis['cagr_ventas']:.1f}%
- Margen EBITDA: {kpis['margen_ebitda_year1']:.1f}% → {kpis['margen_ebitda_year5']:.1f}%

DESCRIPCIÓN DEL NEGOCIO:
{desc.get('descripcion_actividad', 'N/A')}

PRODUCTOS/SERVICIOS: {desc.get('productos_servicios', 'N/A')}

MODELO DE NEGOCIO: {desc.get('modelo_negocio', 'N/A')}

POSICIONAMIENTO DE PRECIO: {desc.get('posicionamiento_precio', 'N/A')}

COMPETIDORES PRINCIPALES: {desc.get('competidores_principales', 'N/A')}

VENTAJA COMPETITIVA: {desc.get('ventaja_competitiva_principal', 'N/A')}

CLIENTES OBJETIVO: {desc.get('clientes_objetivo', 'N/A')}

CUOTA DE MERCADO: {desc.get('cuota_mercado', 'N/A')}%

OBJETIVOS CORTO PLAZO (1 año): {vision.get('corto_plazo', 'N/A')}

OBJETIVOS MEDIO PLAZO (3 años): {vision.get('medio_plazo', 'N/A')}

VISIÓN LARGO PLAZO (5+ años): {vision.get('largo_plazo', 'N/A')}

PRINCIPALES RIESGOS: {desc.get('principales_riesgos', 'N/A')}

INSTRUCCIONES:
1. Redacta un Investment Thesis de 2-3 párrafos que:
   - Explique la propuesta de valor única de la empresa
   - Analice si la TIR vs WACC indica creación de valor (CRÍTICO: si TIR < WACC, el proyecto NO es viable)
   - Evalúe el ROIC vs WACC (si ROIC > WACC, hay eficiencia operativa)
   - Destaque los principales drivers de crecimiento
   - Identifique los riesgos materiales

2. Proporciona una RECOMENDACIÓN FINAL clara:
   - Si TIR >= WACC: "PROCEDER" o "REVISAR" (según el margen)
   - Si TIR < WACC pero ROIC > WACC: "REVISAR - Paradoja ROIC vs TIR" (eficiencia operativa pero falta escala)
   - Si TIR < WACC y ROIC < WACC: "NO PROCEDER"

3. Usa un tono profesional tipo McKinsey/Goldman Sachs

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "investment_thesis": "texto de 2-3 párrafos",
    "recomendacion": "PROCEDER/REVISAR/NO PROCEDER",
    "rating": "BUY/HOLD/SELL",
    "sintesis_una_linea": "resumen de una línea"
}}
"""
    return prompt


def generar_prompt_macro_sectorial(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para análisis macroeconómico y sectorial con perspectivas
    """
    info = datos['info_basica']
    desc = datos['descripcion_negocio']
    
    prompt = f"""
Eres un analista estratégico especializado en análisis sectorial. Genera un análisis MACROECONÓMICO Y SECTORIAL profundo.

EMPRESA: {info['nombre_empresa']}
SECTOR: {info['sector']}
DESCRIPCIÓN: {desc['descripcion_actividad']}
COMPETIDORES: {desc['competidores_principales']}

FECHA DEL ANÁLISIS: {info['fecha_informe']}

INSTRUCCIONES:
Genera un análisis completo dividido en dos partes:

1. CONTEXTO MACROECONÓMICO (2-3 párrafos):
   - Situación económica actual en España/Europa (PIB, inflación, tipos de interés)
   - Tendencias macroeconómicas relevantes para el sector {info['sector']}
   - Perspectivas a 12-24 meses
   - Impacto esperado en el negocio

2. ANÁLISIS SECTORIAL PROFUNDO (3-4 párrafos):
   - Tamaño del mercado de {info['sector']} en España/Europa
   - Tasa de crecimiento sectorial esperada (CAGR próximos 3-5 años)
   - Principales tendencias y disrupciones del sector
   - Dinámica competitiva (concentración, barreras de entrada)
   - Factores críticos de éxito en el sector
   - Perspectivas del sector: ¿crecimiento, madurez o declive?
   - Posicionamiento de {info['nombre_empresa']} vs competidores clave

Usa datos reales y estimaciones razonables basadas en tu conocimiento hasta 2025.

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "contexto_macro": "texto de 2-3 párrafos",
    "analisis_sectorial": "texto de 3-4 párrafos",
    "tamano_mercado_estimado": "valor estimado en €",
    "cagr_sectorial": "porcentaje estimado",
    "perspectiva_sector": "crecimiento/madurez/declive",
    "posicionamiento_vs_sector": "análisis comparativo"
}}
"""
    return prompt


def generar_prompt_swot(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para análisis SWOT profundo y específico
    """
    info = datos['info_basica']
    desc = datos['descripcion_negocio']
    metricas = datos['metricas_valoracion']
    kpis = datos['kpis_financieros']
    vision = datos['vision_estrategica']
    
    prompt = f"""
Eres un consultor estratégico de BCG/Bain. Genera un análisis SWOT profundo y específico.

EMPRESA: {info['nombre_empresa']}
SECTOR: {info['sector']}
MODELO DE NEGOCIO: {desc['modelo_negocio']}
VENTAJA COMPETITIVA: {desc['ventaja_competitiva_clave']}
COMPETIDORES: {desc['competidores_principales']}

MÉTRICAS FINANCIERAS:
- ROIC: {metricas['roic_promedio']:.1f}%
- WACC: {metricas['wacc']:.1f}%
- TIR: {metricas['tir']:.1f}%
- CAGR Ventas: {kpis['cagr_ventas']:.1f}%
- Margen EBITDA: {kpis['margen_ebitda_year1']:.1f}% → {kpis['margen_ebitda_year5']:.1f}%
- Deuda Neta/EBITDA: {kpis['deuda_neta_ebitda']:.1f}x

VISIÓN ESTRATÉGICA:
- Corto plazo: {vision['corto_plazo']}
- Medio plazo: {vision['medio_plazo']}
- Largo plazo: {vision['largo_plazo']}

INSTRUCCIONES:
Genera un análisis SWOT donde CADA punto sea:
- ESPECÍFICO a esta empresa (no genérico)
- CUANTIFICADO cuando sea posible
- ACCIONABLE

Para cada cuadrante, proporciona 4-5 puntos detallados:

FORTALEZAS: Analiza ventajas competitivas reales, capacidades únicas, métricas superiores
DEBILIDADES: Identifica limitaciones, gaps vs competidores, riesgos operativos
OPORTUNIDADES: Tendencias de mercado, expansión, innovación, partnerships
AMENAZAS: Competencia, regulación, tecnología, macro

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "fortalezas": ["punto 1", "punto 2", "punto 3", "punto 4"],
    "debilidades": ["punto 1", "punto 2", "punto 3", "punto 4"],
    "oportunidades": ["punto 1", "punto 2", "punto 3", "punto 4"],
    "amenazas": ["punto 1", "punto 2", "punto 3", "punto 4"],
    "sintesis_estrategica": "párrafo integrando los 4 cuadrantes"
}}
"""
    return prompt


def generar_prompt_kpis_detalle(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para análisis detallado de KPIs con explicaciones y recomendaciones
    """
    info = datos['info_basica']
    kpis = datos['kpis_financieros']
    estructura = datos['estructura_costes']
    
    prompt = f"""
Eres un CFO experimentado. Analiza los siguientes KPIs financieros de {info['nombre_empresa']} (sector {info['sector']}).

KPIs ACTUALES:

RENTABILIDAD:
- ROIC: {float(kpis['roic']):.1f}%
- ROE: {float(kpis['roe']):.1f}%
- Margen EBITDA: {float(kpis['margen_ebitda_year1']):.1f}% (Año 1) → {float(kpis['margen_ebitda_year5']):.1f}% (Año 5)
- Margen Neto: {float(kpis['margen_neto_year1']):.1f}% (Año 1) → {float(kpis['margen_neto_year5']):.1f}% (Año 5)

EFICIENCIA:
- Rotación de Activos: {float(kpis['rotacion_activos']):.2f}x
- Días de Cobro (DSO): {float(kpis['dias_cobro']):.0f} días
- Días de Pago (DPO): {float(kpis['dias_pago']):.0f} días
- Días de Inventario: {float(kpis['dias_inventario']):.0f} días
- Cash Conversion Cycle: {float(kpis['cash_conversion_cycle']):.0f} días

SOLVENCIA:
- Deuda Neta / EBITDA: {float(kpis['deuda_neta_ebitda']):.1f}x
- Cobertura de Intereses: {float(kpis['cobertura_intereses']):.1f}x
- Ratio de Liquidez: {float(kpis['ratio_liquidez']):.2f}

CRECIMIENTO:
- CAGR Ventas: {float(kpis['cagr_ventas']):.1f}%
- CAGR EBITDA: {float(kpis['cagr_ebitda']):.1f}%

ESTRUCTURA DE COSTES:
- Costes Fijos: {estructura['porcentaje_costes_fijos']}%
- Costes Variables: {estructura['porcentaje_costes_variables']}%

INSTRUCCIONES:
Para CADA KPI importante, proporciona:
1. ¿Qué significa este valor para {info['nombre_empresa']}? (contexto)
2. ¿Es bueno, malo o neutro vs benchmark del sector {info['sector']}?
3. ¿Cómo puede la empresa mejorar este KPI? (2-3 acciones concretas)

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "roic": {{
        "interpretacion": "texto explicando qué significa",
        "benchmark": "comparación vs sector",
        "como_mejorar": ["acción 1", "acción 2", "acción 3"]
    }},
    "margen_ebitda": {{ ... }},
    "cash_conversion_cycle": {{ ... }},
    "deuda_neta_ebitda": {{ ... }},
    "cagr_ventas": {{ ... }},
    "sintesis_financiera": "párrafo resumen de la salud financiera"
}}

Analiza al menos 5 KPIs clave.
"""
    return prompt


def generar_prompt_riesgos(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para análisis de riesgos con probabilidad, impacto y mitigación
    """
    info = datos['info_basica']
    desc = datos['descripcion_negocio']
    vision = datos['vision_estrategica']
    metricas = datos['metricas_valoracion']
    
    prompt = f"""
Eres un especialista en gestión de riesgos corporativos. Identifica y analiza los riesgos materiales para {info['nombre_empresa']}.

CONTEXTO:
Empresa: {info['nombre_empresa']}
Sector: {info['sector']}
Modelo de negocio: {desc['modelo_negocio']}
Competidores: {desc['competidores_principales']}
TIR vs WACC: {metricas['tir']:.1f}% vs {metricas['wacc']:.1f}%

RIESGOS IDENTIFICADOS POR LA EMPRESA:
{vision['principales_riesgos']}

INSTRUCCIONES:
Identifica 5-7 riesgos materiales. Para cada uno proporciona:

1. **Descripción del riesgo**: Específico y claro
2. **Probabilidad**: Alta / Media / Baja
3. **Impacto potencial**: Alto / Medio / Bajo (cuantifica en € o % si es posible)
4. **Estrategias de mitigación**: 2-3 acciones concretas
5. **Indicadores de alerta temprana**: KPIs o señales para monitorear

Categorías de riesgos a considerar:
- Competitivos (nuevos entrantes, sustitutos)
- Operativos (ejecución, talento, procesos)
- Financieros (liquidez, apalancamiento, FX)
- Regulatorios (normativa, cumplimiento)
- Tecnológicos (obsolescencia, ciberseguridad)
- De mercado (demanda, pricing power)

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "riesgos": [
        {{
            "nombre": "nombre corto del riesgo",
            "descripcion": "descripción detallada",
            "probabilidad": "Alta/Media/Baja",
            "impacto": "Alto/Medio/Bajo",
            "impacto_cuantificado": "estimación si es posible",
            "mitigacion": ["acción 1", "acción 2", "acción 3"],
            "indicadores_alerta": ["KPI 1", "KPI 2"]
        }}
    ],
    "riesgo_principal": "el riesgo más crítico identificado",
    "nivel_riesgo_global": "Alto/Medio/Bajo"
}}
"""
    return prompt


def generar_prompt_recomendaciones(datos: Dict[str, Any]) -> str:
    """
    Genera prompt para recomendaciones estratégicas accionables y priorizadas
    """
    info = datos['info_basica']
    desc = datos['descripcion_negocio']
    metricas = datos['metricas_valoracion']
    kpis = datos['kpis_financieros']
    vision = datos['vision_estrategica']
    
    prompt = f"""
Eres un consultor estratégico senior. Proporciona recomendaciones ACCIONABLES para crear valor en {info['nombre_empresa']}.

CONTEXTO COMPLETO:
Empresa: {info['nombre_empresa']}
Sector: {info['sector']}
Modelo: {desc['modelo_negocio']}
Ventaja competitiva: {desc['ventaja_competitiva_clave']}

MÉTRICAS:
- TIR: {metricas['tir']:.1f}% vs WACC: {metricas['wacc']:.1f}%
- ROIC: {metricas['roic_promedio']:.1f}%
- CAGR Ventas: {kpis['cagr_ventas']:.1f}%
- Margen EBITDA evolución: {kpis['margen_ebitda_year1']:.1f}% → {kpis['margen_ebitda_year5']:.1f}%

VISIÓN DE LA EMPRESA:
- Corto plazo: {vision['corto_plazo']}
- Medio plazo: {vision['medio_plazo']}
- Largo plazo: {vision['largo_plazo']}

INSTRUCCIONES:
Genera recomendaciones estratégicas en 3 horizontes temporales:

1. QUICK WINS (0-6 meses):
   - 3-5 iniciativas de rápida implementación
   - Alto impacto, baja complejidad
   - Mejoras operativas inmediatas

2. MEDIO PLAZO (6-24 meses):
   - 4-6 iniciativas estratégicas
   - Requieren inversión o transformación
   - Palancas de crecimiento

3. LARGO PLAZO (2-5 años):
   - 2-3 movimientos transformacionales
   - Cambios de modelo, M&A, nuevos mercados
   - Visión aspiracional

Para cada recomendación incluye:
- Descripción clara
- Impacto esperado (cuantificado si es posible)
- Recursos necesarios
- Riesgos de implementación

FORMATO DE RESPUESTA (devuelve SOLO el JSON):
{{
    "quick_wins": [
        {{
            "titulo": "nombre iniciativa",
            "descripcion": "qué hacer",
            "impacto_esperado": "resultado esperado",
            "recursos": "inversión/equipo necesario",
            "timeline": "semanas"
        }}
    ],
    "medio_plazo": [ ... ],
    "largo_plazo": [ ... ],
    "prioridad_1": "la iniciativa MÁS CRÍTICA de todas",
    "roadmap_estrategico": "visión integrada de las 3 fases"
}}
"""
    return prompt

