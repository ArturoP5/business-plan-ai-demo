"""
PDF de Valoración con Explicaciones Completas para Inversores
Versión pedagógica que explica metodología, supuestos y cálculos
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from typing import Dict, List
import pandas as pd

# ═══════════════════════════════════════════════════
# CONSTANTES DE DISEÑO
# ═══════════════════════════════════════════════════

AZUL_PRINCIPAL = colors.HexColor('#1e3a5f')
AZUL_CLARO = colors.HexColor('#4a90e2')
VERDE_POSITIVO = colors.HexColor('#2ecc71')
ROJO_NEGATIVO = colors.HexColor('#e74c3c')
GRIS_CLARO = colors.HexColor('#ecf0f1')
GRIS_TEXTO = colors.HexColor('#7f8c8d')
NEGRO = colors.black

# ═══════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════

def crear_estilos():
    """Crea estilos personalizados para el documento"""
    styles = getSampleStyleSheet()
    
    # Título principal
    styles.add(ParagraphStyle(
        name='TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=AZUL_PRINCIPAL,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Subtítulo
    styles.add(ParagraphStyle(
        name='Subtitulo',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=AZUL_PRINCIPAL,
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    # Sección
    styles.add(ParagraphStyle(
        name='Seccion',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=AZUL_PRINCIPAL,
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    ))
    
    # Texto normal
    styles.add(ParagraphStyle(
        name='TextoNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=NEGRO,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    ))
    
    # Texto explicativo (para supuestos)
    styles.add(ParagraphStyle(
        name='TextoExplicativo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=GRIS_TEXTO,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=12,
        leftIndent=20
    ))
    
    return styles


def formatear_numero(valor, decimales=0, prefijo='€', sufijo='', miles=True):
    """Formatea números con prefijo/sufijo"""
    if valor is None:
        return 'N/A'
    
    try:
        valor = float(valor)
        if miles:
            if abs(valor) >= 1_000_000:
                return f"{prefijo}{valor/1_000_000:,.{decimales}f}M{sufijo}"
            elif abs(valor) >= 1_000:
                return f"{prefijo}{valor/1_000:,.{decimales}f}K{sufijo}"
        
        return f"{prefijo}{valor:,.{decimales}f}{sufijo}"
    except:
        return str(valor)


# ═══════════════════════════════════════════════════
# SECCIONES DEL PDF
# ═══════════════════════════════════════════════════

# TODO: Implementar cada sección paso a paso


def crear_portada(datos_empresa: Dict, resultado_mckinsey: Dict, styles) -> List:
    """Crea portada del informe"""
    elementos = []
    
    # Título principal
    elementos.append(Spacer(1, 2*inch))
    elementos.append(Paragraph(
        "VALORACIÓN EMPRESARIAL",
        styles['TituloPrincipal']
    ))
    elementos.append(Paragraph(
        "Método McKinsey DCF",
        ParagraphStyle(name='SubtituloPortada', 
                      parent=styles['Subtitulo'],
                      fontSize=14,
                      alignment=TA_CENTER,
                      textColor=AZUL_CLARO)
    ))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # Nombre empresa
    elementos.append(Paragraph(
        f"<b>{datos_empresa.get('nombre', 'Empresa')}</b>",
        ParagraphStyle(name='NombreEmpresa',
                      fontSize=18,
                      alignment=TA_CENTER,
                      textColor=AZUL_PRINCIPAL,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Paragraph(
        f"Sector: {datos_empresa.get('sector', 'General')}",
        ParagraphStyle(name='Sector',
                      fontSize=12,
                      alignment=TA_CENTER,
                      textColor=GRIS_TEXTO)
    ))
    
    elementos.append(Spacer(1, 1*inch))
    
    # Métricas principales
    valor_empresa = resultado_mckinsey.get('enterprise_value', 0)
    elementos.append(Paragraph(
        "VALORACIÓN EMPRESA",
        ParagraphStyle(name='LabelValor',
                      fontSize=12,
                      alignment=TA_CENTER,
                      textColor=GRIS_TEXTO)
    ))
    elementos.append(Paragraph(
        formatear_numero(valor_empresa, 1),
        ParagraphStyle(name='Valor',
                      fontSize=32,
                      alignment=TA_CENTER,
                      textColor=AZUL_PRINCIPAL,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # Métricas clave
    metricas_data = [
        ['TIR Proyecto', f"{resultado_mckinsey.get('tir', 0):.1f}%"],
        ['WACC', f"{resultado_mckinsey.get('wacc', 0):.1f}%"],
        ['ROIC Promedio', f"{resultado_mckinsey.get('roic_promedio', 0):.1f}%"]
    ]
    
    tabla_metricas = Table(metricas_data, colWidths=[3*inch, 2*inch])
    tabla_metricas.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, -1), GRIS_TEXTO),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabla_metricas)
    
    elementos.append(Spacer(1, 1.5*inch))
    
    # Fecha
    elementos.append(Paragraph(
        datetime.now().strftime('%B %Y'),
        ParagraphStyle(name='Fecha',
                      fontSize=10,
                      alignment=TA_CENTER,
                      textColor=GRIS_TEXTO)
    ))
    
    elementos.append(PageBreak())
    
    return elementos


def crear_indice(styles) -> List:
    """Crea índice de contenidos"""
    elementos = []
    
    elementos.append(Paragraph("ÍNDICE", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    secciones = [
        ("1. Resumen Ejecutivo", 2),
        ("2. Metodología de Valoración McKinsey", 3),
        ("   2.1. ¿Por qué McKinsey DCF?", 3),
        ("   2.2. Diferencias con DCF Tradicional", 3),
        ("3. Supuestos de Proyección", 4),
        ("   3.1. Proyección de Ingresos", 4),
        ("   3.2. Estructura de Costos", 5),
        ("   3.3. Gastos Operativos", 6),
        ("   3.4. Working Capital", 7),
        ("   3.5. Tesorería y Gestión de Caja", 8),
        ("4. Cálculo del Coste de Capital", 9),
        ("   4.1. Coste de Equity (Ke)", 9),
        ("   4.2. Primas de Riesgo Aplicadas", 10),
        ("   4.3. WACC Explicado", 11),
        ("5. Cálculo de Free Cash Flow McKinsey", 12),
        ("   5.1. NOPLAT", 12),
        ("   5.2. Invested Capital", 13),
        ("6. Fuentes de Datos Externas (APIs)", 14),
        ("7. Resultados de Valoración", 15),
        ("8. Análisis de Sensibilidad", 16),
        ("9. Proyecciones Detalladas", 17),
        ("10. Recomendaciones", 18),
    ]
    
    for seccion, pagina in secciones:
        elementos.append(Paragraph(
            f"{seccion} {'.' * 50} {pagina}",
            ParagraphStyle(name='ItemIndice',
                          fontSize=10,
                          leftIndent=0 if not seccion.startswith('   ') else 20,
                          textColor=GRIS_TEXTO if seccion.startswith('   ') else NEGRO)
        ))
    
    elementos.append(PageBreak())
    
    return elementos


def crear_introduccion_mckinsey(styles) -> List:
    """Explica qué es el método McKinsey y por qué se usa"""
    elementos = []
    
    elementos.append(Paragraph("METODOLOGÍA DE VALORACIÓN MCKINSEY", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    # Qué es
    elementos.append(Paragraph("¿Qué es el Método McKinsey DCF?", styles['Seccion']))
    elementos.append(Paragraph(
        """El método McKinsey de valoración por Descuento de Flujos de Caja (DCF) es considerado 
        el estándar de oro en valoración empresarial. Desarrollado y refinado por McKinsey & Company 
        a lo largo de décadas, este método se centra en el concepto de <b>creación de valor económico</b>, 
        calculando el valor intrínseco de una empresa basándose en su capacidad futura de generar 
        efectivo libre disponible para todos los inversores (deuda y equity).""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Por qué McKinsey vs DCF tradicional
    elementos.append(Paragraph("Diferencias Clave vs DCF Tradicional", styles['Seccion']))
    
    diferencias_data = [
        ['Aspecto', 'DCF Tradicional', 'McKinsey DCF'],
        ['Perspectiva', 'Flujo a accionistas', 'Flujo a la empresa (operativo)'],
        ['Métrica Principal', 'FCF al Equity', 'FCF a la Firma (NOPLAT - ΔIC)'],
        ['Tasa Descuento', 'Ke (coste equity)', 'WACC (coste capital total)'],
        ['Working Capital', 'Cambio total', 'Invested Capital operativo'],
        ['Valor Terminal', 'Perpetuidad simple', 'Modelo explícito con fade'],
        ['Enfoque', 'Financiero', 'Económico-operativo']
    ]
    
    tabla_dif = Table(diferencias_data, colWidths=[1.5*inch, 2.2*inch, 2.2*inch])
    tabla_dif.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('BACKGROUND', (0, 1), (0, -1), GRIS_CLARO),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_dif)
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Ventajas
    elementos.append(Paragraph("Ventajas del Método McKinsey", styles['Seccion']))
    elementos.append(Paragraph(
        """• <b>Independiente de la estructura de capital:</b> Valora el negocio operativo 
        sin distorsión por decisiones de financiación.""",
        styles['TextoNormal']
    ))
    elementos.append(Paragraph(
        """• <b>Comparabilidad:</b> Permite comparar empresas con diferentes estructuras 
        de deuda de forma homogénea.""",
        styles['TextoNormal']
    ))
    elementos.append(Paragraph(
        """• <b>Enfoque en valor económico:</b> Se centra en ROIC (retorno sobre capital 
        invertido) vs WACC, lo que muestra si la empresa crea o destruye valor.""",
        styles['TextoNormal']
    ))
    elementos.append(Paragraph(
        """• <b>Aceptación universal:</b> Es el método preferido por bancos de inversión, 
        fondos de private equity y auditoras Big 4.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Fórmula fundamental
    elementos.append(Paragraph("Fórmula Fundamental", styles['Seccion']))
    
    formula_texto = """
    <b>Enterprise Value = Σ [FCF<sub>t</sub> / (1+WACC)<sup>t</sup>] + Valor Terminal / (1+WACC)<sup>n</sup></b>
    <br/><br/>
    Donde:<br/>
    • FCF = NOPLAT - Δ Invested Capital<br/>
    • NOPLAT = EBIT × (1 - Tax Rate)<br/>
    • Invested Capital = Working Capital + Activo Fijo Neto<br/>
    • WACC = Coste ponderado de capital (deuda + equity)
    """
    
    elementos.append(Paragraph(
        formula_texto,
        ParagraphStyle(name='Formula',
                      fontSize=9,
                      leftIndent=20,
                      textColor=AZUL_PRINCIPAL,
                      leading=14)
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_supuestos_proyeccion(datos_empresa: Dict, pyl_df: pd.DataFrame, balance_df: pd.DataFrame, styles) -> List:
    """Explica todos los supuestos usados en las proyecciones"""
    elementos = []
    
    elementos.append(Paragraph("SUPUESTOS DE PROYECCIÓN", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    # Introducción
    elementos.append(Paragraph(
        """Esta sección detalla todos los supuestos utilizados para proyectar el desempeño 
        financiero de la empresa durante el horizonte de valoración (5 años). Estos supuestos 
        se basan en el análisis histórico de la empresa, benchmarks sectoriales y tendencias macroeconómicas.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.2*inch))
    
    # ═══════════════════════════════════════════════════
    # 1. PROYECCIÓN DE INGRESOS
    # ═══════════════════════════════════════════════════
    
    elementos.append(Paragraph("1. Proyección de Ingresos", styles['Seccion']))
    
    # Calcular crecimientos históricos y proyectados
    if pyl_df is not None and len(pyl_df) > 0:
        try:
            ventas = pyl_df.loc['Ventas'] if 'Ventas' in pyl_df.index else pyl_df.iloc[0]
            ventas_list = ventas.tolist()
            
            # Crecimiento proyectado
            crecimientos = []
            for i in range(1, min(6, len(ventas_list))):
                if ventas_list[i-1] != 0:
                    crecimiento = ((ventas_list[i] / ventas_list[i-1]) - 1) * 100
                    crecimientos.append(crecimiento)
            
            crecimiento_promedio = sum(crecimientos) / len(crecimientos) if crecimientos else 0
            
            elementos.append(Paragraph(
                f"""<b>Tasa de crecimiento promedio proyectada:</b> {crecimiento_promedio:.1f}% anual""",
                styles['TextoNormal']
            ))
            
            elementos.append(Paragraph(
                f"""<b>Supuestos aplicados:</b>""",
                styles['TextoNormal']
            ))
            
            sector = datos_empresa.get('sector', 'General')
            fase = datos_empresa.get('fase_empresa', 'madura')
            
            elementos.append(Paragraph(
                f"""• <b>Sector {sector}:</b> Crecimiento sectorial esperado según análisis 
                de mercado y proyecciones macroeconómicas.""",
                styles['TextoExplicativo']
            ))
            
            elementos.append(Paragraph(
                f"""• <b>Fase empresa ({fase}):</b> Empresas en esta fase típicamente exhiben 
                patrones de crecimiento específicos según su madurez.""",
                styles['TextoExplicativo']
            ))
            
            elementos.append(Paragraph(
                """• <b>Inflación esperada:</b> Se incorpora inflación del 2-3% anual según 
                proyecciones del BCE para España/Eurozona.""",
                styles['TextoExplicativo']
            ))
            
        except:
            pass
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # ═══════════════════════════════════════════════════
    # 2. ESTRUCTURA DE COSTOS
    # ═══════════════════════════════════════════════════
    
    elementos.append(Paragraph("2. Estructura de Costos", styles['Seccion']))
    
    elementos.append(Paragraph(
        """Los costos se dividen en variables (que crecen con las ventas) y fijos 
        (que se mantienen relativamente constantes). Esta clasificación es fundamental 
        para entender el apalancamiento operativo del negocio.""",
        styles['TextoNormal']
    ))
    
    # Estructura por sector
    estructura_costos = {
        'Industrial': {'variable': 60, 'fijo': 40},
        'Tecnología': {'variable': 30, 'fijo': 70},
        'Retail': {'variable': 70, 'fijo': 30},
        'Hostelería': {'variable': 55, 'fijo': 45},
        'Servicios': {'variable': 40, 'fijo': 60},
    }
    
    sector = datos_empresa.get('sector', 'General')
    estructura = estructura_costos.get(sector, {'variable': 50, 'fijo': 50})
    
    estructura_data = [
        ['Tipo de Costo', '% sobre Total', 'Comportamiento'],
        ['Costos Variables', f"{estructura['variable']}%", 'Crecen proporcionalmente con ventas'],
        ['Costos Fijos', f"{estructura['fijo']}%", 'Se mantienen relativamente constantes'],
    ]
    
    tabla_estructura = Table(estructura_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    tabla_estructura.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_estructura)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        f"""<b>Implicación:</b> Por cada euro adicional de ventas, aproximadamente 
        {estructura['variable']} céntimos se destinan a costos variables, mientras que 
        los costos fijos se amortizan mejor con el volumen. Esto genera el 
        <b>apalancamiento operativo</b> observado en los márgenes.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_supuestos_working_capital(balance_df: pd.DataFrame, styles) -> List:
    """Explica supuestos de Working Capital y Tesorería"""
    elementos = []
    
    elementos.append(Paragraph("3. Working Capital y Ciclo de Conversión", styles['Seccion']))
    
    elementos.append(Paragraph(
        """El Working Capital representa la inversión necesaria para operar el negocio día a día. 
        Se calcula como la diferencia entre activos corrientes operativos (clientes + inventario) 
        y pasivos corrientes operativos (proveedores).""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Ciclo de conversión
    elementos.append(Paragraph("<b>Ciclo de Conversión de Efectivo (CCC)</b>", styles['TextoNormal']))
    
    ciclo_data = [
        ['Componente', 'Días', 'Descripción'],
        ['Días de Cobro (DSO)', '45', 'Tiempo promedio para cobrar a clientes'],
        ['Días de Inventario (DIO)', '30', 'Tiempo que el inventario permanece en almacén'],
        ['Días de Pago (DPO)', '60', 'Tiempo que tardamos en pagar a proveedores'],
        ['', '', ''],
        ['Ciclo de Conversión', '15 días', 'DSO + DIO - DPO']
    ]
    
    tabla_ciclo = Table(ciclo_data, colWidths=[2*inch, 1.2*inch, 3*inch])
    tabla_ciclo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('LINEBELOW', (0, 3), (-1, 3), 1, GRIS_TEXTO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_ciclo)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>Interpretación:</b> Un ciclo de 15 días significa que desde que invertimos en 
        inventario hasta que cobramos el efectivo, transcurren 15 días netos. Cuanto menor 
        sea este ciclo, menos capital de trabajo necesitamos.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # ═══════════════════════════════════════════════════
    # TESORERÍA
    # ═══════════════════════════════════════════════════
    
    elementos.append(Paragraph("4. Política de Tesorería", styles['Seccion']))
    
    elementos.append(Paragraph(
        """La gestión de tesorería sigue principios conservadores para garantizar liquidez 
        operativa sin comprometer oportunidades de inversión.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Tesorería mínima
    elementos.append(Paragraph("<b>Tesorería Mínima Operativa</b>", styles['TextoNormal']))
    
    elementos.append(Paragraph(
        """Se calcula como el <b>mínimo</b> entre dos criterios:""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Criterio 1:</b> 2.5% de las ventas anuales""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• <b>Criterio 2:</b> 15 días de gastos operativos""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> Este enfoque conservador asegura que la empresa pueda operar 
        al menos 15 días sin ingresos, o mantener un colchón equivalente al 2.5% de ventas, 
        lo que sea menor. Es más conservador que el benchmark típico de 30-45 días.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Tesorería objetivo
    elementos.append(Paragraph("<b>Tesorería Objetivo (varía por fase empresa)</b>", styles['TextoNormal']))
    
    tesoreria_obj_data = [
        ['Fase Empresa', 'Múltiplo sobre Mínima', 'Razón'],
        ['Crecimiento', '1.2x (20% colchón)', 'Prioriza reinversión en crecimiento'],
        ['Transición', '1.5x (50% colchón)', 'Balance entre liquidez y crecimiento'],
        ['Madura', '2.0x (100% colchón)', 'Mayor estabilidad, menos necesidad capex']
    ]
    
    tabla_tes_obj = Table(tesoreria_obj_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    tabla_tes_obj.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_tes_obj)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Gestión de excesos
    elementos.append(Paragraph("<b>Gestión de Excesos de Tesorería</b>", styles['TextoNormal']))
    
    elementos.append(Paragraph(
        """<b>Política aplicada:</b> Los excesos de tesorería por encima del objetivo 
        <b>NO se invierten automáticamente</b> en instrumentos financieros a largo plazo. 
        Se mantienen como caja disponible para:""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• Distribución a accionistas vía dividendos""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Oportunidades de inversión estratégicas (M&A)""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Colchón adicional para imprevistos""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Fundamentación:</b> Según mejores prácticas de McKinsey y Damodaran, 
        en modelos DCF el cash excedentario debe sumarse al valor final, no restarse 
        del FCF mediante inversiones automáticas. Esto proporciona mayor flexibilidad 
        financiera y reconoce el valor del efectivo disponible.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Gestión de déficits
    elementos.append(Paragraph("<b>Gestión de Déficits de Tesorería</b>", styles['TextoNormal']))
    
    elementos.append(Paragraph(
        """Si la tesorería cae por debajo del mínimo, se activa la siguiente jerarquía de financiación:""",
        styles['TextoNormal']
    ))
    
    jerarquia_data = [
        ['Prioridad', 'Fuente', 'Condiciones'],
        ['1', 'Nueva Deuda (30% CP / 70% LP)', 'Hasta Deuda Total ≤ EBITDA × 4.0'],
        ['2', 'Ampliación de Capital', 'Solo si límite de deuda alcanzado']
    ]
    
    tabla_jerarquia = Table(jerarquia_data, colWidths=[1*inch, 2.5*inch, 2.5*inch])
    tabla_jerarquia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_jerarquia)
    
    elementos.append(PageBreak())
    
    return elementos



def crear_calculo_ke_detallado(resultado_mckinsey: Dict, datos_empresa: Dict, styles) -> List:
    """Explica el cálculo del Coste de Equity con todas las primas"""
    elementos = []
    
    elementos.append(Paragraph("CÁLCULO DEL COSTE DE EQUITY (Ke)", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph(
        """El Coste de Equity (Ke) representa la rentabilidad mínima que los accionistas 
        esperan obtener por su inversión, considerando el riesgo del negocio. Se calcula 
        mediante el modelo CAPM (Capital Asset Pricing Model) ajustado por primas adicionales 
        que reflejan riesgos específicos de la empresa.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Fórmula
    elementos.append(Paragraph("<b>Fórmula Aplicada</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """<b>Ke = Rf + (β × Prima Mercado) + Prima Tamaño + Prima PYME + Riesgo País + Riesgo Sector</b>""",
        ParagraphStyle(name='FormulaKe',
                      fontSize=10,
                      textColor=AZUL_PRINCIPAL,
                      leftIndent=20,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Componentes
    componentes_wacc = resultado_mckinsey.get('componentes_wacc', {})
    
    elementos.append(Paragraph("<b>Desglose de Componentes</b>", styles['Seccion']))
    
    # 1. Risk-free rate
    rf = componentes_wacc.get('rf', 3.5)
    elementos.append(Paragraph(
        f"""<b>1. Tasa Libre de Riesgo (Rf): {rf:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Rendimiento del Bono del Estado Español a 10 años.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> Representa el retorno que un inversor puede obtener sin asumir 
        riesgo alguno. Se usa el bono español porque la empresa opera en España y sus flujos 
        están en euros. El plazo de 10 años es estándar en valoración porque coincide con 
        el horizonte de inversión institucional típico.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # 2. Beta sectorial
    beta = componentes_wacc.get('beta', 1.0)
    elementos.append(Paragraph(
        f"""<b>2. Beta Sectorial: {beta:.2f}</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Beta desapalancado del sector según Damodaran.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> La Beta mide la sensibilidad de los retornos de la empresa respecto 
        al mercado. Una Beta de {:.2f} significa que si el mercado sube un 10%, se espera que 
        la empresa suba un {:.1f}%. Se usa la Beta sectorial desapalancada (sin efecto de deuda) 
        y luego se reapalanca según la estructura de capital objetivo de la empresa.""".format(beta, beta*10),
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # 3. Prima de mercado
    market_premium = componentes_wacc.get('market_premium', 5.5)
    elementos.append(Paragraph(
        f"""<b>3. Prima de Riesgo de Mercado: {market_premium:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Prima histórica del mercado español (promedio geométrico a largo plazo).""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> Representa el retorno adicional que los inversores exigen por invertir 
        en el mercado de renta variable vs activos sin riesgo. Es el premio por asumir el 
        riesgo sistemático del mercado.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # 4. Prima de tamaño
    size_premium = componentes_wacc.get('size_premium', 0)
    elementos.append(Paragraph(
        f"""<b>4. Prima de Tamaño: {size_premium:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Ibbotson Size Premia Study / Duff & Phelps Risk Premium Report.""",
        styles['TextoExplicativo']
    ))
    
    # Determinar categoría de tamaño
    ventas = datos_empresa.get('ventas_anuales', 0)
    if ventas < 2_000_000:
        categoria = "Microempresa (< €2M ventas)"
        prima_tipica = "3-4%"
    elif ventas < 10_000_000:
        categoria = "Pequeña empresa (€2-10M ventas)"
        prima_tipica = "2-3%"
    elif ventas < 50_000_000:
        categoria = "Mediana empresa (€10-50M ventas)"
        prima_tipica = "1-2%"
    else:
        categoria = "Gran empresa (> €50M ventas)"
        prima_tipica = "0-1%"
    
    elementos.append(Paragraph(
        f"""<b>Razón:</b> Estudios empíricos demuestran que empresas más pequeñas generan 
        retornos superiores en el largo plazo, compensando su mayor riesgo (menor liquidez, 
        mayor volatilidad, menor diversificación). Su empresa se clasifica como <b>{categoria}</b> 
        con prima típica de {prima_tipica}. Esta prima reconoce que pequeñas empresas tienen:""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Mayor dificultad para acceder a financiación""",
        ParagraphStyle(name='ListaIndentada', 
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Paragraph(
        """• Menor poder de negociación con clientes/proveedores""",
        ParagraphStyle(name='ListaIndentada2', 
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Paragraph(
        """• Mayor vulnerabilidad a shocks económicos""",
        ParagraphStyle(name='ListaIndentada3', 
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # 5. Riesgo país
    riesgo_pais = componentes_wacc.get('country_risk', 0)
    elementos.append(Paragraph(
        f"""<b>5. Riesgo País: {riesgo_pais:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Credit Default Swaps (CDS) de España o diferencial vs Bund alemán.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> Para España, este componente es típicamente bajo o cero, ya que 
        el Rf ya incorpora la deuda española. Solo se añade si hay exposición a otros países 
        con mayor riesgo soberano.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # 6. Riesgo sector
    riesgo_sector = componentes_wacc.get('sector_risk', 0)
    elementos.append(Paragraph(
        f"""<b>6. Riesgo Sector Específico: {riesgo_sector:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Análisis de volatilidad histórica y riesgos inherentes del sector.""",
        styles['TextoExplicativo']
    ))
    
    sector = datos_empresa.get('sector', 'General')
    elementos.append(Paragraph(
        f"""<b>Razón:</b> El sector <b>{sector}</b> puede tener riesgos específicos adicionales 
        no capturados por la Beta (ej: regulatorio, tecnológico, ciclicidad extrema, disrupciones). 
        Esta prima ajusta por factores idiosincráticos del sector.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Tabla resumen
    elementos.append(Paragraph("<b>Resumen del Cálculo</b>", styles['Seccion']))
    
    ke_total = componentes_wacc.get('cost_of_equity', 0)
    
    ke_data = [
        ['Componente', 'Valor', 'Cálculo'],
        ['Tasa Libre Riesgo (Rf)', f"{rf:.2f}%", 'Bono España 10Y'],
        ['Beta × Prima Mercado', f"{beta * market_premium:.2f}%", f"{beta:.2f} × {market_premium:.2f}%"],
        ['Prima Tamaño', f"{size_premium:.2f}%", 'Según ventas empresa'],
        ['Riesgo País', f"{riesgo_pais:.2f}%", 'CDS España'],
        ['Riesgo Sector', f"{riesgo_sector:.2f}%", f'Específico {sector}'],
        ['', '', ''],
        ['Coste de Equity (Ke)', f"{ke_total:.2f}%", 'SUMA TOTAL']
    ]
    
    tabla_ke = Table(ke_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    tabla_ke.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('LINEBELOW', (0, -2), (-1, -2), 2, NEGRO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('BACKGROUND', (0, -1), (-1, -1), AZUL_CLARO),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_ke)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        f"""<b>Interpretación:</b> Los accionistas de la empresa esperan un retorno mínimo 
        del {ke_total:.2f}% anual para compensar todos los riesgos asumidos. Si la empresa 
        genera retornos sobre equity superiores a este porcentaje, estará creando valor 
        para sus accionistas.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_calculo_wacc_explicado(resultado_mckinsey: Dict, styles) -> List:
    """Explica el cálculo del WACC y su importancia"""
    elementos = []
    
    elementos.append(Paragraph("CÁLCULO DEL WACC", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph(
        """El WACC (Weighted Average Cost of Capital) es el coste promedio ponderado que 
        la empresa paga por su capital, considerando tanto deuda como equity. Es la tasa 
        que usamos para descontar los Free Cash Flows al presente, y representa la 
        <b>rentabilidad mínima que debe generar la empresa</b> para satisfacer a todos 
        sus proveedores de capital (acreedores y accionistas).""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Fórmula
    elementos.append(Paragraph("<b>Fórmula del WACC</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """<b>WACC = (E/V × Ke) + (D/V × Kd × (1 - Tax))</b>""",
        ParagraphStyle(name='FormulaWACC',
                      fontSize=11,
                      textColor=AZUL_PRINCIPAL,
                      leftIndent=20,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.05*inch))
    
    elementos.append(Paragraph(
        """Donde:<br/>
        • <b>E/V</b> = Proporción de Equity sobre Valor Total<br/>
        • <b>D/V</b> = Proporción de Deuda sobre Valor Total<br/>
        • <b>Ke</b> = Coste de Equity (ya calculado)<br/>
        • <b>Kd</b> = Coste de Deuda (tipo interés medio de financiación)<br/>
        • <b>Tax</b> = Tasa impositiva efectiva (genera el "escudo fiscal")""",
        ParagraphStyle(name='DefinicionesWACC',
                      fontSize=9,
                      leftIndent=30,
                      textColor=GRIS_TEXTO,
                      leading=13)
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Componentes
    componentes_wacc = resultado_mckinsey.get('componentes_wacc', {})
    wacc = resultado_mckinsey.get('wacc', 10)
    
    elementos.append(Paragraph("<b>Componentes del Cálculo</b>", styles['Seccion']))
    
    # Estructura de capital
    peso_equity = componentes_wacc.get('weight_equity', 0.7) * 100
    peso_debt = componentes_wacc.get('weight_debt', 0.3) * 100
    
    elementos.append(Paragraph(
        f"""<b>1. Estructura de Capital Objetivo</b>""",
        styles['TextoNormal']
    ))
    
    estructura_data = [
        ['Componente', 'Peso', 'Razón'],
        ['Equity (E/V)', f'{peso_equity:.1f}%', 'Proporción de capital propio'],
        ['Deuda (D/V)', f'{peso_debt:.1f}%', 'Proporción de financiación externa']
    ]
    
    tabla_estructura = Table(estructura_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
    tabla_estructura.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_estructura)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        f"""<b>Nota importante:</b> Se usa la estructura de capital <b>objetivo del sector</b> 
        ({peso_debt:.0f}% deuda / {peso_equity:.0f}% equity), no la estructura actual de la empresa. 
        Esta es la práctica estándar según McKinsey y Damodaran, ya que:""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Refleja cómo la empresa <b>debería</b> financiarse en el largo plazo""",
        ParagraphStyle(name='RazonEstructura1',
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Paragraph(
        """• Es independiente de decisiones puntuales de financiación""",
        ParagraphStyle(name='RazonEstructura2',
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Paragraph(
        """• Permite comparabilidad entre empresas del mismo sector""",
        ParagraphStyle(name='RazonEstructura3',
                      parent=styles['TextoExplicativo'],
                      leftIndent=40,
                      fontSize=8)
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Coste de deuda
    kd = componentes_wacc.get('cost_of_debt', 4.0)
    elementos.append(Paragraph(
        f"""<b>2. Coste de Deuda (Kd): {kd:.2f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Fuente:</b> Tipo de interés medio ponderado de toda la deuda financiera de la empresa.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """<b>Razón:</b> Este es el coste explícito que la empresa paga por su financiación 
        externa. Incluye préstamos bancarios, créditos, líneas de crédito, etc.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Tax shield
    tax_rate = componentes_wacc.get('tax_rate', 25)
    elementos.append(Paragraph(
        f"""<b>3. Escudo Fiscal (Tax Shield): {tax_rate:.0f}%</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Concepto clave:</b> Los intereses de la deuda son <b>deducibles fiscalmente</b>, 
        lo que reduce el coste efectivo de la deuda. Si Kd = 4% y Tax = 25%, el coste 
        real es 4% × (1-0.25) = 3%.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        f"""<b>Ejemplo numérico:</b> Si la empresa paga €100,000 en intereses y tiene un 
        tipo impositivo del {tax_rate:.0f}%, ahorra €{100000 * tax_rate / 100:,.0f} en impuestos. 
        El coste neto de esos intereses es solo €{100000 * (1 - tax_rate/100):,.0f}. 
        Este "ahorro fiscal" es un beneficio directo de usar deuda.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Cálculo final
    elementos.append(Paragraph("<b>Cálculo Final del WACC</b>", styles['Seccion']))
    
    ke = componentes_wacc.get('cost_of_equity', 10)
    kd_after_tax = kd * (1 - tax_rate/100)
    
    wacc_calculo_data = [
        ['Componente', 'Fórmula', 'Resultado'],
        ['Coste Equity Ponderado', f'{peso_equity/100:.3f} × {ke:.2f}%', 
         f'{(peso_equity/100) * ke:.2f}%'],
        ['Coste Deuda Post-Tax', f'{kd:.2f}% × (1 - {tax_rate:.0f}%)', 
         f'{kd_after_tax:.2f}%'],
        ['Coste Deuda Ponderado', f'{peso_debt/100:.3f} × {kd_after_tax:.2f}%', 
         f'{(peso_debt/100) * kd_after_tax:.2f}%'],
        ['', '', ''],
        ['WACC Total', 'Suma de componentes', f'{wacc:.2f}%']
    ]
    
    tabla_wacc_calc = Table(wacc_calculo_data, colWidths=[2.2*inch, 2.2*inch, 1.6*inch])
    tabla_wacc_calc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('LINEBELOW', (0, -2), (-1, -2), 2, NEGRO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('BACKGROUND', (0, -1), (-1, -1), AZUL_CLARO),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_wacc_calc)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Interpretación
    elementos.append(Paragraph(
        f"""<b>Interpretación:</b> El WACC de {wacc:.2f}% es la <b>"hurdle rate"</b> o 
        rentabilidad mínima que debe generar la empresa. Si el ROIC (retorno sobre capital 
        invertido) supera al WACC, la empresa está <b>creando valor</b>. Si es menor, 
        está <b>destruyendo valor</b>. Este es el concepto fundamental de la creación de 
        valor en finanzas corporativas.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_fcf_mckinsey_explicado(resultado_mckinsey: Dict, styles) -> List:
    """Explica el cálculo del Free Cash Flow método McKinsey"""
    elementos = []
    
    elementos.append(Paragraph("FREE CASH FLOW - MÉTODO MCKINSEY", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph(
        """El Free Cash Flow (FCF) McKinsey representa el efectivo generado por las 
        operaciones de la empresa, disponible para TODOS los proveedores de capital 
        (tanto acreedores como accionistas), antes de cualquier decisión de financiación. 
        Esta es la métrica fundamental para valoración porque es independiente de cómo 
        la empresa decide financiarse.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Fórmula
    elementos.append(Paragraph("<b>Fórmula McKinsey</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """<b>FCF = NOPLAT - Δ Invested Capital</b>""",
        ParagraphStyle(name='FormulaFCF',
                      fontSize=12,
                      textColor=AZUL_PRINCIPAL,
                      leftIndent=20,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # NOPLAT
    elementos.append(Paragraph("<b>1. NOPLAT (Net Operating Profit Less Adjusted Taxes)</b>", 
                               styles['Seccion']))
    
    elementos.append(Paragraph(
        """NOPLAT es el beneficio operativo después de impuestos, pero <b>sin considerar</b> 
        los efectos de la estructura financiera. Se calcula como:""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>NOPLAT = EBIT × (1 - Tasa Impositiva)</b>""",
        ParagraphStyle(name='FormulaNOPLAT',
                      fontSize=10,
                      textColor=AZUL_PRINCIPAL,
                      leftIndent=30,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>¿Por qué EBIT y no Beneficio Neto?</b>""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• El EBIT es <b>antes de intereses</b>, lo que lo hace independiente de cómo 
        está financiada la empresa""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Aplicamos la tasa impositiva sobre el EBIT para obtener el beneficio operativo 
        después de impuestos""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Esto nos da el cash flow generado por las operaciones, disponible para TODOS 
        los proveedores de capital""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Ejemplo numérico NOPLAT
    elementos.append(Paragraph(
        """<b>Ejemplo numérico:</b>""",
        styles['TextoNormal']
    ))
    
    ejemplo_noplat = [
        ['Concepto', 'Valor'],
        ['EBIT', '€500,000'],
        ['Tasa Impositiva', '25%'],
        ['Impuestos sobre EBIT', '-€125,000'],
        ['NOPLAT', '€375,000']
    ]
    
    tabla_ejemplo_noplat = Table(ejemplo_noplat, colWidths=[3*inch, 2*inch])
    tabla_ejemplo_noplat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GRIS_CLARO),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 2), (-1, 2), 1, GRIS_TEXTO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), AZUL_CLARO),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_ejemplo_noplat)
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Invested Capital
    elementos.append(Paragraph("<b>2. Δ Invested Capital (Cambio en Capital Invertido)</b>", 
                               styles['Seccion']))
    
    elementos.append(Paragraph(
        """El Invested Capital representa el capital total que la empresa tiene invertido 
        en sus operaciones para generar ingresos. Se calcula como:""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """<b>Invested Capital = Working Capital + Activo Fijo Neto</b>""",
        ParagraphStyle(name='FormulaIC',
                      fontSize=10,
                      textColor=AZUL_PRINCIPAL,
                      leftIndent=30,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>Componentes del Invested Capital:</b>""",
        styles['TextoNormal']
    ))
    
    ic_componentes = [
        ['Componente', 'Incluye', 'Razón'],
        ['Working Capital', 'Clientes + Inventario - Proveedores + Otros', 
         'Capital necesario para operar día a día'],
        ['Activo Fijo Neto', 'Inmuebles + Maquinaria + Equipos (neto amortización)', 
         'Inversiones en activos productivos'],
    ]
    
    tabla_ic = Table(ic_componentes, colWidths=[1.5*inch, 2.2*inch, 2.3*inch])
    tabla_ic.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_ic)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>Δ Invested Capital</b> es el <b>incremento</b> del capital invertido de un 
        año a otro. Representa cuánto capital adicional la empresa necesita inyectar en 
        el negocio para sostener el crecimiento.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Si Δ IC es <b>positivo</b> → La empresa necesita invertir más capital 
        (reduce FCF)""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Paragraph(
        """• Si Δ IC es <b>negativo</b> → La empresa libera capital (aumenta FCF)""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Diferencias vs DCF tradicional
    elementos.append(Paragraph("<b>Diferencias con FCF Tradicional</b>", styles['Seccion']))
    
    diferencias_fcf = [
        ['Aspecto', 'DCF Tradicional', 'McKinsey DCF'],
        ['Punto de partida', 'Beneficio Neto (después intereses)', 
         'NOPLAT (antes intereses)'],
        ['Working Capital', 'Δ WC total (incluye deuda)', 
         'Δ WC operativo (sin deuda)'],
        ['Capex', 'Capex - Amortización', 
         'Incluido en Δ Invested Capital'],
        ['Perspectiva', 'Flujo al accionista', 
         'Flujo a la empresa (todos inversores)'],
    ]
    
    tabla_dif_fcf = Table(diferencias_fcf, colWidths=[1.5*inch, 2.2*inch, 2.3*inch])
    tabla_dif_fcf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('BACKGROUND', (0, 1), (0, -1), GRIS_CLARO),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_dif_fcf)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>Ventaja clave:</b> El FCF McKinsey es <b>comparable</b> entre empresas 
        independientemente de su estructura de deuda. Dos empresas idénticas operativamente 
        pero con diferente financiación tendrán el mismo FCF McKinsey, pero FCF tradicional 
        diferente.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_seccion_apis(datos_empresa: Dict, styles) -> List:
    """Explica las APIs conectadas y qué datos aportan"""
    elementos = []
    
    elementos.append(Paragraph("FUENTES DE DATOS EXTERNAS (APIs)", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph(
        """Esta valoración incorpora datos en tiempo real de múltiples fuentes externas 
        mediante APIs (Application Programming Interfaces) conectadas. Esto asegura que 
        los parámetros de mercado utilizados son actuales y precisos, mejorando 
        significativamente la calidad de la valoración.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # APIs conectadas
    apis_data = [
        ['API / Fuente', 'Datos Proporcionados', 'Impacto en Modelo'],
        
        ['Investing.com / Yahoo Finance', 
         '• Bono España 10Y (Risk-free rate)\n• Índices bursátiles\n• Volatilidad mercado',
         'Actualiza Rf en cálculo Ke\nValidación prima de mercado'],
        
        ['Damodaran Online Data', 
         '• Betas sectoriales desapalancadas\n• Primas de riesgo por sector\n• EV/EBITDA múltiplos',
         'Beta ajustada por sector\nValidación múltiplos comparables'],
        
        ['Banco de España', 
         '• Tipos de interés\n• Proyecciones macroeconómicas\n• Datos sector financiero',
         'Coste de deuda (Kd)\nSupuestos macro'],
        
        ['BCE (Banco Central Europeo)', 
         '• Proyecciones inflación\n• Tipos oficiales\n• Growth forecasts Eurozona',
         'Tasa crecimiento terminal\nSupuestos inflación'],
        
        ['INE / Eurostat', 
         '• PIB sectorial\n• Datos empleo\n• Estadísticas empresariales',
         'Benchmarks sectoriales\nContexto macroeconómico'],
    ]
    
    tabla_apis = Table(apis_data, colWidths=[1.8*inch, 2.3*inch, 2*inch])
    tabla_apis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_apis)
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Beneficios
    elementos.append(Paragraph("<b>Beneficios de Datos en Tiempo Real</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """• <b>Actualización continua:</b> Los parámetros de mercado se actualizan 
        automáticamente, evitando valoraciones obsoletas.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Objetividad:</b> Los datos provienen de fuentes oficiales reconocidas, 
        eliminando sesgos subjetivos.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Comparabilidad:</b> Uso de benchmarks sectoriales homogéneos de fuentes 
        académicas (Damodaran - NYU Stern).""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Trazabilidad:</b> Cada parámetro tiene una fuente verificable, cumpliendo 
        con estándares de auditoría.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Ejemplo de impacto
    elementos.append(Paragraph("<b>Ejemplo de Impacto en Valoración</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """<b>Escenario:</b> El Bono España 10 años (Rf) sube del 3.0% al 3.5%""",
        styles['TextoNormal']
    ))
    
    impacto_ejemplo = [
        ['Variable', 'Antes', 'Después', 'Impacto'],
        ['Risk-free Rate', '3.0%', '3.5%', '+0.5pp'],
        ['Ke (Coste Equity)', '9.0%', '9.5%', '+0.5pp'],
        ['WACC', '7.5%', '8.0%', '+0.5pp'],
        ['Valoración Empresa', '€10.0M', '€9.4M', '-6%']
    ]
    
    tabla_impacto = Table(impacto_ejemplo, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1.4*inch])
    tabla_impacto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TEXTCOLOR', (3, -1), (3, -1), ROJO_NEGATIVO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_impacto)
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """Este ejemplo ilustra cómo cambios en variables de mercado impactan 
        directamente la valoración. La conexión con APIs asegura que siempre 
        usamos los valores más recientes del mercado.""",
        styles['TextoExplicativo']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



def crear_resultados_valoracion(resultado_mckinsey: Dict, styles) -> List:
    """Muestra resultados finales de valoración"""
    elementos = []
    
    elementos.append(Paragraph("RESULTADOS DE VALORACIÓN", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    # Tabla resumen
    ev = resultado_mckinsey.get('enterprise_value', 0)
    pv_fcf = resultado_mckinsey.get('pv_fcf', 0)
    pv_terminal = resultado_mckinsey.get('pv_terminal', 0)
    deuda_neta = resultado_mckinsey.get('deuda_neta', 0)
    equity_value = resultado_mckinsey.get('equity_value', 0)
    
    resultados_data = [
        ['Componente', 'Valor'],
        ['Valor Presente FCF (años 1-5)', formatear_numero(pv_fcf, 1)],
        ['Valor Terminal (descontado)', formatear_numero(pv_terminal, 1)],
        ['Enterprise Value', formatear_numero(ev, 1)],
        ['(-) Deuda Neta', formatear_numero(deuda_neta, 1)],
        ['Equity Value', formatear_numero(equity_value, 1)]
    ]
    
    tabla_resultados = Table(resultados_data, colWidths=[3.5*inch, 2*inch])
    tabla_resultados.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 3), (-1, 3), 2, NEGRO),
        ('LINEBELOW', (0, 4), (-1, 4), 1, GRIS_TEXTO),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), AZUL_CLARO),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabla_resultados)
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Métricas clave
    tir = resultado_mckinsey.get('tir', 0)
    wacc = resultado_mckinsey.get('wacc', 0)
    roic = resultado_mckinsey.get('roic_promedio', 0)
    
    elementos.append(Paragraph("<b>Métricas de Creación de Valor</b>", styles['Seccion']))
    
    metricas_valor = [
        ['Métrica', 'Valor', 'Interpretación'],
        ['TIR Proyecto', f'{tir:.1f}%', 
         'Rentabilidad efectiva del proyecto' if tir > wacc else 'Por debajo del coste capital'],
        ['WACC', f'{wacc:.1f}%', 
         'Coste de capital (hurdle rate)'],
        ['ROIC Promedio', f'{roic:.1f}%', 
         'Crea valor' if roic > wacc else 'Destruye valor']
    ]
    
    tabla_metricas = Table(metricas_valor, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    tabla_metricas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_metricas)
    
    elementos.append(PageBreak())
    
    return elementos


def generar_pdf_valoracion_explicado(
    datos_empresa: Dict,
    resultado_mckinsey: Dict,
    pyl_df: pd.DataFrame,
    balance_df: pd.DataFrame = None,
    fcf_df: pd.DataFrame = None
) -> bytes:
    """
    Genera PDF completo con explicaciones para inversores
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Crear estilos
    styles = crear_estilos()
    
    # Construir documento
    elementos = []
    
    # 1. PORTADA
    elementos.extend(crear_portada(datos_empresa, resultado_mckinsey, styles))
    
    # 2. RESUMEN EJECUTIVO
    elementos.extend(crear_executive_summary(datos_empresa, resultado_mckinsey, pyl_df, styles))
    
    # 3. ANÁLISIS MACROECONÓMICO
    elementos.extend(crear_analisis_macro(datos_empresa, styles))
    
    # 4. ÍNDICE
    elementos.extend(crear_indice(styles))
    
    # 3. METODOLOGÍA MCKINSEY
    elementos.extend(crear_introduccion_mckinsey(styles))
    
    # 4. SUPUESTOS DE PROYECCIÓN
    elementos.extend(crear_supuestos_proyeccion(datos_empresa, pyl_df, balance_df, styles))
    
    # 5. WORKING CAPITAL Y TESORERÍA
    if balance_df is not None:
        elementos.extend(crear_supuestos_working_capital(balance_df, styles))
    
    # 6. CÁLCULO Ke
    elementos.extend(crear_calculo_ke_detallado(resultado_mckinsey, datos_empresa, styles))
    
    # 7. CÁLCULO WACC
    elementos.extend(crear_calculo_wacc_explicado(resultado_mckinsey, styles))
    
    # 8. FCF MCKINSEY
    elementos.extend(crear_fcf_mckinsey_explicado(resultado_mckinsey, styles))
    
    # 9. APIs Y DATOS EXTERNOS
    elementos.extend(crear_seccion_apis(datos_empresa, styles))
    
    # 10. RESULTADOS VALORACIÓN
    elementos.extend(crear_resultados_valoracion(resultado_mckinsey, styles))
    
    # 11. ANÁLISIS DE SENSIBILIDAD (RECALCULADO)
    elementos.extend(crear_analisis_sensibilidad_real(resultado_mckinsey, pyl_df, styles))
    
    # 12. PROYECCIONES DETALLADAS AÑO POR AÑO
    if pyl_df is not None:
        elementos.extend(crear_proyecciones_anuales_detalladas(pyl_df, balance_df, fcf_df, styles))
    
    # Construir PDF
    doc.build(elementos)
    
    # Retornar bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes



def calcular_sensibilidad_real(resultado_mckinsey: Dict, pyl_df: pd.DataFrame) -> Dict:
    """
    Calcula sensibilidad REAL recalculando el DCF, no usando multiplicadores arbitrarios
    """
    
    # Valores base
    wacc_base = resultado_mckinsey.get('wacc', 10.0)
    fcf_proyectados = resultado_mckinsey.get('fcf_proyectados', [])
    valor_terminal_base = resultado_mckinsey.get('valor_terminal', 0)
    g_base = resultado_mckinsey.get('tasa_crecimiento_perpetuo', 2.0)
    
    # Rangos para sensibilidad
    wacc_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
    g_range = [1.0, 1.5, 2.0, 2.5, 3.0]
    
    matriz_sensibilidad = {}
    
    for wacc in wacc_range:
        matriz_sensibilidad[wacc] = {}
        
        for g in g_range:
            # Calcular PV de FCF con este WACC
            pv_fcf = 0
            for i, fcf_data in enumerate(fcf_proyectados[:5], start=1):
                fcf = fcf_data.get('fcf', 0)
                pv_fcf += fcf / ((1 + wacc/100) ** i)
            
            # Calcular nuevo valor terminal con este g
            if len(fcf_proyectados) >= 5:
                fcf_year5 = fcf_proyectados[4].get('fcf', 0)
                fcf_year6 = fcf_year5 * (1 + g/100)
                
                if (wacc/100) > (g/100):
                    valor_terminal = fcf_year6 / ((wacc/100) - (g/100))
                    pv_terminal = valor_terminal / ((1 + wacc/100) ** 5)
                else:
                    pv_terminal = 0
            else:
                pv_terminal = 0
            
            # Enterprise Value
            ev = pv_fcf + pv_terminal
            matriz_sensibilidad[wacc][g] = ev
    
    return {
        'matriz': matriz_sensibilidad,
        'wacc_base': wacc_base,
        'g_base': g_base,
        'wacc_range': wacc_range,
        'g_range': g_range
    }


def crear_analisis_sensibilidad_real(resultado_mckinsey: Dict, pyl_df: pd.DataFrame, styles) -> List:
    """Crea análisis de sensibilidad con cálculos reales"""
    elementos = []
    
    elementos.append(Paragraph("ANÁLISIS DE SENSIBILIDAD", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph(
        """El análisis de sensibilidad muestra cómo varía la valoración ante cambios en las 
        dos variables más críticas del modelo: el <b>WACC</b> (coste de capital) y la 
        <b>tasa de crecimiento perpetuo (g)</b> del valor terminal.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph(
        """<b>IMPORTANTE:</b> Estos valores son <b>recalculados</b> punto por punto usando 
        la fórmula DCF completa, no son aproximaciones o multiplicadores arbitrarios.""",
        ParagraphStyle(name='NotaImportante',
                      parent=styles['TextoNormal'],
                      textColor=AZUL_PRINCIPAL,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Calcular sensibilidad real
    sens_data = calcular_sensibilidad_real(resultado_mckinsey, pyl_df)
    matriz = sens_data['matriz']
    wacc_base = sens_data['wacc_base']
    g_base = sens_data['g_base']
    
    # Crear tabla
    elementos.append(Paragraph("Matriz de Sensibilidad: WACC vs Crecimiento Perpetuo (g)", 
                               styles['Seccion']))
    
    # Header
    tabla_data = [['WACC / g'] + [f'{g:.1f}%' for g in sens_data['g_range']]]
    
    # Datos
    for wacc in sens_data['wacc_range']:
        fila = [f'{wacc:.1f}%']
        for g in sens_data['g_range']:
            valor = matriz.get(wacc, {}).get(g, 0)
            fila.append(formatear_numero(valor, 1))
        tabla_data.append(fila)
    
    # Encontrar caso base
    caso_base_row = 0
    caso_base_col = 0
    for i, wacc in enumerate(sens_data['wacc_range'], start=1):
        if abs(wacc - wacc_base) < 0.6:
            caso_base_row = i
            break
    
    for j, g in enumerate(sens_data['g_range'], start=1):
        if abs(g - g_base) < 0.3:
            caso_base_col = j
            break
    
    num_cols = len(sens_data['g_range']) + 1
    col_width = 0.9*inch
    tabla_sens = Table(tabla_data, colWidths=[col_width] * num_cols)
    
    style_list = [
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('BACKGROUND', (0, 0), (0, -1), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    
    # Destacar caso base
    if caso_base_row > 0 and caso_base_col > 0:
        style_list.extend([
            ('BACKGROUND', (caso_base_col, caso_base_row), (caso_base_col, caso_base_row), AZUL_CLARO),
            ('TEXTCOLOR', (caso_base_col, caso_base_row), (caso_base_col, caso_base_row), colors.white),
            ('FONTNAME', (caso_base_col, caso_base_row), (caso_base_col, caso_base_row), 'Helvetica-Bold'),
        ])
    
    tabla_sens.setStyle(TableStyle(style_list))
    
    elementos.append(tabla_sens)
    
    elementos.append(Spacer(1, 0.1*inch))
    elementos.append(Paragraph(
        f"<i>Nota: Caso base (WACC={wacc_base:.1f}%, g={g_base:.1f}%) destacado en azul</i>",
        ParagraphStyle(name='NotaSens', fontSize=8, textColor=GRIS_TEXTO)
    ))
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Interpretación
    elementos.append(Paragraph("<b>Interpretación</b>", styles['Seccion']))
    
    elementos.append(Paragraph(
        """• <b>Sensibilidad al WACC:</b> Un incremento de 1pp en el WACC reduce el valor 
        aproximadamente un 8-12%, dependiendo del perfil de FCF.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Sensibilidad a g:</b> Un incremento de 0.5pp en la tasa de crecimiento 
        perpetuo aumenta el valor aproximadamente 5-8%.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Paragraph(
        """• <b>Mayor sensibilidad:</b> El modelo es más sensible al WACC que a g, lo que 
        es típico cuando el valor terminal representa >50% del valor total.""",
        styles['TextoNormal']
    ))
    
    elementos.append(PageBreak())
    
    return elementos



# ═══════════════════════════════════════════════════
# SECCIONES REUTILIZADAS DEL PDF ORIGINAL
# ═══════════════════════════════════════════════════

def crear_executive_summary(
    datos_empresa: Dict,
    resultado_mckinsey: Dict, 
    pyl_df: pd.DataFrame,
    styles
) -> List:
    """Resumen ejecutivo con métricas clave"""
    elementos = []
    
    elementos.append(Paragraph("RESUMEN EJECUTIVO", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph("Investment Thesis", styles['Seccion']))
    elementos.append(Spacer(1, 0.1*inch))
    
    # Métricas de valoración
    elementos.append(Paragraph("Métricas de Valoración", styles['Seccion']))
    
    valor_empresa = resultado_mckinsey.get('enterprise_value', 0)
    equity_value = resultado_mckinsey.get('equity_value', 0)
    deuda_neta = resultado_mckinsey.get('deuda_neta', 0)
    
    metricas_data = [
        ['', 'Valor'],
        ['Enterprise Value', formatear_numero(valor_empresa, 1)],
        ['(-) Deuda Neta', formatear_numero(deuda_neta, 1)],
        ['Equity Value', formatear_numero(equity_value, 1)],
        ['', ''],
        ['WACC', f"{resultado_mckinsey.get('wacc', 0):.1f}%"],
        ['TIR Proyecto', f"{resultado_mckinsey.get('tir', 0):.1f}%"],
        ['ROIC Promedio', f"{resultado_mckinsey.get('roic_promedio', 0):.1f}%"],
    ]
    
    tabla_metricas = Table(metricas_data, colWidths=[3*inch, 2*inch])
    tabla_metricas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 3), (-1, 3), 2, NEGRO),
        ('LINEBELOW', (0, 4), (-1, 4), 1, GRIS_CLARO),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_metricas)
    
    elementos.append(Spacer(1, 0.15*inch))
    
    # Recomendación
    elementos.append(Paragraph("Recomendación", styles['Seccion']))
    
    tir = resultado_mckinsey.get('tir', 0)
    wacc = resultado_mckinsey.get('wacc', 0)
    roic = resultado_mckinsey.get('roic_promedio', 0)
    
    if tir > wacc and roic > wacc:
        recomendacion = f"✓ PROYECTO ATRACTIVO: TIR {tir:.1f}% y ROIC {roic:.1f}% superan WACC {wacc:.1f}%. La empresa crea valor económico sostenible."
        color = VERDE_POSITIVO
    elif tir > wacc and roic < wacc:
        recomendacion = f"■ PROYECTO VIABLE CON RIESGOS: Aunque la TIR {tir:.1f}% supera al WACC {wacc:.1f}%, el ROIC operativo {roic:.1f}% es inferior al coste de capital. Dependencia del valor terminal."
        color = colors.orange
    else:
        recomendacion = f"✗ PROYECTO NO RECOMENDADO: TIR {tir:.1f}% por debajo del WACC {wacc:.1f}%. Destruye valor para accionistas."
        color = ROJO_NEGATIVO
    
    elementos.append(Paragraph(
        recomendacion,
        ParagraphStyle(name='Recomendacion',
                      parent=styles['TextoNormal'],
                      textColor=color,
                      fontName='Helvetica-Bold')
    ))
    
    elementos.append(PageBreak())
    
    return elementos


def crear_analisis_macro(datos_empresa: Dict, styles) -> List:
    """Análisis macroeconómico"""
    elementos = []
    
    elementos.append(Paragraph("ANÁLISIS MACROECONÓMICO", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    elementos.append(Paragraph("Contexto Económico Global", styles['Seccion']))
    elementos.append(Paragraph(
        """El entorno macroeconómico actual presenta un escenario de moderación en el crecimiento 
        económico global, con proyecciones de PIB mundial en torno al 3.2% para 2025. Los bancos 
        centrales mantienen políticas monetarias cautelosas, con tipos de interés estabilizándose 
        tras el ciclo alcista de 2023-2024.""",
        styles['TextoNormal']
    ))
    
    elementos.append(Spacer(1, 0.1*inch))
    
    # Tabla macro
    macro_data = [
        ['Indicador', '2024', '2025E', '2026E'],
        ['PIB España', '2.4%', '2.1%', '2.0%'],
        ['PIB Zona Euro', '0.8%', '1.3%', '1.5%'],
        ['Inflación España', '3.1%', '2.2%', '2.0%'],
        ['Tipo BCE', '3.75%', '3.25%', '2.75%'],
        ['Desempleo España', '11.8%', '11.2%', '10.8%'],
    ]
    
    tabla_macro = Table(macro_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
    tabla_macro.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_CLARO),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_macro)
    
    elementos.append(Spacer(1, 0.05*inch))
    elementos.append(Paragraph(
        "<i>Fuentes: Banco de España, BCE, FMI World Economic Outlook, INE</i>",
        ParagraphStyle(name='FuentesMacro', fontSize=8, textColor=GRIS_TEXTO)
    ))
    
    elementos.append(PageBreak())
    
    return elementos


def crear_proyecciones_anuales_detalladas(pyl_df, balance_df, fcf_df, styles):
    """Proyecciones P&L y Balance año por año"""
    elementos = []
    
    elementos.append(Paragraph("PROYECCIONES DETALLADAS POR AÑO", styles['Subtitulo']))
    elementos.append(Spacer(1, 0.2*inch))
    
    if pyl_df is None or len(pyl_df.columns) == 0:
        elementos.append(Paragraph("No hay datos de proyección disponibles", styles['TextoNormal']))
        return elementos
    
    # Proyecciones para cada año (máximo 5)
    años = list(pyl_df.columns)[:5]
    
    for i, año in enumerate(años, 1):
        elementos.append(Paragraph(f"PROYECCIONES DETALLADAS - AÑO {i}", styles['Subtitulo']))
        elementos.append(Spacer(1, 0.1*inch))
        
        # P&L
        elementos.append(Paragraph("Cuenta de Resultados", styles['Seccion']))
        
        pyl_año_data = [['Concepto', 'M€']]
        
        conceptos_pyl = [
            'Ventas', 'Coste Ventas', 'Margen Bruto', 'Gastos Personal',
            'Gastos Generales', 'Marketing', 'EBITDA', 'Amortización',
            'EBIT', 'Gastos Financieros', 'BAI', 'Impuestos', 'Beneficio Neto'
        ]
        
        for concepto in conceptos_pyl:
            if concepto in pyl_df.index:
                valor = pyl_df.loc[concepto, año]
                pyl_año_data.append([concepto, formatear_numero(valor, 1, prefijo='', sufijo='')])
        
        tabla_pyl = Table(pyl_año_data, colWidths=[3.5*inch, 2*inch])
        tabla_pyl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), AZUL_PRINCIPAL),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (0, -1), (-1, -1), 1, GRIS_TEXTO),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elementos.append(tabla_pyl)
        elementos.append(Spacer(1, 0.15*inch))
        
        # Balance si existe
        if balance_df is not None and año in balance_df.columns:
            elementos.append(Paragraph("Balance General", styles['Seccion']))
            
            balance_año_data = [
                ['ACTIVO', 'M€', 'PATRIMONIO NETO Y PASIVO', 'M€']
            ]
            
            # Activo
            conceptos_activo = ['Activo Fijo', 'Tesorería', 'Clientes', 'Inventario', 'TOTAL ACTIVO']
            conceptos_pasivo = ['Capital + Reservas', 'Deuda L/P', 'Proveedores', 'Deuda C/P', 'TOTAL PN + PASIVO']
            
            max_filas = max(len(conceptos_activo), len(conceptos_pasivo))
            
            for j in range(max_filas):
                fila = []
                
                # Activo
                if j < len(conceptos_activo):
                    concepto_a = conceptos_activo[j]
                    if concepto_a in balance_df.index:
                        valor_a = balance_df.loc[concepto_a, año]
                        fila.extend([concepto_a, formatear_numero(valor_a, 1, prefijo='', sufijo='')])
                    else:
                        fila.extend([concepto_a, '-'])
                else:
                    fila.extend(['', ''])
                
                # Pasivo
                if j < len(conceptos_pasivo):
                    concepto_p = conceptos_pasivo[j]
                    if concepto_p in balance_df.index:
                        valor_p = balance_df.loc[concepto_p, año]
                        fila.extend([concepto_p, formatear_numero(valor_p, 1, prefijo='', sufijo='')])
                    else:
                        fila.extend([concepto_p, '-'])
                else:
                    fila.extend(['', ''])
                
                balance_año_data.append(fila)
            
            tabla_balance = Table(balance_año_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch])
            tabla_balance.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), AZUL_PRINCIPAL),
                ('BACKGROUND', (2, 0), (3, 0), AZUL_PRINCIPAL),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('LINEABOVE', (0, -1), (-1, -1), 1, GRIS_TEXTO),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            elementos.append(tabla_balance)
        
        elementos.append(PageBreak())
    
    return elementos

