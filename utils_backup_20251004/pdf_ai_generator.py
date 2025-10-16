"""
Generador de PDF con Análisis de IA
Versión completa con análisis financiero profundo
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Image
import streamlit as st
from datetime import datetime
import os
from io import BytesIO
import json

class PDFAIGenerator:
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Define estilos personalizados para el PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceBefore=20,
            spaceAfter=12,
            bold=True
        ))
        
    def generate_pdf_with_ai(self, datos, ai_analysis=None):
        """
        Genera PDF con análisis de IA integrado
        
        Args:
            datos: Diccionario con todos los datos de la empresa
            ai_analysis: Diccionario con los análisis generados por IA
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Portada
        story.extend(self._create_cover_page(datos))
        story.append(PageBreak())
        
        # Resumen Ejecutivo con IA
        if ai_analysis and 'investment_thesis' in ai_analysis:
            story.extend(self._create_executive_summary_ai(datos, ai_analysis['investment_thesis']))
            story.append(PageBreak())
        
        # Análisis SWOT con IA
        if ai_analysis and 'swot' in ai_analysis:
            story.extend(self._create_swot_ai(ai_analysis['swot']))
            story.append(PageBreak())
        
        # Análisis Financiero con IA
        if ai_analysis and 'financial_analysis' in ai_analysis:
            story.extend(self._create_financial_analysis_ai(datos, ai_analysis['financial_analysis']))
            story.append(PageBreak())
        
        # Proyecciones con comentarios de IA
        if ai_analysis and 'projections_analysis' in ai_analysis:
            story.extend(self._create_projections_ai(datos, ai_analysis['projections_analysis']))
            story.append(PageBreak())
        
        # Recomendaciones Estratégicas
        if ai_analysis and 'recommendations' in ai_analysis:
            story.extend(self._create_recommendations_ai(ai_analysis['recommendations']))
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_cover_page(self, datos):
        """Crea la portada del informe"""
        elements = []
        
        # Título principal
        title = Paragraph("INFORME DE ANÁLISIS EMPRESARIAL CON IA", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Información de la empresa
        company_name = datos.get('nombre_empresa', 'Empresa')
        subtitle = Paragraph(f"<b>{company_name}</b>", self.styles['Title'])
        elements.append(subtitle)
        elements.append(Spacer(1, 30))
        
        # Fecha
        fecha = datetime.now().strftime("%B %Y")
        date_para = Paragraph(f"<b>Fecha:</b> {fecha}", self.styles['Normal'])
        elements.append(date_para)
        
        return elements
    
    def _create_swot_ai(self, swot_data):
        """Crea la sección SWOT con datos de IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS SWOT - GENERADO POR IA", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Crear tabla SWOT 2x2
        data = [
            [Paragraph("<b>FORTALEZAS</b>", self.styles['Normal']),
             Paragraph("<b>DEBILIDADES</b>", self.styles['Normal'])],
            [self._format_list(swot_data.get('fortalezas', [])),
             self._format_list(swot_data.get('debilidades', []))],
            [Paragraph("<b>OPORTUNIDADES</b>", self.styles['Normal']),
             Paragraph("<b>AMENAZAS</b>", self.styles['Normal'])],
            [self._format_list(swot_data.get('oportunidades', [])),
             self._format_list(swot_data.get('amenazas', []))]
        ]
        
        table = Table(data, colWidths=[9*cm, 9*cm])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6f2ff')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e6f2ff')),
        ]))
        
        elements.append(table)
        return elements
    
    def _format_list(self, items):
        """Formatea una lista para el PDF"""
        if not items:
            return Paragraph("No disponible", self.styles['Normal'])
        
        text = "<br/>".join([f"• {item}" for item in items])
        return Paragraph(text, self.styles['Normal'])
    
    def _create_executive_summary_ai(self, datos, thesis_data):
        """Crea resumen ejecutivo con tesis de inversión de IA"""
        elements = []
        
        title = Paragraph("RESUMEN EJECUTIVO", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Resumen de IA
        if thesis_data.get('resumen_ejecutivo'):
            summary = Paragraph(thesis_data['resumen_ejecutivo'], self.styles['Normal'])
            elements.append(summary)
            elements.append(Spacer(1, 12))
        
        # Puntos clave
        if thesis_data.get('puntos_clave_inversion'):
            subtitle = Paragraph("<b>Puntos Clave de Inversión:</b>", self.styles['Normal'])
            elements.append(subtitle)
            elements.append(self._format_list(thesis_data['puntos_clave_inversion']))
            elements.append(Spacer(1, 12))
        
        # Recomendación
        if thesis_data.get('recomendacion'):
            rec_text = f"<b>Recomendación:</b> {thesis_data['recomendacion']}"
            rec_para = Paragraph(rec_text, self.styles['Normal'])
            elements.append(rec_para)
        
        return elements
    
    def _create_financial_analysis_ai(self, datos, financial_analysis):
        """Crea análisis financiero detallado con comentarios de IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS FINANCIERO PROFUNDO", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Análisis de márgenes
        if financial_analysis.get('analisis_margenes'):
            subtitle = Paragraph("<b>Análisis de Márgenes:</b>", self.styles['Normal'])
            elements.append(subtitle)
            margin_text = financial_analysis['analisis_margenes']
            elements.append(Paragraph(margin_text, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Análisis de liquidez
        if financial_analysis.get('analisis_liquidez'):
            subtitle = Paragraph("<b>Análisis de Liquidez:</b>", self.styles['Normal'])
            elements.append(subtitle)
            liquidity_text = financial_analysis['analisis_liquidez']
            elements.append(Paragraph(liquidity_text, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Análisis de eficiencia
        if financial_analysis.get('analisis_eficiencia'):
            subtitle = Paragraph("<b>Eficiencia Operativa:</b>", self.styles['Normal'])
            elements.append(subtitle)
            efficiency_text = financial_analysis['analisis_eficiencia']
            elements.append(Paragraph(efficiency_text, self.styles['Normal']))
        
        return elements
    
    def _create_projections_ai(self, datos, projections_analysis):
        """Crea sección de proyecciones con análisis de IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS DE PROYECCIONES", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Análisis de crecimiento
        if projections_analysis.get('analisis_crecimiento'):
            growth_text = projections_analysis['analisis_crecimiento']
            elements.append(Paragraph(growth_text, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Escenarios
        if projections_analysis.get('escenarios'):
            subtitle = Paragraph("<b>Análisis de Escenarios:</b>", self.styles['Normal'])
            elements.append(subtitle)
            
            for escenario in ['optimista', 'base', 'pesimista']:
                if escenario in projections_analysis['escenarios']:
                    esc_data = projections_analysis['escenarios'][escenario]
                    esc_text = f"<b>{escenario.capitalize()}:</b> {esc_data}"
                    elements.append(Paragraph(esc_text, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        return elements
    
    def _create_recommendations_ai(self, recommendations):
        """Crea sección de recomendaciones estratégicas de IA"""
        elements = []
        
        title = Paragraph("RECOMENDACIONES ESTRATÉGICAS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Recomendaciones por área
        for area in ['operativas', 'financieras', 'estrategicas', 'comerciales']:
            if area in recommendations:
                subtitle = Paragraph(f"<b>{area.capitalize()}:</b>", self.styles['Normal'])
                elements.append(subtitle)
                elements.append(self._format_list(recommendations[area]))
                elements.append(Spacer(1, 12))
        
        return elements

# Función principal para generar el PDF
def generate_ai_pdf(datos, ai_analysis=None):
    """
    Función principal para generar PDF con análisis de IA
    """
    generator = PDFAIGenerator()
    return generator.generate_pdf_with_ai(datos, ai_analysis)
