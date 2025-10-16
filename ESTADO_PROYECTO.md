# ESTADO DEL PROYECTO - Business Plan IA Demo
**Fecha:** 08 Octubre 2025

## BUGS PENDIENTES EN PDF MetalPro:

1. ROIC = 0.0% (debería ser ~15-20%)
2. Margen EBITDA = 0.0% (debería ser ~20-25%)
3. Cash Conversion Cycle = 0 días (debería ser 60-90)
4. Company Overview incompleto (falta info del sidebar)
5. SWOT en 2 páginas (debería ser 1)
6. Proyecciones: falta columna VARIACIÓN
7. Faltan: FCF proyectado y Balance proyectado
8. Tabla sectorial: texto se sale

## ARCHIVOS CLAVE:
- utils/data_collector.py: Recopila datos para IA
- utils/ai_prompts.py: Genera prompts
- utils/pdf_ia_generator.py: Genera PDF
- utils/mckinsey.py: Cálculos financieros

## CORRECCIONES YA HECHAS:
✅ Modelo actualizado a Gemini 2.5 Flash
✅ Variables info_empresa agregadas
✅ Función get_val() para tablas
✅ Tests de sintaxis pasan

## PRÓXIMO PASO:
Debug de data_collector.py para ver por qué los KPIs están en 0
