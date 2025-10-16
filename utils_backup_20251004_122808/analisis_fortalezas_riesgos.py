def generar_analisis_fortalezas_riesgos(datos, metodo='estandar'):
    """
    Genera análisis de fortalezas, riesgos y hoja de ruta adaptado al método de valoración
    """
    
    # Extraer métricas clave
    valor_empresa = datos.get('valor_empresa', 0)
    margen_ebitda = datos.get('margen_ebitda', 0)
    ratio_deuda_ebitda = datos.get('ratio_deuda_ebitda', 0)
    roe = datos.get('roe', 0)
    roce = datos.get('roce', 0)
    fcf_yield = datos.get('fcf_yield', 0)
    ebitda_to_fcf = datos.get('ebitda_to_fcf', 0)
    ev_ebitda = datos.get('ev_ebitda', 0)
    cagr_ventas = datos.get('cagr_ventas', 0)
    benchmark_sector = datos.get('benchmark_sector', 15)
    
    fortalezas = []
    riesgos = []
    
    if metodo == 'mckinsey':
        # Análisis más agresivo para McKinsey
        
        # FORTALEZAS - Enfoque growth/expansión
        if margen_ebitda > benchmark_sector * 1.2:
            fortalezas.append(f"**Excelencia operativa demostrada**: Margen EBITDA {margen_ebitda:.1f}% supera sector en {(margen_ebitda/benchmark_sector-1)*100:.0f}%, validando tesis de roll-up")
        elif margen_ebitda > benchmark_sector:
            fortalezas.append(f"**Plataforma sólida para M&A**: Margen EBITDA {margen_ebitda:.1f}% permite sinergias en adquisiciones")
            
        if ratio_deuda_ebitda < 1.5:
            fortalezas.append(f"**Capacidad de apalancamiento sin explotar**: {ratio_deuda_ebitda:.1f}x permite LBO agresivo hasta 4-5x para maximizar TIR")
        elif ratio_deuda_ebitda < 2.5:
            fortalezas.append(f"**Estructura óptima para recap**: Espacio para dividend recap de €{valor_empresa*0.3:,.0f}")
            
        if roce > 20:
            fortalezas.append(f"**ROCE excepcional {roce:.0f}%**: Justifica múltiplos premium y estrategia buy-and-build")
            
        if fcf_yield > 7:
            fortalezas.append(f"**Cash machine con FCF yield {fcf_yield:.1f}%**: Autofinancia crecimiento inorgánico")
            
        # RIESGOS - Perspectiva PE/Growth
        if cagr_ventas < 5:
            riesgos.append(f"**Crecimiento orgánico limitado {cagr_ventas:.1f}%**: Requiere M&A agresivo para generar alfa")
        
        if ev_ebitda > 12:
            riesgos.append(f"**Valoración entrada {ev_ebitda:.1f}x**: Limita arbitraje de múltiplos, requiere mejora operativa")
            
    else:
        # Análisis más conservador para método estándar
        
        # FORTALEZAS - Enfoque value/conservador  
        if margen_ebitda > benchmark_sector * 1.1:
            fortalezas.append(f"**Rentabilidad superior**: Margen EBITDA {margen_ebitda:.1f}% vs sector {benchmark_sector:.0f}% indica ventajas competitivas")
        
        if ratio_deuda_ebitda < 2.0:
            fortalezas.append(f"**Balance sólido**: Apalancamiento {ratio_deuda_ebitda:.1f}x proporciona flexibilidad financiera")
        elif ratio_deuda_ebitda < 3.0:
            fortalezas.append(f"**Deuda controlada**: Ratio {ratio_deuda_ebitda:.1f}x dentro de parámetros prudentes")
            
        if roce > 15:
            fortalezas.append(f"**Creación de valor sostenible**: ROCE {roce:.0f}% supera coste de capital")
            
        if fcf_yield > 5:
            fortalezas.append(f"**Generación de caja atractiva**: FCF yield {fcf_yield:.1f}% permite retornos estables")
            
        # RIESGOS - Perspectiva conservadora
        if cagr_ventas < 3:
            riesgos.append(f"**Crecimiento débil {cagr_ventas:.1f}%**: Posible pérdida de cuota de mercado")
            
        if ratio_deuda_ebitda > 3.5:
            riesgos.append(f"**Apalancamiento elevado {ratio_deuda_ebitda:.1f}x**: Limita flexibilidad ante crisis")
    
    return {
        'fortalezas': fortalezas[:5],  # Top 5
        'riesgos': riesgos[:3],  # Top 3
        'metodo': metodo
    }

