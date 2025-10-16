# Términos que deberían estar en el glosario
terminos_importantes = {
    "Ratio de Apalancamiento": "Acabamos de renombrarlo, debería estar",
    "Fondo de Maniobra": "Capital de trabajo operativo",
    "Autonomía Financiera": "% del activo financiado con recursos propios",
    "CAGR": "Compound Annual Growth Rate - Tasa de crecimiento anual compuesto",
    "Break-even": "Punto de equilibrio donde ingresos = gastos",
    "Burn Rate": "Velocidad de consumo de caja",
    "Runway": "Meses de caja disponible al ritmo actual de gasto",
    "LTV": "Lifetime Value - Valor del cliente en su ciclo de vida",
    "CAC": "Customer Acquisition Cost - Coste de adquisición de cliente",
    "Churn Rate": "Tasa de pérdida de clientes",
    "MRR": "Monthly Recurring Revenue - Ingresos recurrentes mensuales",
    "ARR": "Annual Recurring Revenue - Ingresos recurrentes anuales"
}

print("=== TÉRMINOS QUE PODRÍAN AGREGARSE AL GLOSARIO ===\n")
for termino, descripcion in terminos_importantes.items():
    print(f"• {termino}: {descripcion}")

print("\n✅ TÉRMINOS YA INCLUIDOS:")
print("• EBITDA, FCF, WACC, DCF, ROE, ROCE, DSO, DPO")
print("• Working Capital, Liquidity Ratio, Debt-to-Equity")
print("• IRR, NPV, Payback, Terminal Value")
