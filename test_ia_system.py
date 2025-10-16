#!/usr/bin/env python3
"""
Script de prueba para detectar TODOS los errores del sistema IA V2
"""

import sys
import traceback
from datetime import datetime

print("=" * 80)
print("TEST COMPLETO DEL SISTEMA IA V2")
print("=" * 80)

# Simular session_state mínimo
class MockSessionState:
    def __init__(self):
        self.data = {
            'datos_guardados': {
                'nombre_empresa': 'Test Company',
                'sector': 'Tecnología',
                'datos_empresa': {
                    'descripcion_actividad': 'Test',
                    'productos_servicios': 'Test',
                    'modelo_negocio': 'SaaS',
                    'posicionamiento_precio': 'Premium',
                    'competidores_principales': 'Comp1, Comp2',
                    'ventaja_competitiva_principal': 'Test advantage',
                    'principales_riesgos': 'Test risks',
                    'clientes_objetivo': 'Test clients',
                    'vision_corto': 'Short term',
                    'vision_medio': 'Medium term',
                    'vision_largo': 'Long term',
                    'porcentaje_fijos': 70,
                    'porcentaje_variables': 30
                },
                'pyl': None,
                'balance': None,
                'cash_flow': None,
                'ratios': {},
                'resultado_mckinsey': {
                    'enterprise_value': 1000000,
                    'equity_value': 800000,
                    'wacc': 10.5,
                    'tir': 15.2,
                    'deuda_neta': 200000,
                    'dcf_detalle': {
                        'roic_promedio': 18.5,
                        'fcf_total_5anos': 500000,
                        'valor_terminal': 600000,
                        'g': 2.5
                    }
                }
            },
            'escenario_seleccionado': 'Base',
            'descripcion_actividad_sidebar': 'Test activity',
            'modelo_negocio': 'SaaS',
            'posicionamiento_precio': 'Premium',
            'competidores_principales': 'Comp1, Comp2',
            'ventaja_competitiva_clave': 'Innovation',
            'vision_corto_plazo': 'Short',
            'vision_medio_plazo': 'Medium',
            'vision_largo_plazo': 'Long',
            'principales_riesgos': 'Market risk'
        }
    
    def get(self, key, default=None):
        return self.data.get(key, default)

# Mockear streamlit
class MockStreamlit:
    session_state = MockSessionState()

sys.modules['streamlit'] = MockStreamlit()
import streamlit as st

errors = []

# Test 1: data_collector
print("\n1️⃣  Testing data_collector...")
try:
    from utils.data_collector import recopilar_datos_completos
    datos = recopilar_datos_completos()
    print("   ✅ data_collector OK")
    print(f"   Info básica: {datos['info_basica']['nombre_empresa']}")