def generar_hoja_ruta_valor(datos, metodo='estandar'):
    """
    Genera hoja de ruta para creación de valor adaptada al método
    """
    
    valor_empresa = datos.get('valor_empresa', 0)
    ebitda_actual = datos.get('ebitda_actual', 0)
    ventas_actuales = datos.get('ventas_actuales', 0)
    ratio_deuda_ebitda = datos.get('ratio_deuda_ebitda', 0)
    margen_ebitda = datos.get('margen_ebitda', 0)
    benchmark_sector = datos.get('benchmark_sector', 15)
    cash_cycle = datos.get('cash_cycle', 45)
    ev_ebitda = datos.get('ev_ebitda', 0)
    
    prioridades_corto = []
    palancas_medio = []
    opciones_salida = []
    
    if metodo == 'mckinsey':
        # HOJA DE RUTA AGRESIVA - Enfoque PE/Growth
        
        # Prioridades 0-12M
        if ratio_deuda_ebitda < 2:
            dividend_recap = min(valor_empresa * 0.4, ebitda_actual * 3)
            prioridades_corto.append(f"💰 **Dividend Recap inmediato**: Extraer €{dividend_recap:,.0f} vía LBO hasta 4x Deuda/EBITDA")
        
        prioridades_corto.append(f"🎯 **100-day plan agresivo**: Target +20% EBITDA vía pricing power y ZBB")
        
        if cash_cycle > 30:
            wc_liberacion = ventas_actuales * 0.05
            prioridades_corto.append(f"💵 **Quick win capital trabajo**: Liberar €{wc_liberacion:,.0f} optimizando términos")
        
        # Palancas 1-3A
        palancas_medio.append(f"🚀 **Buy-and-build agresivo**: 3-5 bolt-ons anuales para consolidación sectorial")
        palancas_medio.append(f"🌍 **Expansión internacional rápida**: Réplica modelo en 2-3 mercados core")
        palancas_medio.append(f"💻 **Transformación digital profunda**: Target 30% margen via IA/automatización")
        
        # Salida 3-5A
        if ebitda_actual > 10000000:
            opciones_salida.append(f"📊 **Dual-track process**: IPO o venta estratégica a {ev_ebitda*1.5:.1f}x")
        else:
            opciones_salida.append(f"🤝 **Secondary buyout**: Venta a PE larger-cap a {ev_ebitda*1.3:.1f}x")
        
        opciones_salida.append(f"💼 **Trade sale con sinergias**: Valoración {valor_empresa*1.5:,.0f} con premio control")
        
    else:
        # HOJA DE RUTA CONSERVADORA - Enfoque value/estable
        
        # Prioridades 0-12M
        if ratio_deuda_ebitda > 3:
            prioridades_corto.append(f"💰 **Reducción deuda prioritaria**: Bajar a 2.5x en 12 meses")
        else:
            prioridades_corto.append(f"💰 **Política dividendos estable**: Payout 30-40% del FCF")
            
        if cash_cycle > 60:
            prioridades_corto.append(f"📊 **Optimización capital trabajo**: Reducir ciclo a 45 días")
        
        # Palancas 1-3A
        if margen_ebitda < benchmark_sector:
            palancas_medio.append(f"📈 **Plan mejora márgenes**: Alcanzar {benchmark_sector}% vía eficiencias")
        
        palancas_medio.append(f"🌱 **Crecimiento orgánico sostenible**: CAGR 5-7% con inversión moderada")
        palancas_medio.append(f"💻 **Digitalización gradual**: Mejora 5-10% productividad")
        
        # Salida 3-5A
        if ev_ebitda < 10:
            opciones_salida.append(f"💼 **Venta a competidor**: Re-rating a {10:.1f}x múltiplo sector")
        
        if ebitda_actual > 5000000:
            opciones_salida.append(f"📊 **Preparación para mercado**: Profesionalización para venta institucional")
        else:
            opciones_salida.append(f"🤝 **MBO/Sucesión familiar**: Transición ordenada con financiación bancaria")
    
    return {
        'prioridades_corto': prioridades_corto[:3],
        'palancas_medio': palancas_medio[:3],
        'opciones_salida': opciones_salida[:3]
    }
