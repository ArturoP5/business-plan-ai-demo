"""
Generador de PDF con Análisis de IA - Versión Completa
Incluye análisis estratégico, benchmarking, KPIs y anexos financieros
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

class PDFAIGeneratorCompleto:
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
        
        self.styles.add(ParagraphStyle(
            name='FinancialHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            alignment=TA_CENTER,
            bold=True
        ))
        
    def generate_complete_pdf(self, datos, ai_analysis=None):
        """
        Genera PDF completo con análisis de IA y anexos financieros
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # PARTE 1: ANÁLISIS ESTRATÉGICO CON IA
        
        # 1. Portada
        story.extend(self._create_cover_page(datos))
        story.append(PageBreak())
        
        # 2. Resumen Ejecutivo
        if ai_analysis and 'investment_thesis' in ai_analysis:
            story.extend(self._create_executive_summary(datos, ai_analysis['investment_thesis']))
            story.append(PageBreak())
        
        # 3. SWOT Detallado
        if ai_analysis and 'swot' in ai_analysis:
            story.extend(self._create_swot_analysis(ai_analysis['swot']))
            story.append(PageBreak())
        
        # 4. Benchmarking Sectorial
        if ai_analysis and 'benchmarking' in ai_analysis:
            story.extend(self._create_benchmarking(ai_analysis['benchmarking']))
            story.append(PageBreak())
        
        # 5. Matriz de Riesgos
        if ai_analysis and 'risk_matrix' in ai_analysis:
            story.extend(self._create_risk_matrix(ai_analysis['risk_matrix']))
            story.append(PageBreak())
        
        # 6. Valoración Comentada
        if ai_analysis and 'valuation_commentary' in ai_analysis:
            story.extend(self._create_valuation_commentary(datos, ai_analysis['valuation_commentary']))
            story.append(PageBreak())
        
        # 7. KPIs Recomendados
        if ai_analysis and 'recommended_kpis' in ai_analysis:
            story.extend(self._create_kpis_dashboard(ai_analysis['recommended_kpis']))
            story.append(PageBreak())
        
        # 8. Plan de Acción
        if ai_analysis and 'action_plan' in ai_analysis:
            story.extend(self._create_action_plan(ai_analysis['action_plan']))
            story.append(PageBreak())
        
        # PARTE 2: ANEXOS FINANCIEROS
        
        # 9. P&L Proyectado
        if 'pyl' in datos:
            story.extend(self._create_pyl_projection(datos['pyl']))
            story.append(PageBreak())
        
        # 10. FCF Proyectado
        if 'fcf' in datos:
            story.extend(self._create_fcf_projection(datos['fcf']))
            story.append(PageBreak())
        
        # 11. Balance Proyectado
        if 'balance' in datos:
            story.extend(self._create_balance_projection(datos['balance']))
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_cover_page(self, datos):
        """Crea la portada del informe"""
        elements = []
        
        title = Paragraph("INFORME DE ANÁLISIS EMPRESARIAL CON IA", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 30))
        
        company_name = datos.get('datos_empresa', {}).get('nombre_empresa', 'Empresa')
        subtitle = Paragraph(f"<b>{company_name}</b>", self.styles['Title'])
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        sector = datos.get('datos_empresa', {}).get('sector', '')
        if sector:
            sector_para = Paragraph(f"Sector: {sector}", self.styles['Normal'])
            elements.append(sector_para)
        
        elements.append(Spacer(1, 30))
        
        fecha = datetime.now().strftime("%B %Y")
        date_para = Paragraph(f"<b>Fecha:</b> {fecha}", self.styles['Normal'])
        elements.append(date_para)
        
        # Modelo IA usado
        if 'ia_model' in datos:
            model_para = Paragraph(f"<b>Análisis realizado con:</b> {datos['ia_model']}", self.styles['Normal'])
            elements.append(model_para)
        
        return elements
    
    def _create_executive_summary(self, datos, thesis_data):
        """Crea resumen ejecutivo mejorado"""
        elements = []
        
        title = Paragraph("RESUMEN EJECUTIVO", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Resumen principal
        if thesis_data.get('resumen_ejecutivo'):
            summary = Paragraph(thesis_data['resumen_ejecutivo'], self.styles['Normal'])
            elements.append(summary)
            elements.append(Spacer(1, 12))
        
        # Métricas clave en tabla
        metrics_data = [
            ['MÉTRICAS CLAVE', 'VALOR'],
            ['Valoración DCF', f"€{datos.get('valoracion', {}).get('enterprise_value', 0):,.0f}"],
            ['TIR Proyecto', f"{datos.get('valoracion', {}).get('tir', 0):.1%}"],
            ['Payback', f"{datos.get('valoracion', {}).get('payback', 0)} años"],
            ['WACC', f"{datos.get('valoracion', {}).get('wacc', 0):.1%}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[8*cm, 8*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        # Recomendación
        if thesis_data.get('recomendacion'):
            rec_style = ParagraphStyle(
                'Recommendation',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#2e7d32'),
                alignment=TA_CENTER,
                bold=True
            )
            rec_para = Paragraph(f"RECOMENDACIÓN: {thesis_data['recomendacion']}", rec_style)
            elements.append(rec_para)
        
        return elements
    
    def _create_swot_analysis(self, swot_data):
        """Crea la sección SWOT con datos de IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS SWOT", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        if swot_data and not swot_data.get('fallback'):
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
            
            table = Table(data, colWidths=[8*cm, 8*cm])
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6f2ff')),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e6f2ff')),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("Análisis SWOT no disponible", self.styles['Normal']))
        
        return elements
    
    def _format_list(self, items):
        """Formatea una lista para el PDF"""
        if not items:
            return Paragraph("—", self.styles['Normal'])
        
        text = "<br/>".join([f"• {item}" for item in items[:5]])  # Máximo 5 items
        return Paragraph(text, self.styles['Normal'])

    
    def _create_benchmarking(self, benchmarking_data):
        """Crea sección de benchmarking sectorial"""
        elements = []
        
        title = Paragraph("BENCHMARKING SECTORIAL", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        if benchmarking_data.get('posicionamiento'):
            pos_para = Paragraph(f"<b>Posicionamiento:</b> {benchmarking_data['posicionamiento']}", 
                                self.styles['Normal'])
            elements.append(pos_para)
            elements.append(Spacer(1, 12))
        
        # Tabla comparativa
        if benchmarking_data.get('comparacion'):
            comp_data = [['MÉTRICA', 'EMPRESA', 'MEDIA SECTOR', 'POSICIÓN']]
            for metric in benchmarking_data['comparacion']:
                comp_data.append([
                    metric.get('metrica', ''),
                    metric.get('empresa', ''),
                    metric.get('sector', ''),
                    metric.get('posicion', '')
                ])
            
            comp_table = Table(comp_data, colWidths=[5*cm, 4*cm, 4*cm, 3*cm])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6f2ff')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            elements.append(comp_table)
        
        return elements
    
    def _create_risk_matrix(self, risk_data):
        """Crea matriz de riesgos detallada"""
        elements = []
        
        title = Paragraph("MATRIZ DE RIESGOS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Tabla de riesgos
        risk_table_data = [['RIESGO', 'PROBABILIDAD', 'IMPACTO', 'MITIGACIÓN']]
        
        for risk in risk_data.get('risks', []):
            risk_table_data.append([
                risk.get('descripcion', ''),
                risk.get('probabilidad', ''),
                risk.get('impacto', ''),
                risk.get('mitigacion', '')
            ])
        
        risk_table = Table(risk_table_data, colWidths=[4*cm, 2.5*cm, 2.5*cm, 7*cm])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b6b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(risk_table)
        
        return elements
    
    def _create_valuation_commentary(self, datos, commentary):
        """Crea comentario de valoración con IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS DE VALORACIÓN", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Comentario principal
        if commentary.get('analisis'):
            analysis_para = Paragraph(commentary['analisis'], self.styles['Normal'])
            elements.append(analysis_para)
            elements.append(Spacer(1, 12))
        
        # Sensibilidad
        if commentary.get('sensibilidad'):
            sens_title = Paragraph("<b>Análisis de Sensibilidad:</b>", self.styles['Normal'])
            elements.append(sens_title)
            sens_para = Paragraph(commentary['sensibilidad'], self.styles['Normal'])
            elements.append(sens_para)
        
        return elements
    
    def _create_kpis_dashboard(self, kpis_data):
        """Crea dashboard de KPIs recomendados"""
        elements = []
        
        title = Paragraph("KPIs RECOMENDADOS", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Tabla de KPIs
        kpi_table_data = [['KPI', 'OBJETIVO', 'FRECUENCIA', 'RESPONSABLE']]
        
        for kpi in kpis_data.get('kpis', []):
            kpi_table_data.append([
                kpi.get('nombre', ''),
                kpi.get('objetivo', ''),
                kpi.get('frecuencia', ''),
                kpi.get('responsable', '')
            ])
        
        kpi_table = Table(kpi_table_data, colWidths=[4*cm, 5*cm, 2.5*cm, 3.5*cm])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(kpi_table)
        
        return elements
    
    def _create_action_plan(self, action_data):
        """Crea plan de acción prioritizado"""
        elements = []
        
        title = Paragraph("PLAN DE ACCIÓN", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Acciones por trimestre
        for periodo in ['corto_plazo', 'medio_plazo', 'largo_plazo']:
            if periodo in action_data:
                periodo_title = periodo.replace('_', ' ').upper()
                subtitle = Paragraph(f"<b>{periodo_title}:</b>", self.styles['Normal'])
                elements.append(subtitle)
                elements.append(Spacer(1, 6))
                
                for action in action_data[periodo]:
                    action_para = Paragraph(f"• {action}", self.styles['Normal'])
                    elements.append(action_para)
                
                elements.append(Spacer(1, 12))
        
        return elements
    
    def _create_pyl_projection(self, pyl_df):
        """Crea P&L en formato contable"""
        elements = []
        
        title = Paragraph("ANEXO I: CUENTA DE RESULTADOS PROYECTADA", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        if pyl_df is not None and not pyl_df.empty:
            # Preparar datos para tabla
            data = [['CONCEPTO'] + [f"Año {i+1}" for i in range(min(5, len(pyl_df.columns)))]]
            
            # Filas principales del P&L
            rows_to_include = ['Ventas', 'Coste de Ventas', 'Margen Bruto', 
                             'Gastos Personal', 'EBITDA', 'EBIT', 'Resultado Neto']
            
            for row in rows_to_include:
                if row in pyl_df.index:
                    row_data = [row]
                    for col in pyl_df.columns[:5]:
                        value = pyl_df.loc[row, col]
                        if pd.notna(value):
                            row_data.append(f"€{value:,.0f}")
                        else:
                            row_data.append("—")
                    data.append(row_data)
            
            # Crear tabla
            table = Table(data, colWidths=[4*cm] + [2.8*cm]*5)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            elements.append(table)
        
        return elements
    
    def _create_fcf_projection(self, fcf_data):
        """Crea FCF en formato contable"""
        elements = []
        
        title = Paragraph("ANEXO II: FLUJO DE CAJA LIBRE PROYECTADO", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Similar estructura a P&L pero con datos de FCF
        if fcf_data:
            # Aquí iría la tabla de FCF
            pass
        
        return elements
    
    def _create_balance_projection(self, balance_df):
        """Crea Balance en formato contable"""
        elements = []
        
        title = Paragraph("ANEXO III: BALANCE PROYECTADO", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Similar estructura pero con Activo/Pasivo/Patrimonio
        if balance_df is not None and not balance_df.empty:
            # Aquí iría la tabla del balance
            pass
        
        return elements

# Función principal para generar el PDF
def generate_complete_ai_pdf(datos, ai_analysis=None):
    """
    Función principal para generar PDF completo con análisis de IA
    """
    generator = PDFAIGeneratorCompleto()
    return generator.generate_complete_pdf(datos, ai_analysis)
