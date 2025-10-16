#!/usr/bin/env python3
"""
Generador de Informe de Valoración Profesional
Estándar Banca de Inversión para Medianas Empresas
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import KeepTogether, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import pandas as pd
from typing import Dict, Any

class ValuationReportGenerator:
    """
    Genera informe de valoración con estándar de banca de inversión
    """
    
    def __init__(self):
        self.buffer = BytesIO()
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Define estilos personalizados para el informe"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#4a5568'),
            spaceBefore=12,
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Título de sección
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a5f'),
            spaceBefore=24,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto profesional
        self.styles.add(ParagraphStyle(
            name='ProfessionalBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2d3748'),
            leftIndent=20,
            spaceBefore=3,
            spaceAfter=3
        ))
        
        # Disclaimer
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#718096'),
            alignment=TA_JUSTIFY,
            spaceBefore=12
        ))
        
    def generate_report(self, company_data: Dict, financial_data: Dict, 
                       valuation_data: Dict, ai_analysis: Dict) -> BytesIO:
        """
        Genera el informe completo de valoración
        """
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # 1. Portada
        story.extend(self._create_cover_page(company_data))
        story.append(PageBreak())
        
        # 2. Executive Summary
        story.extend(self._create_executive_summary(company_data, financial_data, valuation_data))
        story.append(PageBreak())
        
        # 3. Análisis Macroeconómico y Sectorial
        story.extend(self._create_macro_analysis(company_data, ai_analysis))
        story.append(PageBreak())
        
        # 4. Company Overview
        story.extend(self._create_company_overview(company_data))
        story.append(PageBreak())
        
        # 5. Análisis Estratégico - SWOT
        story.extend(self._create_swot_analysis(ai_analysis))
        story.append(PageBreak())
        
        # 6. Financial Performance Analysis
        story.extend(self._create_financial_analysis(financial_data))
        story.append(PageBreak())
        
        # 7. Valuation Analysis
        story.extend(self._create_valuation_analysis(valuation_data))
        story.append(PageBreak())
        
        # 8. Risk Assessment
        story.extend(self._create_risk_assessment(ai_analysis))
        story.append(PageBreak())
        
        # 9. Strategic Recommendations
        story.extend(self._create_recommendations(ai_analysis))
        story.append(PageBreak())
        
        # 10. Appendix
        story.extend(self._create_appendix(financial_data))
        
        # Generar PDF
        doc.build(story)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_cover_page(self, company_data: Dict) -> list:
        """Crea la portada del informe"""
        elements = []
        
        # Espaciado superior
        elements.append(Spacer(1, 5*cm))
        
        # Título principal
        title = Paragraph(
            "INFORME DE VALORACIÓN",
            self.styles['MainTitle']
        )
        elements.append(title)
        
        # Nombre de la empresa
        company_name = Paragraph(
            f"<b>{company_data.get('nombre_empresa', 'Empresa')}</b>",
            self.styles['MainTitle']
        )
        elements.append(company_name)
        
        elements.append(Spacer(1, 1*cm))
        
        # Subtítulos
        sector = Paragraph(
            f"Sector: {company_data.get('sector', 'N/A')}",
            self.styles['Subtitle']
        )
        elements.append(sector)
        
        date = Paragraph(
            f"Fecha: {datetime.now().strftime('%B %Y')}",
            self.styles['Subtitle']
        )
        elements.append(date)
        
        elements.append(Spacer(1, 3*cm))
        
        # Disclaimer
        disclaimer_text = """
        Este informe ha sido preparado con fines informativos. Las proyecciones y valoraciones 
        se basan en supuestos que pueden no materializarse. Se recomienda realizar due diligence 
        adicional antes de tomar decisiones de inversión.
        """
        disclaimer = Paragraph(disclaimer_text, self.styles['Disclaimer'])
        elements.append(disclaimer)
        
        return elements
    
    def _create_executive_summary(self, company_data: Dict, financial_data: Dict, 
                                 valuation_data: Dict) -> list:
        """Crea el resumen ejecutivo"""
        elements = []
        
        title = Paragraph("EXECUTIVE SUMMARY", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Investment Thesis
        thesis_title = Paragraph("<b>Investment Thesis</b>", self.styles['ProfessionalBody'])
        elements.append(thesis_title)
        
        thesis_text = f"""
        {company_data.get('nombre_empresa', 'La empresa')} presenta una oportunidad de inversión
        en el sector {company_data.get('sector', 'N/A')} con un valor empresa estimado de 
        €{valuation_data.get('enterprise_value', 0):,.0f}. El modelo de negocio se basa en
        {company_data.get('modelo_negocio', 'N/A')} con ventajas competitivas sostenibles.
        """
        thesis = Paragraph(thesis_text, self.styles['ProfessionalBody'])
        elements.append(thesis)
        elements.append(Spacer(1, 12))
        
        # Métricas clave
        metrics_data = [
            ['MÉTRICAS CLAVE', 'VALOR'],
            ['Valor Empresa (DCF)', f"€{valuation_data.get('enterprise_value', 0):,.0f}"],
            ['WACC', f"{valuation_data.get('wacc', 0):.1f}%"],
            ['TIR Proyecto', f"{valuation_data.get('tir', 0):.1f}%"],
            ['ROIC Promedio', f"{valuation_data.get('roic_promedio', 0):.1f}%"],
            ['Deuda Neta', f"€{valuation_data.get('deuda_neta', 0):,.0f}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[8*cm, 6*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')])
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 12))
        
        # Recomendación
        rec_value = self._determine_recommendation(valuation_data)
        rec_text = f"<b>RECOMENDACIÓN: {rec_value}</b>"
        recommendation = Paragraph(rec_text, self.styles['SectionTitle'])
        elements.append(recommendation)
        
        return elements
    
    def _create_macro_analysis(self, company_data: Dict, ai_analysis: Dict) -> list:
        """Crea el análisis macroeconómico y sectorial"""
        elements = []
        
        title = Paragraph("ANÁLISIS MACROECONÓMICO Y SECTORIAL", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Contexto Macroeconómico
        macro_title = Paragraph("<b>Contexto Macroeconómico</b>", self.styles['ProfessionalBody'])
        elements.append(macro_title)
        
        macro_data = ai_analysis.get('macro_analysis', {})
        if not macro_data or macro_data.get('fallback'):
            # Generar análisis genérico basado en el sector
            macro_text = f"""
            El sector {company_data.get('sector', 'N/A')} se encuentra en un momento de transformación
            impulsado por la digitalización y cambios en patrones de consumo. Los tipos de interés 
            actuales y la inflación moderada crean un entorno favorable para la inversión, aunque 
            persisten riesgos geopolíticos y de cadena de suministro que requieren monitorización.
            """
        else:
            macro_text = macro_data.get('analisis', 'Análisis no disponible')
        
        macro = Paragraph(macro_text, self.styles['ProfessionalBody'])
        elements.append(macro)
        elements.append(Spacer(1, 12))
        
        # Análisis Sectorial
        sector_title = Paragraph("<b>Análisis Sectorial</b>", self.styles['ProfessionalBody'])
        elements.append(sector_title)
        
        # Tabla de datos sectoriales
        sector_data = [
            ['MÉTRICA SECTORIAL', 'EMPRESA', 'MEDIA SECTOR', 'POSICIÓN'],
            ['Cuota de Mercado', f"{company_data.get('cuota_mercado', 0)}%", '5-15%', 'En desarrollo'],
            ['Crecimiento Anual', 'Por determinar', '10-15%', 'Por determinar'],
            ['Margen EBITDA', 'Por determinar', '15-25%', 'Por determinar']
        ]
        
        sector_table = Table(sector_data, colWidths=[5*cm, 3.5*cm, 3.5*cm, 3*cm])
        sector_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        elements.append(sector_table)
        
        return elements
    
    def _create_company_overview(self, company_data: Dict) -> list:
        """Crea el overview de la empresa"""
        elements = []
        
        title = Paragraph("COMPANY OVERVIEW", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Modelo de Negocio
        model_title = Paragraph("<b>Modelo de Negocio</b>", self.styles['ProfessionalBody'])
        elements.append(model_title)
        
        model_text = f"""
        {company_data.get('descripcion_actividad', 'N/A')}. El modelo de negocio se centra en
        {company_data.get('modelo_negocio', 'N/A')}, ofreciendo {company_data.get('productos_servicios', 'N/A')}.
        """
        model = Paragraph(model_text, self.styles['ProfessionalBody'])
        elements.append(model)
        elements.append(Spacer(1, 12))
        
        # Ventajas Competitivas
        competitive_title = Paragraph("<b>Ventajas Competitivas</b>", self.styles['ProfessionalBody'])
        elements.append(competitive_title)
        
        competitive_text = company_data.get('ventaja_competitiva_clave', 
                                           'Pendiente de identificación de ventajas competitivas sostenibles')
        competitive = Paragraph(competitive_text, self.styles['ProfessionalBody'])
        elements.append(competitive)
        
        return elements
    
    def _create_swot_analysis(self, ai_analysis: Dict) -> list:
        """Crea el análisis SWOT"""
        elements = []
        
        title = Paragraph("ANÁLISIS ESTRATÉGICO - SWOT", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        swot_data = ai_analysis.get('swot', {})
        
        # Crear tabla SWOT 2x2
        swot_table_data = [
            [Paragraph("<b>FORTALEZAS</b>", self.styles['ProfessionalBody']),
             Paragraph("<b>DEBILIDADES</b>", self.styles['ProfessionalBody'])],
            [self._format_swot_list(swot_data.get('fortalezas', [])),
             self._format_swot_list(swot_data.get('debilidades', []))],
            [Paragraph("<b>OPORTUNIDADES</b>", self.styles['ProfessionalBody']),
             Paragraph("<b>AMENAZAS</b>", self.styles['ProfessionalBody'])],
            [self._format_swot_list(swot_data.get('oportunidades', [])),
             self._format_swot_list(swot_data.get('amenazas', []))]
        ]
        
        swot_table = Table(swot_table_data, colWidths=[7.5*cm, 7.5*cm])
        swot_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#e6f2ff')),
            ('BACKGROUND', (0, 2), (1, 2), colors.HexColor('#e6f2ff')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 10)
        ]))
        
        elements.append(swot_table)
        
        return elements
    
    def _format_swot_list(self, items: list) -> Paragraph:
        """Formatea una lista para el SWOT"""
        if not items:
            return Paragraph("• Por determinar", self.styles['BulletPoint'])
        
        text = "<br/>".join([f"• {item}" for item in items[:4]])  # Máximo 4 items
        return Paragraph(text, self.styles['BulletPoint'])
    
    def _create_financial_analysis(self, financial_data: Dict) -> list:
        """Crea el análisis financiero"""
        elements = []
        
        title = Paragraph("FINANCIAL PERFORMANCE ANALYSIS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Proyecciones Financieras
        proj_title = Paragraph("<b>Proyecciones Financieras (5 años)</b>", self.styles['ProfessionalBody'])
        elements.append(proj_title)
        elements.append(Spacer(1, 6))
        
        # Tabla resumen de proyecciones
        if financial_data.get('pyl_df') is not None:
            pyl_df = financial_data['pyl_df']
            # Crear tabla simplificada con métricas clave
            proj_data = [
                ['CONCEPTO', 'Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5'],
                ['Ingresos (€000)', '—', '—', '—', '—', '—'],
                ['EBITDA (€000)', '—', '—', '—', '—', '—'],
                ['Margen EBITDA (%)', '—', '—', '—', '—', '—'],
                ['FCF (€000)', '—', '—', '—', '—', '—']
            ]
        else:
            proj_data = [
                ['CONCEPTO', 'Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5'],
                ['Proyecciones no disponibles', '—', '—', '—', '—', '—']
            ]
        
        proj_table = Table(proj_data, colWidths=[4*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(proj_table)
        
        return elements
    
    def _create_valuation_analysis(self, valuation_data: Dict) -> list:
        """Crea el análisis de valoración"""
        elements = []
        
        title = Paragraph("VALUATION ANALYSIS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # DCF Analysis
        dcf_title = Paragraph("<b>Discounted Cash Flow Analysis</b>", self.styles['ProfessionalBody'])
        elements.append(dcf_title)
        elements.append(Spacer(1, 6))
        
        # Tabla de valoración
        val_data = [
            ['COMPONENTE', 'VALOR'],
            ['Valor Presente FCF (5 años)', f"€{valuation_data.get('pv_fcf', 0):,.0f}"],
            ['Valor Terminal', f"€{valuation_data.get('valor_terminal', 0):,.0f}"],
            ['Valor Presente Terminal', f"€{valuation_data.get('pv_terminal', 0):,.0f}"],
            ['Enterprise Value', f"€{valuation_data.get('enterprise_value', 0):,.0f}"],
            ['(-) Deuda Neta', f"€{valuation_data.get('deuda_neta', 0):,.0f}"],
            ['Equity Value', f"€{valuation_data.get('equity_value', 0):,.0f}"]
        ]
        
        val_table = Table(val_data, colWidths=[8*cm, 6*cm])
        val_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#e6f2ff'))
        ]))
        
        elements.append(val_table)
        
        return elements
    
    def _create_risk_assessment(self, ai_analysis: Dict) -> list:
        """Crea la evaluación de riesgos"""
        elements = []
        
        title = Paragraph("RISK ASSESSMENT", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        risk_data = ai_analysis.get('risks', {})
        
        # Tabla de riesgos
        risk_table_data = [
            ['RIESGO', 'PROBABILIDAD', 'IMPACTO', 'MITIGACIÓN']
        ]
        
        if risk_data and not risk_data.get('fallback'):
            for risk in risk_data.get('risks', [])[:5]:  # Máximo 5 riesgos
                risk_table_data.append([
                    Paragraph(risk.get('descripcion', ''), self.styles['BulletPoint']),
                    risk.get('probabilidad', 'Media'),
                    risk.get('impacto', 'Alto'),
                    Paragraph(risk.get('mitigacion', ''), self.styles['BulletPoint'])
                ])
        else:
            risk_table_data.append([
                'Análisis de riesgos pendiente', 'N/A', 'N/A', 'N/A'
            ])
        
        risk_table = Table(risk_table_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 5.5*cm])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b6b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(risk_table)
        
        return elements
    
    def _create_recommendations(self, ai_analysis: Dict) -> list:
        """Crea las recomendaciones estratégicas"""
        elements = []
        
        title = Paragraph("STRATEGIC RECOMMENDATIONS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        action_plan = ai_analysis.get('action_plan', {})
        
        # Iniciativas de Creación de Valor
        value_title = Paragraph("<b>Iniciativas de Creación de Valor</b>", self.styles['ProfessionalBody'])
        elements.append(value_title)
        elements.append(Spacer(1, 6))
        
        if action_plan and not action_plan.get('fallback'):
            # Corto plazo
            short_term = action_plan.get('corto_plazo', [])
            if short_term:
                st_title = Paragraph("Corto Plazo (0-12 meses):", self.styles['ProfessionalBody'])
                elements.append(st_title)
                for item in short_term[:3]:
                    bullet = Paragraph(f"• {item}", self.styles['BulletPoint'])
                    elements.append(bullet)
                elements.append(Spacer(1, 6))
            
            # Medio plazo
            medium_term = action_plan.get('medio_plazo', [])
            if medium_term:
                mt_title = Paragraph("Medio Plazo (1-3 años):", self.styles['ProfessionalBody'])
                elements.append(mt_title)
                for item in medium_term[:3]:
                    bullet = Paragraph(f"• {item}", self.styles['BulletPoint'])
                    elements.append(bullet)
                elements.append(Spacer(1, 6))
            
            # Largo plazo
            long_term = action_plan.get('largo_plazo', [])
            if long_term:
                lt_title = Paragraph("Largo Plazo (3+ años):", self.styles['ProfessionalBody'])
                elements.append(lt_title)
                for item in long_term[:3]:
                    bullet = Paragraph(f"• {item}", self.styles['BulletPoint'])
                    elements.append(bullet)
        else:
            text = Paragraph("Plan de acción estratégico en desarrollo", self.styles['ProfessionalBody'])
            elements.append(text)
        
        return elements
    
    def _create_appendix(self, financial_data: Dict) -> list:
        """Crea el apéndice con estados financieros"""
        elements = []
        
        title = Paragraph("APPENDIX - ESTADOS FINANCIEROS PROYECTADOS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Nota sobre los estados financieros
        note_text = """
        Los estados financieros proyectados se basan en las asunciones detalladas en el modelo
        de valoración. Las proyecciones están sujetas a incertidumbre y los resultados reales
        pueden diferir materialmente de las estimaciones.
        """
        note = Paragraph(note_text, self.styles['Disclaimer'])
        elements.append(note)
        
        return elements
    
    def _determine_recommendation(self, valuation_data: Dict) -> str:
        """Determina la recomendación de inversión"""
        tir = valuation_data.get('tir', 0)
        wacc = valuation_data.get('wacc', 0)
        
        if tir > wacc + 5:
            return "COMPRAR"
        elif tir > wacc:
            return "MANTENER"
        else:
            return "REVISAR"


def generate_professional_valuation_report(datos: Dict, ai_analysis: Dict) -> BytesIO:
    """
    Función principal para generar el informe de valoración profesional
    """
    generator = ValuationReportGenerator()
    
    # Extraer datos necesarios
    company_data = {
        'nombre_empresa': datos.get('nombre_empresa', 'Empresa'),
        'sector': datos.get('sector', 'N/A'),
        'descripcion_actividad': datos.get('datos_empresa', {}).get('descripcion_actividad', 'N/A'),
        'modelo_negocio': datos.get('datos_empresa', {}).get('modelo_negocio', 'N/A'),
        'productos_servicios': datos.get('datos_empresa', {}).get('productos_servicios', 'N/A'),
        'ventaja_competitiva_clave': datos.get('datos_empresa', {}).get('ventaja_competitiva_clave', 'N/A')
    }
    financial_data = {
        'pyl_df': datos.get('pyl'),
        'balance_df': datos.get('balance'),
        'fcf_df': datos.get('cash_flow')
    }
    valuation_data = datos.get('resultado_mckinsey', {})
    
    # Generar informe
    return generator.generate_report(
        company_data=company_data,
        financial_data=financial_data,
        valuation_data=valuation_data,
        ai_analysis=ai_analysis
    )