except Exception as e:
    errors.append(("data_collector", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")

# Test 2: ai_prompts
print("\n2️⃣  Testing ai_prompts...")
try:
    from utils.ai_prompts import (
        generar_prompt_executive_summary,
        generar_prompt_macro_sectorial,
        generar_prompt_swot,
        generar_prompt_kpis_detalle,
        generar_prompt_riesgos,
        generar_prompt_recomendaciones
    )
    
    if 'datos' in locals():
        prompt_exec = generar_prompt_executive_summary(datos)
        prompt_macro = generar_prompt_macro_sectorial(datos)
        prompt_swot = generar_prompt_swot(datos)
        prompt_kpis = generar_prompt_kpis_detalle(datos)
        prompt_riesgos = generar_prompt_riesgos(datos)
        prompt_recom = generar_prompt_recomendaciones(datos)
        
        print("   ✅ ai_prompts OK")
        print(f"   Prompts generados: 6/6")
    else:
        print("   ⚠️  Skipped (datos no disponibles)")
except Exception as e:
    errors.append(("ai_prompts", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")

# Test 3: pdf_ia_generator (solo estructura, sin generar)
print("\n3️⃣  Testing pdf_ia_generator...")
try:
    from utils.pdf_ia_generator import PDFIAGenerator
    
    # Solo crear el objeto para verificar estilos
    generator = PDFIAGenerator()
    print("   ✅ pdf_ia_generator OK")
    print(f"   Estilos personalizados: {len([s for s in generator.styles.byName if 'Custom' in s or 'Section' in s])}")
except Exception as e:
    errors.append(("pdf_ia_generator", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")

# Test 4: ai_analyzer_v2 (sin llamar a IA real)
print("\n4️⃣  Testing ai_analyzer_v2...")
try:
    from utils.ai_analyzer_v2 import AIAnalyzerV2
    
    # Solo verificar que se puede importar y crear
    print("   ✅ ai_analyzer_v2 OK (import)")
except Exception as e:
    errors.append(("ai_analyzer_v2", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")

# Resumen
print("\n" + "=" * 80)
print("RESUMEN DE TESTS")
print("=" * 80)

if not errors:
    print("🎉 ¡TODOS LOS TESTS PASARON!")
    print("\nEl sistema está listo para usar con IA real.")
else:
    print(f"❌ {len(errors)} ERROR(ES) ENCONTRADO(S):\n")
    for i, (modulo, error, trace) in enumerate(errors, 1):
        print(f"\n{i}. ERROR EN: {modulo}")
        print(f"   Mensaje: {error}")
        print(f"\n   Traceback:")
        print("   " + "\n   ".join(trace.split("\n")[:10]))
        print("   ...")

print("\n" + "=" * 80)


# Test 5: Generar PDF simulado (con análisis mock)
print("\n5️⃣  Testing generación de PDF completo...")
try:
    from utils.pdf_ia_generator import generar_pdf_con_ia
    
    # Análisis mock (simulando respuesta de IA)
    analisis_mock = {
        'modelo_ia': 'test',
        'executive_summary': {
            'investment_thesis': 'Test thesis sobre la empresa.',
            'recomendacion': 'PROCEDER',
            'rating': 'BUY',
            'sintesis_una_linea': 'Empresa con buen potencial'
        },
        'macro_sectorial': {
            'contexto_macro': 'Contexto económico favorable.',
            'analisis_sectorial': 'Sector en crecimiento.',
            'tamano_mercado_estimado': '€500M',
            'cagr_sectorial': '8%',
            'perspectiva_sector': 'crecimiento',
            'posicionamiento_vs_sector': 'Posicionado favorablemente'
        },
        'swot': {
            'fortalezas': ['F1', 'F2', 'F3', 'F4'],
            'debilidades': ['D1', 'D2', 'D3', 'D4'],
            'oportunidades': ['O1', 'O2', 'O3', 'O4'],
            'amenazas': ['A1', 'A2', 'A3', 'A4'],
            'sintesis_estrategica': 'Síntesis del SWOT'
        },
        'kpis_detalle': {
            'roic': {
                'interpretacion': 'ROIC saludable',
                'benchmark': 'Por encima del sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'margen_ebitda': {
                'interpretacion': 'Márgenes en expansión',
                'benchmark': 'Comparable al sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'cash_conversion_cycle': {
                'interpretacion': 'Ciclo eficiente',
                'benchmark': 'Mejor que promedio',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'deuda_neta_ebitda': {
                'interpretacion': 'Apalancamiento moderado',
                'benchmark': 'Saludable',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'cagr_ventas': {
                'interpretacion': 'Crecimiento sólido',
                'benchmark': 'Por encima del sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'sintesis_financiera': 'La empresa muestra salud financiera sólida.'
        },
        'riesgos': {
            'riesgos': [
                {
                    'nombre': 'Riesgo 1',
                    'descripcion': 'Descripción del riesgo',
                    'probabilidad': 'Media',
                    'impacto': 'Alto',
                    'mitigacion': ['Mitigación 1', 'Mitigación 2'],
                    'indicadores_alerta': ['KPI1', 'KPI2']
                }
            ],
            'riesgo_principal': 'Riesgo competitivo',
            'nivel_riesgo_global': 'Medio'
        },
        'recomendaciones': {
            'quick_wins': [
                {
                    'titulo': 'Quick Win 1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Alto',
                    'recursos': 'Bajos',
                    'timeline': '3 meses'
                }
            ],
            'medio_plazo': [
                {
                    'titulo': 'Iniciativa MP1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Alto',
                    'recursos': 'Medios',
                    'timeline': '12 meses'
                }
            ],
            'largo_plazo': [
                {
                    'titulo': 'Iniciativa LP1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Muy Alto',
                    'recursos': 'Altos',
                    'timeline': '24 meses'
                }
            ],
            'prioridad_1': 'Enfocarse en Quick Win 1',
            'roadmap_estrategico': 'Roadmap integrado'
        }
    }
    
    if 'datos' in locals():
        pdf_buffer = generar_pdf_con_ia(datos, analisis_mock)
        
        # Guardar PDF de prueba
        with open('/tmp/test_informe_ia.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print("   ✅ PDF generado correctamente")
        print("   Archivo guardado: /tmp/test_informe_ia.pdf")
        
        import os
        size_kb = os.path.getsize('/tmp/test_informe_ia.pdf') / 1024
        print(f"   Tamaño: {size_kb:.1f} KB")
    else:
        print("   ⚠️  Skipped (datos no disponibles)")
        
except Exception as e:
    errors.append(("pdf_generation", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")
    traceback.print_exc()

# Resumen final actualizado
print("\n" + "=" * 80)
if not errors:
    print("🎉 ¡SISTEMA 100% FUNCIONAL!")
    print("\n✅ Puedes usar el botón '🤖 Análisis Completo IA V2' en la app")
else:
    print(f"⚠️  {len(errors)} problema(s) encontrado(s)")


# Test 5: Generar PDF simulado (con análisis mock)
print("\n5️⃣  Testing generación de PDF completo...")
try:
    from utils.pdf_ia_generator import generar_pdf_con_ia
    
    # Análisis mock (simulando respuesta de IA)
    analisis_mock = {
        'modelo_ia': 'test',
        'executive_summary': {
            'investment_thesis': 'Test thesis sobre la empresa.',
            'recomendacion': 'PROCEDER',
            'rating': 'BUY',
            'sintesis_una_linea': 'Empresa con buen potencial'
        },
        'macro_sectorial': {
            'contexto_macro': 'Contexto económico favorable.',
            'analisis_sectorial': 'Sector en crecimiento.',
            'tamano_mercado_estimado': '€500M',
            'cagr_sectorial': '8%',
            'perspectiva_sector': 'crecimiento',
            'posicionamiento_vs_sector': 'Posicionado favorablemente'
        },
        'swot': {
            'fortalezas': ['F1', 'F2', 'F3', 'F4'],
            'debilidades': ['D1', 'D2', 'D3', 'D4'],
            'oportunidades': ['O1', 'O2', 'O3', 'O4'],
            'amenazas': ['A1', 'A2', 'A3', 'A4'],
            'sintesis_estrategica': 'Síntesis del SWOT'
        },
        'kpis_detalle': {
            'roic': {
                'interpretacion': 'ROIC saludable',
                'benchmark': 'Por encima del sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'margen_ebitda': {
                'interpretacion': 'Márgenes en expansión',
                'benchmark': 'Comparable al sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'cash_conversion_cycle': {
                'interpretacion': 'Ciclo eficiente',
                'benchmark': 'Mejor que promedio',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'deuda_neta_ebitda': {
                'interpretacion': 'Apalancamiento moderado',
                'benchmark': 'Saludable',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'cagr_ventas': {
                'interpretacion': 'Crecimiento sólido',
                'benchmark': 'Por encima del sector',
                'como_mejorar': ['Mejora 1', 'Mejora 2']
            },
            'sintesis_financiera': 'La empresa muestra salud financiera sólida.'
        },
        'riesgos': {
            'riesgos': [
                {
                    'nombre': 'Riesgo 1',
                    'descripcion': 'Descripción del riesgo',
                    'probabilidad': 'Media',
                    'impacto': 'Alto',
                    'mitigacion': ['Mitigación 1', 'Mitigación 2'],
                    'indicadores_alerta': ['KPI1', 'KPI2']
                }
            ],
            'riesgo_principal': 'Riesgo competitivo',
            'nivel_riesgo_global': 'Medio'
        },
        'recomendaciones': {
            'quick_wins': [
                {
                    'titulo': 'Quick Win 1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Alto',
                    'recursos': 'Bajos',
                    'timeline': '3 meses'
                }
            ],
            'medio_plazo': [
                {
                    'titulo': 'Iniciativa MP1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Alto',
                    'recursos': 'Medios',
                    'timeline': '12 meses'
                }
            ],
            'largo_plazo': [
                {
                    'titulo': 'Iniciativa LP1',
                    'descripcion': 'Descripción',
                    'impacto_esperado': 'Muy Alto',
                    'recursos': 'Altos',
                    'timeline': '24 meses'
                }
            ],
            'prioridad_1': 'Enfocarse en Quick Win 1',
            'roadmap_estrategico': 'Roadmap integrado'
        }
    }
    
    if 'datos' in locals():
        pdf_buffer = generar_pdf_con_ia(datos, analisis_mock)
        
        # Guardar PDF de prueba
        with open('/tmp/test_informe_ia.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print("   ✅ PDF generado correctamente")
        print("   Archivo guardado: /tmp/test_informe_ia.pdf")
        
        import os
        size_kb = os.path.getsize('/tmp/test_informe_ia.pdf') / 1024
        print(f"   Tamaño: {size_kb:.1f} KB")
    else:
        print("   ⚠️  Skipped (datos no disponibles)")
        
except Exception as e:
    errors.append(("pdf_generation", str(e), traceback.format_exc()))
    print(f"   ❌ ERROR: {e}")
    traceback.print_exc()

# Resumen final actualizado
print("\n" + "=" * 80)
if not errors:
    print("🎉 ¡SISTEMA 100% FUNCIONAL!")
    print("\n✅ Puedes usar el botón '🤖 Análisis Completo IA V2' en la app")
else:
    print(f"⚠️  {len(errors)} problema(s) encontrado(s)")

