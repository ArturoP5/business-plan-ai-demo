#!/usr/bin/env python3
"""
Generador de PDF con Análisis de IA
Versión 2.0 - Diseñado desde cero para análisis profundo
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, KeepTogether, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import pandas as pd
from typing import Dict, Any, List

class PDFIAGenerator:
    """
    Generador de PDF profesional con análisis de IA integrado
    """
    
    def __init__(self):
        self.buffer = BytesIO()
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _sanitize_text(self, text: str) -> str:
        """Sanitiza texto de IA para prevenir errores de HTML"""
        if not text:
            return ""
        import re
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return text
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        
        # Función helper para agregar estilos sin duplicar
        def add_style_safe(style):
            if style.name not in self.styles:
                self.styles.add(style)
        
        # Título principal
        add_style_safe(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        add_style_safe(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Encabezado de sección
        add_style_safe(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5
        ))
        
        # Subsección
        add_style_safe(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal mejorado
        add_style_safe(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Texto para tablas
        add_style_safe(ParagraphStyle(
            name='TableText',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11
        ))
        
        # Destacado/Insight
        add_style_safe(ParagraphStyle(
            name='Insight',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2980b9'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=10,
            backColor=colors.HexColor('#ecf0f1')
        ))
    
    def _crear_portada(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> List:
        """Crea la página de portada del informe"""
        elementos = []
        
        # Espaciado superior
        elementos.append(Spacer(1, 2*cm))
        
        # Título principal
        titulo = Paragraph(
            "INFORME DE ANÁLISIS ESTRATÉGICO<br/>Y VALORACIÓN",
            self.styles['CustomTitle']
        )
        elementos.append(titulo)
        elementos.append(Spacer(1, 1*cm))
        
        # Nombre de la empresa
        info_basica = datos['info_basica']
        empresa = Paragraph(
            f"<b>{info_basica['nombre_empresa']}</b>",
            self.styles['CustomTitle']
        )
        elementos.append(empresa)
        
        # Sector
        sector = Paragraph(
            f"Sector: {info_basica['sector']}",
            self.styles['CustomSubtitle']
        )
        elementos.append(sector)
        elementos.append(Spacer(1, 2*cm))
        
        # Métricas clave en portada
        metricas = datos['metricas_valoracion']
        
        data_metricas = [
            ['VALORACIÓN EMPRESA', f"€{metricas['enterprise_value']:,.0f}"],
            ['TIR Proyecto', f"{metricas['tir']:.1f}%"],
            ['WACC', f"{metricas['wacc']:.1f}%"],
            ['ROIC Promedio', f"{metricas['roic_promedio']:.1f}%"]
        ]
        
        tabla_metricas = Table(data_metricas, colWidths=[8*cm, 6*cm])
        tabla_metricas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elementos.append(tabla_metricas)
        elementos.append(Spacer(1, 2*cm))
        
        # Fecha y modelo IA
        fecha_texto = Paragraph(
            f"Fecha: {info_basica['fecha_informe']}<br/>"
            f"Generado por IA: {analisis.get('modelo_ia', 'N/A').upper()}",
            self.styles['CustomSubtitle']
        )
        elementos.append(fecha_texto)
        
        # Disclaimer
        elementos.append(Spacer(1, 3*cm))
        disclaimer = Paragraph(
            "<i>Este informe ha sido generado con fines informativos. "
            "Las proyecciones y valoraciones se basan en supuestos que pueden no materializarse. "
            "Se recomienda realizar due diligence adicional antes de tomar decisiones de inversión.</i>",
            self.styles['Normal']
        )
        elementos.append(disclaimer)
        
        elementos.append(PageBreak())
        
        return elementos
    
    def generar_pdf(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> BytesIO:
        """
        Genera el PDF completo
        
        Args:
            datos: Datos completos de data_collector
            analisis: Análisis generado por ai_analyzer_v2
            
        Returns:
            BytesIO con el PDF generado
        """
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elementos = []
        
        # 1. Portada
        elementos.extend(self._crear_portada(datos, analisis))
        
        # 2. Executive Summary
        elementos.extend(self._crear_executive_summary(datos, analisis))
        
        # 3. Análisis Macro y Sectorial
        elementos.extend(self._crear_macro_sectorial(datos, analisis))
        
        # 4. Company Overview
        elementos.extend(self._crear_company_overview(datos))
        
        # 5. SWOT
        elementos.extend(self._crear_swot(analisis))
        
        # 6. Análisis Financiero
        elementos.extend(self._crear_analisis_financiero(datos, analisis))
        
        # 7. Valoración
        elementos.extend(self._crear_valoracion(datos))
        
        # 8. Riesgos
        elementos.extend(self._crear_riesgos(analisis))
        
        # 9. Recomendaciones
        elementos.extend(self._crear_recomendaciones(datos, analisis))
        
        # Construir PDF
        doc.build(elementos)
        
        # Retornar buffer
        self.buffer.seek(0)
        return self.buffer


# Función de conveniencia
    def _crear_executive_summary(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> List:
        """Crea la sección de Executive Summary"""
        elementos = []
        
        elementos.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        exec_sum = analisis.get('executive_summary', {})
        
        # Investment Thesis
        elementos.append(Paragraph("Investment Thesis", self.styles['SubsectionHeader']))
        
        thesis = exec_sum.get('investment_thesis', 'Análisis no disponible')
        elementos.append(Paragraph(self._sanitize_text(thesis), self.styles['BodyText']))
        elementos.append(Spacer(1, 0.5*cm))
        
        # Tabla de métricas clave
        elementos.append(Paragraph("Métricas Clave", self.styles['SubsectionHeader']))
        
        metricas = datos['metricas_valoracion']
        
        data_metricas = [
            ['MÉTRICA', 'VALOR'],
            ['Valor Empresa (DCF)', f"€{metricas['enterprise_value']:,.0f}"],
            ['Valor Equity', f"€{metricas['equity_value']:,.0f}"],
            ['WACC', f"{metricas['wacc']:.1f}%"],
            ['TIR Proyecto', f"{metricas['tir']:.1f}%"],
            ['ROIC Promedio', f"{metricas['roic_promedio']:.1f}%"],
            ['Deuda Neta', f"€{metricas['deuda_neta']:,.0f}"]
        ]
        
        tabla = Table(data_metricas, colWidths=[10*cm, 6*cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Recomendación final
        elementos.append(Paragraph("Recomendación", self.styles['SubsectionHeader']))
        
        recomendacion = exec_sum.get('recomendacion', 'N/A')
        rating = exec_sum.get('rating', 'N/A')
        
        # Color según recomendación
        if 'PROCEDER' in recomendacion:
            color_rec = colors.green
        elif 'REVISAR' in recomendacion:
            color_rec = colors.orange
        else:
            color_rec = colors.red
        
        data_rec = [
            [Paragraph(f"<b>{recomendacion}</b>", self.styles['TableText']), 
             Paragraph(f"<b>Rating: {rating}</b>", self.styles['TableText'])]
        ]
        
        tabla_rec = Table(data_rec, colWidths=[10*cm, 6*cm])
        tabla_rec.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_rec),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elementos.append(tabla_rec)
        elementos.append(Spacer(1, 0.3*cm))
        
        # Síntesis
        sintesis = exec_sum.get('sintesis_una_linea', '')
        if sintesis:
            elementos.append(Paragraph(f"<i>{sintesis}</i>", self.styles['Insight']))
        
        elementos.append(PageBreak())
        
        return elementos


    def _crear_macro_sectorial(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> List:
        """Crea la sección de Análisis Macroeconómico y Sectorial"""
        elementos = []
        
        elementos.append(Paragraph("ANÁLISIS MACROECONÓMICO Y SECTORIAL", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        macro = analisis.get('macro_sectorial', {})
        
        # Contexto Macroeconómico
        elementos.append(Paragraph("Contexto Macroeconómico", self.styles['SubsectionHeader']))
        contexto = macro.get('contexto_macro', 'Análisis no disponible')
        elementos.append(Paragraph(self._sanitize_text(contexto), self.styles['BodyText']))
        elementos.append(Spacer(1, 0.5*cm))
        
        # Análisis Sectorial
        elementos.append(Paragraph("Análisis Sectorial", self.styles['SubsectionHeader']))
        analisis_sect = macro.get('analisis_sectorial', 'Análisis no disponible')
        elementos.append(Paragraph(self._sanitize_text(analisis_sect), self.styles['BodyText']))
        elementos.append(Spacer(1, 0.5*cm))
        
        # Métricas sectoriales en tabla
        data_sector = [
            ['MÉTRICA SECTORIAL', 'VALOR'],
            ['Tamaño Mercado Estimado', macro.get('tamano_mercado_estimado', 'N/A')],
            ['CAGR Sectorial', macro.get('cagr_sectorial', 'N/A')],
            ['Perspectiva', macro.get('perspectiva_sector', 'N/A')]
        ]
        
        tabla_sector = Table(data_sector, colWidths=[10*cm, 6*cm])
        tabla_sector.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elementos.append(tabla_sector)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Posicionamiento vs Sector
        posicionamiento = macro.get('posicionamiento_vs_sector', '')
        if posicionamiento:
            elementos.append(Paragraph("Posicionamiento Competitivo", self.styles['SubsectionHeader']))
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(Paragraph(self._sanitize_text(posicionamiento), self.styles['Insight']))
        
        elementos.append(PageBreak())
        
        return elementos


    def _crear_company_overview(self, datos: Dict[str, Any]) -> List:
        """Crea la sección de Company Overview"""
        elementos = []
        
        elementos.append(Paragraph("COMPANY OVERVIEW", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        desc = datos['descripcion_negocio']
        info = datos['info_basica']
        vision = datos.get('vision_estrategica', {})
        
        # 1. Descripción del Negocio
        elementos.append(Paragraph("Descripción del Negocio", self.styles['SubsectionHeader']))
        
        # Descripción de la Actividad
        descripcion = desc.get('descripcion_actividad', 'N/A')
        elementos.append(Paragraph(f"<b>Descripción de la Actividad:</b> {descripcion}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Productos/Servicios Principales
        productos = desc.get('productos_servicios', 'N/A')
        elementos.append(Paragraph(f"<b>Productos/Servicios Principales:</b> {productos}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.4*cm))
        
        # 2. Información Estratégica
        elementos.append(Paragraph("Información Estratégica", self.styles['SubsectionHeader']))
        
        # Modelo de Negocio
        modelo = desc.get('modelo_negocio', 'N/A')
        elementos.append(Paragraph(f"<b>Modelo de Negocio:</b> {modelo}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Posicionamiento de Precio
        precio = desc.get('posicionamiento_precio', 'N/A')
        elementos.append(Paragraph(f"<b>Posicionamiento de Precio:</b> {precio}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Top 3 Competidores Principales
        competidores = desc.get('competidores_principales', 'N/A')
        elementos.append(Paragraph(f"<b>Top 3 Competidores Principales:</b> {competidores}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Visión Estratégica (con subapartados)
        if vision and vision.get('corto_plazo', 'N/A') != 'N/A':
            elementos.append(Paragraph("<b>Visión Estratégica:</b>", self.styles['BodyText']))
            elementos.append(Spacer(1, 0.1*cm))
            
            if vision.get('corto_plazo', 'N/A') != 'N/A':
                elementos.append(Paragraph(f"• <b>Objetivos a Corto Plazo:</b> {vision.get('corto_plazo', 'N/A')}", self.styles['BodyText']))
                elementos.append(Spacer(1, 0.1*cm))
            
            if vision.get('medio_plazo', 'N/A') != 'N/A':
                elementos.append(Paragraph(f"• <b>Objetivos a Medio Plazo:</b> {vision.get('medio_plazo', 'N/A')}", self.styles['BodyText']))
                elementos.append(Spacer(1, 0.1*cm))
            
            if vision.get('largo_plazo', 'N/A') != 'N/A':
                elementos.append(Paragraph(f"• <b>Visión a Largo Plazo:</b> {vision.get('largo_plazo', 'N/A')}", self.styles['BodyText']))
                elementos.append(Spacer(1, 0.2*cm))
        
        # Ventaja Competitiva Principal
        ventaja = desc.get('ventaja_competitiva_clave', 'N/A')
        elementos.append(Paragraph(f"<b>Ventaja Competitiva Principal:</b> {ventaja}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Principales Riesgos del Negocio
        riesgos = desc.get('principales_riesgos', 'N/A')
        elementos.append(Paragraph(f"<b>Principales Riesgos del Negocio:</b> {riesgos}", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Cuota de Mercado
        cuota = desc.get('cuota_mercado', 'N/A')
        elementos.append(Paragraph(f"<b>Cuota de Mercado (%):</b> {cuota}%", self.styles['BodyText']))
        elementos.append(Spacer(1, 0.2*cm))
        
        # Clientes Objetivo
        clientes = desc.get('clientes_objetivo', 'N/A')
        elementos.append(Paragraph(f"<b>Clientes Objetivo:</b> {clientes}", self.styles['BodyText']))
        
        elementos.append(PageBreak())
        
        return elementos


    def _crear_swot(self, analisis: Dict[str, Any]) -> List:
        """Crea la sección de Análisis SWOT"""
        elementos = []
        
        elementos.append(Paragraph("ANÁLISIS ESTRATÉGICO - SWOT", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        swot = analisis.get('swot', {})
        
        # Crear tabla SWOT 2x2
        fortalezas = swot.get('fortalezas', [])
        debilidades = swot.get('debilidades', [])
        oportunidades = swot.get('oportunidades', [])
        amenazas = swot.get('amenazas', [])
        
        # Formatear listas con bullets
        def formatear_lista(items, color_fondo):
            texto = ""
            for item in items[:3]:  # Máximo 3 items
                texto += f"• {item}<br/>"
            return Paragraph(texto, ParagraphStyle(
                'ListStyle',
                parent=self.styles['Normal'],
                fontSize=8,
                leading=10,
                backColor=color_fondo
            ))
        
        # Construir tabla SWOT
        data_swot = [
            [
                Paragraph("<b>FORTALEZAS</b>", self.styles['TableText']),
                Paragraph("<b>DEBILIDADES</b>", self.styles['TableText'])
            ],
            [
                formatear_lista(fortalezas, colors.HexColor('#d4edda')),
                formatear_lista(debilidades, colors.HexColor('#f8d7da'))
            ],
            [
                Paragraph("<b>OPORTUNIDADES</b>", self.styles['TableText']),
                Paragraph("<b>AMENAZAS</b>", self.styles['TableText'])
            ],
            [
                formatear_lista(oportunidades, colors.HexColor('#d1ecf1')),
                formatear_lista(amenazas, colors.HexColor('#fff3cd'))
            ]
        ]
        
        tabla_swot = Table(data_swot, colWidths=[8*cm, 8*cm])
        tabla_swot.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#28a745')),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#dc3545')),
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#17a2b8')),
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#ffc107')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elementos.append(tabla_swot)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Síntesis estratégica
        sintesis = swot.get('sintesis_estrategica', '')
        if sintesis:
            elementos.append(Paragraph("Síntesis Estratégica", self.styles['SubsectionHeader']))
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(Paragraph(self._sanitize_text(sintesis), self.styles['Insight']))
        
        elementos.append(PageBreak())
        
        return elementos


    def _crear_analisis_financiero(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> List:
        """Crea la sección de Análisis Financiero completo"""
        elementos = []
        
        elementos.append(Paragraph("ANÁLISIS FINANCIERO DETALLADO", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        # Proyecciones P&L
        elementos.append(Paragraph("Proyecciones Financieras (P&L)", self.styles['SubsectionHeader']))
        
        pyl_data = datos['datos_financieros'].get('pyl')
        if pyl_data and len(pyl_data) > 0:
            # Crear tabla P&L resumida (primero y último año)
            cols_importantes = ['Año', 'Ventas', 'EBITDA', 'Margen EBITDA', 'EBIT', 'Beneficio Neto']
            
            # Preparar datos
            df_pyl = pd.DataFrame(pyl_data)
            
            # Tomar año 1 y año 5
            if len(df_pyl) >= 5:
                rows = [df_pyl.iloc[0], df_pyl.iloc[4]]
            else:
                rows = [df_pyl.iloc[0], df_pyl.iloc[-1]]
            
            data_pyl = [['CONCEPTO', 'AÑO 1', 'AÑO 5', 'VARIACIÓN']]
            
            # Helper para obtener valores de forma robusta
            def get_val(row, *keys):
                for key in keys:
                    if key in row and row[key] is not None:
                        return float(row[key])
                return 0
            
            # Ventas
            v1 = get_val(rows[0], 'Ventas')
            v5 = get_val(rows[1], 'Ventas')
            var_ventas = ((v5/v1 - 1) * 100) if v1 > 0 else 0
            data_pyl.append(['Ventas', f"€{v1:,.0f}", f"€{v5:,.0f}", f"{var_ventas:+.1f}%"])
            
            # EBITDA
            e1 = get_val(rows[0], 'EBITDA')
            e5 = get_val(rows[1], 'EBITDA')
            var_ebitda = ((e5/e1 - 1) * 100) if e1 > 0 else 0
            data_pyl.append(['EBITDA', f"€{e1:,.0f}", f"€{e5:,.0f}", f"{var_ebitda:+.1f}%"])
            
            # Margen EBITDA
            # Calcular Margen EBITDA: (EBITDA / Ventas) * 100
            m1 = (e1 / v1 * 100) if v1 > 0 else 0
            m5 = (e5 / v5 * 100) if v5 > 0 else 0
            data_pyl.append(['Margen EBITDA', f"{m1:.1f}%", f"{m5:.1f}%", f"{m5-m1:+.1f}pp"])
            
            # Beneficio Neto
            bn1 = get_val(rows[0], 'Beneficio Neto')
            bn5 = get_val(rows[1], 'Beneficio Neto')
            var_bn = ((bn5/bn1 - 1) * 100) if bn1 > 0 else 0
            data_pyl.append(['Beneficio Neto', f"€{bn1:,.0f}", f"€{bn5:,.0f}", f"{var_bn:+.1f}%"])
            
            tabla_pyl = Table(data_pyl, colWidths=[6*cm, 3*cm, 3*cm, 4*cm])
            tabla_pyl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elementos.append(tabla_pyl)
        
        elementos.append(Spacer(1, 0.5*cm))
        
        # KPIs Financieros Detallados con análisis de IA
        elementos.append(Paragraph("KPIs Financieros Clave - Análisis Detallado", self.styles['SubsectionHeader']))
        elementos.append(Spacer(1, 0.3*cm))
        
        kpis_detalle = analisis.get('kpis_detalle', {})
        kpis = datos['kpis_financieros']
        
        # Para cada KPI importante, crear un bloque
        kpis_importantes = ['roic', 'margen_ebitda', 'cash_conversion_cycle', 'deuda_neta_ebitda', 'cagr_ventas']
        
        for kpi_key in kpis_importantes:
            if kpi_key in kpis_detalle:
                kpi_analisis = kpis_detalle[kpi_key]
                
                # Nombre del KPI
                nombres_kpis = {
                    'roic': 'ROIC (Return on Invested Capital)',
                    'margen_ebitda': 'Margen EBITDA',
                    'cash_conversion_cycle': 'Cash Conversion Cycle',
                    'deuda_neta_ebitda': 'Deuda Neta / EBITDA',
                    'cagr_ventas': 'CAGR Ventas'
                }
                
                nombre_kpi = nombres_kpis.get(kpi_key, kpi_key)
                
                # Valor actual
                if kpi_key == 'roic':
                    valor = f"{kpis['roic']:.1f}%"
                elif kpi_key == 'margen_ebitda':
                    valor = f"{kpis['margen_ebitda_year1']:.1f}% → {kpis['margen_ebitda_year5']:.1f}%"
                elif kpi_key == 'cash_conversion_cycle':
                    valor = f"{kpis['cash_conversion_cycle']:.0f} días"
                elif kpi_key == 'deuda_neta_ebitda':
                    valor = f"{kpis['deuda_neta_ebitda']:.1f}x"
                elif kpi_key == 'cagr_ventas':
                    valor = f"{kpis['cagr_ventas']:.1f}%"
                else:
                    valor = "N/A"
                
                # Crear bloque del KPI
                elementos.append(Paragraph(f"<b>{nombre_kpi}: {valor}</b>", self.styles['BodyText']))
                
                # Interpretación
                interpretacion = kpi_analisis.get('interpretacion', '')
                if interpretacion:
                    elementos.append(Paragraph(f"<i>Interpretación:</i> {interpretacion}", self.styles['Normal']))
                
                # Benchmark
                benchmark = kpi_analisis.get('benchmark', '')
                if benchmark:
                    elementos.append(Paragraph(f"<i>Benchmark:</i> {benchmark}", self.styles['Normal']))
                
                # Cómo mejorar
                mejoras = kpi_analisis.get('como_mejorar', [])
                if mejoras:
                    texto_mejoras = "<i>Cómo mejorar:</i><br/>"
                    for mejora in mejoras[:3]:
                        texto_mejoras += f"• {mejora}<br/>"
                    elementos.append(Paragraph(texto_mejoras, self.styles['Normal']))
                
                elementos.append(Spacer(1, 0.4*cm))
        
        # Síntesis financiera
        sintesis_fin = kpis_detalle.get('sintesis_financiera', '')
        if sintesis_fin:
            elementos.append(Paragraph("Síntesis de Salud Financiera", self.styles['SubsectionHeader']))
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(Paragraph(self._sanitize_text(sintesis_fin), self.styles['Insight']))
        
        elementos.append(PageBreak())
        
        return elementos


    def _crear_valoracion(self, datos: Dict[str, Any]) -> List:
        """Crea la sección de Valoración"""
        elementos = []
        
        elementos.append(Paragraph("VALORACIÓN", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        metricas = datos['metricas_valoracion']
        
        # DCF Overview
        elementos.append(Paragraph("Discounted Cash Flow (DCF)", self.styles['SubsectionHeader']))
        
        data_dcf = [
            ['COMPONENTE', 'VALOR'],
            ['FCF 5 años (VP)', f"€{metricas['fcf_5anos']:,.0f}"],
            ['Valor Terminal', f"€{metricas['valor_terminal']:,.0f}"],
            ['Enterprise Value', f"€{metricas['enterprise_value']:,.0f}"],
            ['(-) Deuda Neta', f"€{metricas['deuda_neta']:,.0f}"],
            ['Equity Value', f"€{metricas['equity_value']:,.0f}"]
        ]
        
        tabla_dcf = Table(data_dcf, colWidths=[10*cm, 6*cm])
        tabla_dcf.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEABOVE', (0, -2), (-1, -2), 2, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elementos.append(tabla_dcf)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Parámetros clave
        elementos.append(Paragraph("Parámetros Clave", self.styles['SubsectionHeader']))
        
        data_params = [
            ['PARÁMETRO', 'VALOR'],
            ['WACC', f"{metricas['wacc']:.1f}%"],
            ['TIR', f"{metricas['tir']:.1f}%"],
            ['ROIC Promedio', f"{metricas['roic_promedio']:.1f}%"],
            ['Tasa Crecimiento Perpetuo (g)', f"{metricas['tasa_crecimiento_perpetuo']:.1f}%"]
        ]
        
        tabla_params = Table(data_params, colWidths=[10*cm, 6*cm])
        tabla_params.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elementos.append(tabla_params)
        
        # Interpretación TIR vs WACC
        tir = metricas['tir']
        wacc = metricas['wacc']
        roic = metricas['roic_promedio']
        
        if tir >= wacc:
            mensaje = f"✓ La TIR ({tir:.1f}%) supera al WACC ({wacc:.1f}%), indicando creación de valor para los accionistas."
            color_msg = colors.HexColor('#d4edda')
        else:
            if roic > wacc:
                mensaje = f"⚠ PARADOJA: TIR ({tir:.1f}%) < WACC ({wacc:.1f}%) pero ROIC ({roic:.1f}%) > WACC. Eficiencia operativa confirmada, pero falta escala para rentabilidad del proyecto."
                color_msg = colors.HexColor('#fff3cd')
            else:
                mensaje = f"✗ TIR ({tir:.1f}%) inferior al WACC ({wacc:.1f}%). El proyecto no genera valor suficiente."
                color_msg = colors.HexColor('#f8d7da')
        
        elementos.append(Spacer(1, 0.5*cm))
        elementos.append(Paragraph(mensaje, ParagraphStyle(
            'InterpretacionValor',
            parent=self.styles['Normal'],
            fontSize=10,
            backColor=color_msg,
            borderWidth=1,
            borderColor=colors.grey,
            borderPadding=10,
            spaceAfter=10
        )))
        
        elementos.append(PageBreak())
        
        return elementos
    
    def _crear_riesgos(self, analisis: Dict[str, Any]) -> List:
        """Crea la sección de Análisis de Riesgos"""
        elementos = []
        
        elementos.append(Paragraph("ANÁLISIS DE RIESGOS", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        riesgos_data = analisis.get('riesgos', {})
        riesgos_lista = riesgos_data.get('riesgos', [])
        
        if riesgos_lista:
            # Crear tabla de riesgos
            data_riesgos = [['RIESGO', 'PROB.', 'IMPACTO', 'MITIGACIÓN']]
            
            for riesgo in riesgos_lista[:6]:  # Máximo 6 riesgos
                nombre = riesgo.get('nombre', 'N/A')
                prob = riesgo.get('probabilidad', 'N/A')
                impacto = riesgo.get('impacto', 'N/A')
                
                # Mitigaciones (hasta 2)
                mitigaciones = riesgo.get('mitigacion', [])
                texto_mit = ""
                for mit in mitigaciones[:2]:
                    texto_mit += f"• {mit}\n"
                
                data_riesgos.append([
                    Paragraph(f"<b>{nombre}</b><br/>{riesgo.get('descripcion', '')[:100]}...", self.styles['TableText']),
                    prob,
                    impacto,
                    Paragraph(texto_mit, self.styles['TableText'])
                ])
            
            tabla_riesgos = Table(data_riesgos, colWidths=[5*cm, 2*cm, 2*cm, 7*cm])
            tabla_riesgos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c0392b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (2, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elementos.append(tabla_riesgos)
        
        # Nivel de riesgo global
        nivel_global = riesgos_data.get('nivel_riesgo_global', 'N/A')
        riesgo_principal = riesgos_data.get('riesgo_principal', 'N/A')
        
        elementos.append(Spacer(1, 0.5*cm))
        elementos.append(Paragraph(f"<b>Nivel de Riesgo Global:</b> {nivel_global}", self.styles['BodyText']))
        elementos.append(Paragraph(f"<b>Riesgo Principal Identificado:</b> {riesgo_principal}", self.styles['Insight']))
        
        elementos.append(PageBreak())
        
        return elementos
    
    def _crear_recomendaciones(self, datos: Dict[str, Any], analisis: Dict[str, Any]) -> List:
        """Crea la sección de Recomendaciones Estratégicas"""
        elementos = []
        
        elementos.append(Paragraph("RECOMENDACIONES ESTRATÉGICAS", self.styles['SectionHeader']))
        elementos.append(Spacer(1, 0.5*cm))
        
        recom = analisis.get('recomendaciones', {})
        vision = datos['vision_estrategica']
        
        # Quick Wins
        elementos.append(Paragraph("Quick Wins (0-6 meses)", self.styles['SubsectionHeader']))
        elementos.append(Spacer(1, 0.2*cm))
        
        quick_wins = recom.get('quick_wins', [])
        for i, qw in enumerate(quick_wins[:3], 1):
            titulo = qw.get('titulo', 'N/A')
            desc = qw.get('descripcion', '')
            impacto = qw.get('impacto_esperado', '')
            
            elementos.append(Paragraph(f"<b>{i}. {titulo}</b>", self.styles['BodyText']))
            elementos.append(Paragraph(desc, self.styles['Normal']))
            if impacto:
                elementos.append(Paragraph(f"<i>Impacto esperado: {impacto}</i>", self.styles['Normal']))
            elementos.append(Spacer(1, 0.3*cm))
        
        # Medio Plazo
        elementos.append(Paragraph("Iniciativas Medio Plazo (6-24 meses)", self.styles['SubsectionHeader']))
        elementos.append(Spacer(1, 0.2*cm))
        
        medio_plazo = recom.get('medio_plazo', [])
        for i, mp in enumerate(medio_plazo[:3], 1):
            titulo = mp.get('titulo', 'N/A')
            desc = mp.get('descripcion', '')
            
            elementos.append(Paragraph(f"<b>{i}. {titulo}</b>", self.styles['BodyText']))
            elementos.append(Paragraph(desc, self.styles['Normal']))
            elementos.append(Spacer(1, 0.3*cm))
        
        # Largo Plazo
        elementos.append(Paragraph("Visión Largo Plazo (2-5 años)", self.styles['SubsectionHeader']))
        elementos.append(Spacer(1, 0.2*cm))
        
        largo_plazo = recom.get('largo_plazo', [])
        for i, lp in enumerate(largo_plazo[:2], 1):
            titulo = lp.get('titulo', 'N/A')
            desc = lp.get('descripcion', '')
            
            elementos.append(Paragraph(f"<b>{i}. {titulo}</b>", self.styles['BodyText']))
            elementos.append(Paragraph(desc, self.styles['Normal']))
            elementos.append(Spacer(1, 0.3*cm))
        
        # Prioridad #1
        prioridad_1 = recom.get('prioridad_1', '')
        if prioridad_1:
            elementos.append(Spacer(1, 0.7*cm))
            elementos.append(Paragraph("Iniciativa Prioritaria #1", self.styles['SubsectionHeader']))
            elementos.append(Paragraph(self._sanitize_text(prioridad_1), self.styles['Insight']))
        
        # Roadmap estratégico
        roadmap = recom.get('roadmap_estrategico', '')
        if roadmap:
            elementos.append(Spacer(1, 0.5*cm))
            elementos.append(Paragraph("Roadmap Estratégico Integrado", self.styles['SubsectionHeader']))
            elementos.append(Paragraph(self._sanitize_text(roadmap), self.styles['BodyText']))
        
        elementos.append(PageBreak())
        
        return elementos

def generar_pdf_con_ia(datos: Dict[str, Any], analisis: Dict[str, Any]) -> BytesIO:
    """
    Función de conveniencia para generar PDF
    
    Args:
        datos: Datos completos de data_collector
        analisis: Análisis de ai_analyzer_v2
        
    Returns:
        BytesIO con PDF generado
    """
    generator = PDFIAGenerator()
    return generator.generar_pdf(datos, analisis)


