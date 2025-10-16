#!/usr/bin/env python3
"""
Agregar todos los campos faltantes a las empresas demo que no los tienen
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Para TechStart SaaS - buscar donde agregar los campos
for i, line in enumerate(lines):
    if 'elif empresa_demo == "💻 TechStart SaaS":' in line:
        print(f"Encontrado TechStart en línea {i+1}")
        
        # Buscar donde termina ventaja_competitiva_principal
        for j in range(i+10, min(i+50, len(lines))):
            if "'ventaja_competitiva_principal':" in lines[j] and "'principales_riesgos':" in lines[j+1]:
                print(f"  Insertando campos después de línea {j+1}")
                
                # Insertar los campos faltantes
                nuevos_campos = """                'descripcion_actividad': 'Plataforma CRM cloud diseñada específicamente para PYMES españolas. Gestión de clientes, pipeline de ventas, automatización de marketing y analíticas en tiempo real.',
                'productos_servicios': 'Plan Básico (gratis hasta 3 usuarios), Plan Profesional (29€/usuario/mes), Plan Enterprise (59€/usuario/mes), servicios de onboarding y consultoría',
                'cuota_mercado': 8.5,
                'ventajas_competitivas': 'Interfaz 100% en español, cumplimiento RGPD nativo, integración con gestorías españolas, soporte 24/7 en español, precio 50% menor que competidores',
                'clientes_objetivo': 'PYMES españolas 10-100 empleados, startups en crecimiento, equipos comerciales, empresas B2B con proceso de venta complejo, consultoras y agencias',
"""
                lines[j+1] = lines[j+1].rstrip() + ',\n' + nuevos_campos + lines[j+1].lstrip()
                break
        break

# Para ModaOnline Shop
for i, line in enumerate(lines):
    if 'elif empresa_demo == "🛍️ ModaOnline Shop":' in line:
        print(f"Encontrado ModaOnline en línea {i+1}")
        
        # Buscar donde termina ventaja_competitiva_principal
        for j in range(i+10, min(i+50, len(lines))):
            if "'ventaja_competitiva_principal':" in lines[j] and "'principales_riesgos':" in lines[j+1]:
                print(f"  Insertando campos después de línea {j+1}")
                
                nuevos_campos = """                'descripcion_actividad': 'E-commerce de moda sostenible con curación de marcas europeas. Tecnología de recomendación por IA, servicio de personal shopper y programa de fidelización.',
                'productos_servicios': 'Ropa mujer (60%), hombre (25%), accesorios (15%). Servicio personal shopper online, suscripción premium con envíos gratis y descuentos exclusivos',
                'cuota_mercado': 2.3,
                'ventajas_competitivas': 'Marcas sostenibles exclusivas, entrega en 24h garantizada, devoluciones gratuitas 60 días, personal shopper por IA, programa de reciclaje textil',
                'clientes_objetivo': 'Mujeres 25-40 años urbanas, conciencia ecológica, renta media-alta, early adopters de moda, profesionales que valoran calidad y sostenibilidad',
"""
                lines[j+1] = lines[j+1].rstrip() + ',\n' + nuevos_campos + lines[j+1].lstrip()
                break
        break

# Para MetalPro Industrial
for i, line in enumerate(lines):
    if 'elif empresa_demo == "🏭 MetalPro Industrial":' in line:
        print(f"Encontrado MetalPro en línea {i+1}")
        
        # Buscar donde termina ventaja_competitiva_principal
        for j in range(i+10, min(i+50, len(lines))):
            if "'ventaja_competitiva_principal':" in lines[j] and "'principales_riesgos':" in lines[j+1]:
                print(f"  Insertando campos después de línea {j+1}")
                
                nuevos_campos = """                'descripcion_actividad': 'Fabricación de componentes metálicos de alta precisión para automoción y aeronáutica. Especialistas en aleaciones especiales y tratamientos térmicos avanzados.',
                'productos_servicios': 'Piezas forjadas para motor, componentes aeronáuticos certificados, servicios de mecanizado CNC, prototipado rápido, ingeniería de diseño colaborativo',
                'cuota_mercado': 12.0,
                'ventajas_competitivas': 'Certificaciones aeronáuticas NADCAP, tecnología de forja en caliente única, entregas JIT garantizadas, departamento I+D con 15 ingenieros, 30 años de experiencia',
                'clientes_objetivo': 'OEMs automoción (Seat, VW, Ford), Tier 1 aeronáutica (Airbus, ITP Aero), fabricantes de maquinaria industrial, empresas de defensa',
"""
                lines[j+1] = lines[j+1].rstrip() + ',\n' + nuevos_campos + lines[j+1].lstrip()
                break
        break

# Ahora arreglar el modelo_negocio de MetalPro que debe ser B2B
for i, line in enumerate(lines):
    if "'modelo_negocio': 'Fabricación - Producción propia'" in line:
        lines[i] = line.replace("'Fabricación - Producción propia'", "'B2B - Venta a empresas'")
        print(f"Corregido modelo_negocio de MetalPro en línea {i+1}")

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Campos agregados a todas las empresas demo")

