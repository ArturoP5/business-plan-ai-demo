"""
Extraer componentes WACC exactos que usa la app
"""
from utils.valoracion_mckinsey import ValoracionMcKinsey
from modelo_financiero import ModeloFinanciero

# Crear modelo con datos ODS
modelo = ModeloFinanciero(
    ingresos_iniciales=2_715_239,
    tasa_crecimiento=0.05,
    margen_ebitda=0.133,
    tasa_impositiva=0.25
)

# Params que usa la app (línea 4868 app.py)
params_mck = {
    'tasa_libre_riesgo': 0.03,
    'prima_mercado': 0.055,
    'tasa_impositiva': 0.25,
    'g_terminal': 0.02,
    'target_equity_weight': 0.70,
    'target_debt_weight': 0.30
}

valorador = ValoracionMcKinsey(modelo)
wacc, componentes = valorador.calcular_wacc_mckinsey(params_mck)

print("=" * 80)
print("COMPONENTES WACC - APP")
print("=" * 80)

print(f"\n📊 COSTE DE EQUITY (Ke):")
print(f"  Risk-free (Rf):           {componentes['rf']*100:>6.2f}%")
print(f"  Beta sectorial:           {componentes['beta']:>6.2f}")
print(f"  Prima Mercado:            {componentes['prima_mercado']*100:>6.2f}%")
print(f"  Beta × Prima:             {(componentes['beta'] * componentes['prima_mercado'])*100:>6.2f}%")
print(f"  Prima Tamaño:             {componentes['size_premium']*100:>6.2f}%")
print(f"  Prima PYME:               {componentes.get('prima_pyme', 0)*100:>6.2f}%")
print(f"  Riesgo País:              {componentes['riesgo_pais']*100:>6.2f}%")
print(f"  Riesgo Sector:            {componentes['riesgo_sector']*100:>6.2f}%")
print(f"  ─────────────────────────────────")
print(f"  Ke TOTAL:                 {componentes['cost_of_equity']*100:>6.2f}%")

print(f"\n💰 COSTE DE DEUDA (Kd):")
kd = 0.04  # Hardcoded en valoracion_mckinsey.py
print(f"  Kd antes tax:             {kd*100:>6.2f}%")
print(f"  Kd después tax (25%):     {componentes['cost_of_debt_after_tax']*100:>6.2f}%")

print(f"\n⚖️ ESTRUCTURA CAPITAL:")
print(f"  Peso Equity:              {componentes['weights']['equity']*100:>6.1f}%")
print(f"  Peso Deuda:               {componentes['weights']['debt']*100:>6.1f}%")

print(f"\n📈 WACC FINAL:")
print(f"  WACC:                     {wacc*100:>6.2f}%")

print("\n" + "=" * 80)
print("COMPARACIÓN CON MI CÁLCULO:")
print("=" * 80)

mi_rf = 3.5
mi_beta = 1.1
mi_prima_mercado = 5.5
mi_beta_x_prima = 6.05
mi_prima_tamano = 2.0
mi_riesgo_sector = 0.5
mi_ke = 12.05
mi_wacc = 9.45

print(f"\n{'Componente':<25} {'APP':<12} {'MI CÁLCULO':<12} {'DIFERENCIA':<15}")
print("-" * 70)
print(f"{'Rf':<25} {componentes['rf']*100:>6.2f}%      {mi_rf:>6.2f}%      {(componentes['rf']*100 - mi_rf):>+6.2f}pp")
print(f"{'Beta':<25} {componentes['beta']:>6.2f}       {mi_beta:>6.2f}       {(componentes['beta'] - mi_beta):>+6.2f}")
print(f"{'Prima Mercado':<25} {componentes['prima_mercado']*100:>6.2f}%      {mi_prima_mercado:>6.2f}%      {(componentes['prima_mercado']*100 - mi_prima_mercado):>+6.2f}pp")
print(f"{'Beta × Prima':<25} {(componentes['beta']*componentes['prima_mercado'])*100:>6.2f}%      {mi_beta_x_prima:>6.2f}%      {((componentes['beta']*componentes['prima_mercado'])*100 - mi_beta_x_prima):>+6.2f}pp")
print(f"{'Prima Tamaño':<25} {componentes['size_premium']*100:>6.2f}%      {mi_prima_tamano:>6.2f}%      {(componentes['size_premium']*100 - mi_prima_tamano):>+6.2f}pp")
print(f"{'Riesgo Sector':<25} {componentes['riesgo_sector']*100:>6.2f}%      {mi_riesgo_sector:>6.2f}%      {(componentes['riesgo_sector']*100 - mi_riesgo_sector):>+6.2f}pp")
print(f"{'Ke TOTAL':<25} {componentes['cost_of_equity']*100:>6.2f}%      {mi_ke:>6.2f}%      {(componentes['cost_of_equity']*100 - mi_ke):>+6.2f}pp")
print(f"{'WACC':<25} {wacc*100:>6.2f}%      {mi_wacc:>6.2f}%      {(wacc*100 - mi_wacc):>+6.2f}pp")

print("\n" + "=" * 80)

