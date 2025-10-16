"""
Corrección de la hoja de líneas de financiación para permitir múltiples líneas
"""

def crear_hoja_lineas_financiacion_mejorada(writer):
    """Hoja 7: Líneas Financiación - Permite múltiples líneas del mismo tipo"""
    
    # Crear estructura con múltiples filas para cada tipo
    tipos_lineas = [
        'Póliza de Crédito',
        'Póliza Crédito Stock',
        'Descuento Comercial',
        'Anticipo de Facturas',
        'Factoring con Recurso',
        'Factoring sin Recurso',
        'Confirming Proveedores',
        'Pagarés Empresa',
        'Crédito Importación',
        'Otras líneas'
    ]
    
    # Crear 3 filas para cada tipo de línea (30 líneas en total)
    data = []
    data.append(['--- INSTRUCCIONES: Puede agregar múltiples líneas del mismo tipo ---', '', '', '', '', ''])
    
    for tipo in tipos_lineas:
        for i in range(3):  # 3 líneas posibles de cada tipo
            if i == 0:
                data.append([tipo, '', 0, 0, 0, 0])
            else:
                data.append(['', '', 0, 0, 0, 0])  # Líneas adicionales vacías
    
    # Agregar filas extras para otros tipos
    data.append(['', '', '', '', '', ''])
    data.append(['--- LÍNEAS ADICIONALES (especificar tipo) ---', '', '', '', '', ''])
    for i in range(5):  # 5 líneas extras para tipos no listados
        data.append(['', '', 0, 0, 0, 0])
    
    df = pd.DataFrame(data, columns=['Tipo de Línea', 'Banco/Entidad', 'Límite', 'Dispuesto', 'Tipo (%)', 'Comisión (%)'])
    df.to_excel(writer, sheet_name='Líneas Financiación', index=False)
