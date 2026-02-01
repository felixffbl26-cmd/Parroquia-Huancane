"""
Analizador Profundo de Datos Excel - Parroquia Huancané
Genera un informe detallado de calidad y estructura de datos
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import warnings
warnings.filterwarnings('ignore')

class AnalizadorExcelProfundo:
    def __init__(self, ruta_datos):
        self.ruta_datos = Path(ruta_datos)
        self.reportes = []
        self.problemas_globales = []
        self.estadisticas_globales = {}
        
    def analizar_archivo(self, archivo_path):
        """Análisis profundo de un archivo Excel individual"""
        print(f"\n{'='*80}")
        print(f"📄 ANALIZANDO: {archivo_path.name}")
        print(f"{'='*80}")
        
        reporte = {
            'archivo': archivo_path.name,
            'ruta': str(archivo_path),
            'tamaño_kb': archivo_path.stat().st_size / 1024,
            'fecha_modificacion': datetime.fromtimestamp(archivo_path.stat().st_mtime),
            'problemas': [],
            'advertencias': [],
            'estadisticas': {},
            'calidad_datos': 0
        }
        
        try:
            # Leer archivo
            if archivo_path.suffix == '.xls':
                df = pd.read_excel(archivo_path, engine='xlrd')
            else:
                df = pd.read_excel(archivo_path, engine='openpyxl')
            
            print(f"✓ Archivo leído exitosamente")
            print(f"  Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            
            # 1. ANÁLISIS DE ESTRUCTURA
            print(f"\n📊 ANÁLISIS DE ESTRUCTURA:")
            reporte['estadisticas']['filas_totales'] = len(df)
            reporte['estadisticas']['columnas_totales'] = len(df.columns)
            
            # Detectar columnas
            columnas_detectadas = {}
            for col in df.columns:
                col_str = str(col).upper().strip()
                if 'FECHA' in col_str:
                    columnas_detectadas['fecha'] = col
                elif 'DETALLE' in col_str or 'CONCEPTO' in col_str:
                    columnas_detectadas['detalle'] = col
                elif 'INGRESO' in col_str:
                    columnas_detectadas['ingreso'] = col
                elif 'EGRESO' in col_str:
                    columnas_detectadas['egreso'] = col
            
            print(f"  Columnas detectadas: {list(columnas_detectadas.keys())}")
            reporte['estadisticas']['columnas_detectadas'] = list(columnas_detectadas.keys())
            
            if len(columnas_detectadas) < 3:
                reporte['problemas'].append("⚠️ CRÍTICO: No se detectaron todas las columnas necesarias")
            
            # 2. ANÁLISIS DE FECHAS
            if 'fecha' in columnas_detectadas:
                print(f"\n📅 ANÁLISIS DE FECHAS:")
                col_fecha = columnas_detectadas['fecha']
                fechas_validas = 0
                fechas_invalidas = 0
                fechas_futuras = 0
                fechas_antiguas = 0
                
                for idx, fecha_raw in enumerate(df[col_fecha]):
                    if pd.notna(fecha_raw):
                        try:
                            if isinstance(fecha_raw, datetime):
                                fecha = fecha_raw
                            elif isinstance(fecha_raw, str):
                                fecha = pd.to_datetime(fecha_raw, errors='coerce')
                            elif isinstance(fecha_raw, (int, float)):
                                fecha = pd.to_datetime(fecha_raw, origin='1899-12-30', unit='D', errors='coerce')
                            else:
                                fecha = None
                            
                            if fecha and not pd.isna(fecha):
                                fechas_validas += 1
                                # Validar rango
                                if fecha.year < 2020:
                                    fechas_antiguas += 1
                                elif fecha > datetime.now():
                                    fechas_futuras += 1
                            else:
                                fechas_invalidas += 1
                        except:
                            fechas_invalidas += 1
                
                print(f"  ✓ Fechas válidas: {fechas_validas}")
                print(f"  ✗ Fechas inválidas: {fechas_invalidas}")
                if fechas_futuras > 0:
                    print(f"  ⚠️ Fechas futuras: {fechas_futuras}")
                    reporte['advertencias'].append(f"Hay {fechas_futuras} fechas futuras")
                if fechas_antiguas > 0:
                    print(f"  ⚠️ Fechas anteriores a 2020: {fechas_antiguas}")
                    reporte['advertencias'].append(f"Hay {fechas_antiguas} fechas anteriores a 2020")
                
                reporte['estadisticas']['fechas_validas'] = fechas_validas
                reporte['estadisticas']['fechas_invalidas'] = fechas_invalidas
            
            # 3. ANÁLISIS DE MONTOS
            print(f"\n💰 ANÁLISIS DE MONTOS:")
            
            if 'ingreso' in columnas_detectadas:
                col_ing = columnas_detectadas['ingreso']
                ingresos = pd.to_numeric(df[col_ing], errors='coerce')
                ingresos_validos = ingresos[ingresos.notna()]
                
                print(f"  INGRESOS:")
                print(f"    Total registros: {len(ingresos_validos)}")
                print(f"    Suma total: S/ {ingresos_validos.sum():,.2f}")
                print(f"    Promedio: S/ {ingresos_validos.mean():,.2f}")
                print(f"    Mínimo: S/ {ingresos_validos.min():,.2f}")
                print(f"    Máximo: S/ {ingresos_validos.max():,.2f}")
                print(f"    Desv. estándar: S/ {ingresos_validos.std():,.2f}")
                
                # Detectar valores atípicos (outliers)
                Q1 = ingresos_validos.quantile(0.25)
                Q3 = ingresos_validos.quantile(0.75)
                IQR = Q3 - Q1
                outliers_ing = ingresos_validos[(ingresos_validos < (Q1 - 1.5 * IQR)) | 
                                                (ingresos_validos > (Q3 + 1.5 * IQR))]
                
                if len(outliers_ing) > 0:
                    print(f"    ⚠️ Valores atípicos detectados: {len(outliers_ing)}")
                    print(f"       Valores: {sorted(outliers_ing.values, reverse=True)[:5]}")
                    reporte['advertencias'].append(f"{len(outliers_ing)} ingresos atípicos detectados")
                
                # Validar negativos
                negativos = ingresos_validos[ingresos_validos < 0]
                if len(negativos) > 0:
                    print(f"    ❌ PROBLEMA: {len(negativos)} ingresos negativos")
                    reporte['problemas'].append(f"Hay {len(negativos)} ingresos con valores negativos")
                
                reporte['estadisticas']['ingresos_total'] = float(ingresos_validos.sum())
                reporte['estadisticas']['ingresos_promedio'] = float(ingresos_validos.mean())
                reporte['estadisticas']['ingresos_max'] = float(ingresos_validos.max())
                reporte['estadisticas']['ingresos_outliers'] = len(outliers_ing)
            
            if 'egreso' in columnas_detectadas:
                col_egr = columnas_detectadas['egreso']
                egresos = pd.to_numeric(df[col_egr], errors='coerce')
                egresos_validos = egresos[egresos.notna()]
                
                print(f"\n  EGRESOS:")
                print(f"    Total registros: {len(egresos_validos)}")
                print(f"    Suma total: S/ {egresos_validos.sum():,.2f}")
                print(f"    Promedio: S/ {egresos_validos.mean():,.2f}")
                print(f"    Mínimo: S/ {egresos_validos.min():,.2f}")
                print(f"    Máximo: S/ {egresos_validos.max():,.2f}")
                
                # Detectar negativos
                negativos = egresos_validos[egresos_validos < 0]
                if len(negativos) > 0:
                    print(f"    ❌ PROBLEMA: {len(negativos)} egresos negativos")
                    reporte['problemas'].append(f"Hay {len(negativos)} egresos con valores negativos")
                
                reporte['estadisticas']['egresos_total'] = float(egresos_validos.sum())
                reporte['estadisticas']['egresos_promedio'] = float(egresos_validos.mean())
            
            # 4. ANÁLISIS DE DETALLES
            if 'detalle' in columnas_detectadas:
                print(f"\n📝 ANÁLISIS DE DETALLES:")
                col_det = columnas_detectadas['detalle']
                detalles_vacios = df[col_det].isna().sum()
                detalles_unicos = df[col_det].nunique()
                
                print(f"  Detalles únicos: {detalles_unicos}")
                print(f"  Detalles vacíos: {detalles_vacios}")
                
                if detalles_vacios > 0:
                    reporte['advertencias'].append(f"{detalles_vacios} registros sin detalle")
                
                # Detectar duplicados exactos
                duplicados = df[df.duplicated(subset=[col_det], keep=False)]
                if len(duplicados) > 0:
                    print(f"  ⚠️ Posibles duplicados: {len(duplicados)} registros")
                    reporte['advertencias'].append(f"{len(duplicados)} posibles registros duplicados")
                
                reporte['estadisticas']['detalles_unicos'] = detalles_unicos
                reporte['estadisticas']['detalles_vacios'] = detalles_vacios
            
            # 5. VALIDACIÓN DE BALANCE
            if 'ingreso' in columnas_detectadas and 'egreso' in columnas_detectadas:
                print(f"\n⚖️ VALIDACIÓN DE BALANCE:")
                total_ing = ingresos_validos.sum()
                total_egr = egresos_validos.sum()
                balance = total_ing - total_egr
                
                print(f"  Total Ingresos: S/ {total_ing:,.2f}")
                print(f"  Total Egresos:  S/ {total_egr:,.2f}")
                print(f"  Balance:        S/ {balance:,.2f}")
                
                if balance < 0:
                    print(f"  ⚠️ Balance negativo en este archivo")
                    reporte['advertencias'].append("Balance negativo en el archivo")
                
                reporte['estadisticas']['balance'] = float(balance)
            
            # 6. CALIDAD DE DATOS (Score 0-100)
            puntos = 100
            if len(reporte['problemas']) > 0:
                puntos -= len(reporte['problemas']) * 20
            if len(reporte['advertencias']) > 0:
                puntos -= len(reporte['advertencias']) * 5
            if fechas_invalidas > 0:
                puntos -= min(fechas_invalidas * 2, 20)
            
            reporte['calidad_datos'] = max(0, puntos)
            
            print(f"\n📊 CALIDAD DE DATOS: {reporte['calidad_datos']}/100")
            
            if reporte['calidad_datos'] >= 80:
                print(f"   ✅ EXCELENTE")
            elif reporte['calidad_datos'] >= 60:
                print(f"   ⚠️ BUENA (con advertencias)")
            else:
                print(f"   ❌ REQUIERE ATENCIÓN")
            
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: {str(e)}")
            reporte['problemas'].append(f"Error al procesar archivo: {str(e)}")
            reporte['calidad_datos'] = 0
        
        self.reportes.append(reporte)
        return reporte
    
    def analizar_todos(self):
        """Analiza todos los archivos Excel en la carpeta"""
        archivos = sorted(self.ruta_datos.glob("*.xls*"))
        
        print(f"\n{'='*80}")
        print(f"🔍 ANÁLISIS PROFUNDO DE DATOS - PARROQUIA HUANCANÉ")
        print(f"{'='*80}")
        print(f"\n📁 Archivos encontrados: {len(archivos)}")
        
        if len(archivos) == 0:
            print(f"\n⚠️ No se encontraron archivos Excel en: {self.ruta_datos}")
            return None
        
        for archivo in archivos:
            self.analizar_archivo(archivo)
        
        # Generar resumen global
        self.generar_resumen_global()
        
        return self.reportes
    
    def generar_resumen_global(self):
        """Genera un resumen consolidado de todos los archivos"""
        print(f"\n{'='*80}")
        print(f"📊 RESUMEN GLOBAL")
        print(f"{'='*80}")
        
        total_archivos = len(self.reportes)
        archivos_excelentes = sum(1 for r in self.reportes if r['calidad_datos'] >= 80)
        archivos_buenos = sum(1 for r in self.reportes if 60 <= r['calidad_datos'] < 80)
        archivos_problematicos = sum(1 for r in self.reportes if r['calidad_datos'] < 60)
        
        print(f"\n📈 CALIDAD GENERAL:")
        print(f"  ✅ Excelente: {archivos_excelentes}/{total_archivos}")
        print(f"  ⚠️ Buena:     {archivos_buenos}/{total_archivos}")
        print(f"  ❌ Problemática: {archivos_problematicos}/{total_archivos}")
        
        # Estadísticas consolidadas
        total_ingresos = sum(r['estadisticas'].get('ingresos_total', 0) for r in self.reportes)
        total_egresos = sum(r['estadisticas'].get('egresos_total', 0) for r in self.reportes)
        balance_global = total_ingresos - total_egresos
        
        print(f"\n💰 TOTALES CONSOLIDADOS:")
        print(f"  Ingresos: S/ {total_ingresos:,.2f}")
        print(f"  Egresos:  S/ {total_egresos:,.2f}")
        print(f"  Balance:  S/ {balance_global:,.2f}")
        
        # Problemas más comunes
        todos_problemas = []
        todas_advertencias = []
        for r in self.reportes:
            todos_problemas.extend(r['problemas'])
            todas_advertencias.extend(r['advertencias'])
        
        if todos_problemas:
            print(f"\n❌ PROBLEMAS CRÍTICOS ENCONTRADOS ({len(todos_problemas)}):")
            for p in set(todos_problemas):
                count = todos_problemas.count(p)
                print(f"  • {p} ({count} archivos)")
        
        if todas_advertencias:
            print(f"\n⚠️ ADVERTENCIAS ({len(todas_advertencias)}):")
            for a in set(todas_advertencias):
                count = todas_advertencias.count(a)
                print(f"  • {a} ({count} archivos)")
        
        self.estadisticas_globales = {
            'total_archivos': total_archivos,
            'archivos_excelentes': archivos_excelentes,
            'archivos_buenos': archivos_buenos,
            'archivos_problematicos': archivos_problematicos,
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'balance_global': balance_global,
            'total_problemas': len(todos_problemas),
            'total_advertencias': len(todas_advertencias)
        }
    
    def generar_informe_html(self, ruta_salida="informe_analisis.html"):
        """Genera un informe HTML detallado"""
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Análisis - Parroquia Huancané</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .archivo {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .calidad-excelente {{ border-left: 5px solid #2ecc71; }}
        .calidad-buena {{ border-left: 5px solid #f39c12; }}
        .calidad-problematica {{ border-left: 5px solid #e74c3c; }}
        .stat {{ 
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 5px;
        }}
        .problema {{ color: #e74c3c; }}
        .advertencia {{ color: #f39c12; }}
        .ok {{ color: #2ecc71; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⛪ Informe de Análisis de Datos</h1>
        <h2>Parroquia Santiago Apóstol de Huancané</h2>
        <p>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Resumen Global</h2>
        <div class="stat">
            <strong>Total Archivos:</strong> {self.estadisticas_globales.get('total_archivos', 0)}
        </div>
        <div class="stat ok">
            <strong>✅ Excelentes:</strong> {self.estadisticas_globales.get('archivos_excelentes', 0)}
        </div>
        <div class="stat advertencia">
            <strong>⚠️ Buenos:</strong> {self.estadisticas_globales.get('archivos_buenos', 0)}
        </div>
        <div class="stat problema">
            <strong>❌ Problemáticos:</strong> {self.estadisticas_globales.get('archivos_problematicos', 0)}
        </div>
        
        <h3>💰 Totales Consolidados</h3>
        <table>
            <tr>
                <th>Concepto</th>
                <th>Monto</th>
            </tr>
            <tr>
                <td>Total Ingresos</td>
                <td class="ok">S/ {self.estadisticas_globales.get('total_ingresos', 0):,.2f}</td>
            </tr>
            <tr>
                <td>Total Egresos</td>
                <td class="problema">S/ {self.estadisticas_globales.get('total_egresos', 0):,.2f}</td>
            </tr>
            <tr>
                <td><strong>Balance</strong></td>
                <td><strong>S/ {self.estadisticas_globales.get('balance_global', 0):,.2f}</strong></td>
            </tr>
        </table>
    </div>
"""
        
        # Agregar detalles de cada archivo
        for reporte in self.reportes:
            calidad_class = 'calidad-excelente' if reporte['calidad_datos'] >= 80 else \
                           'calidad-buena' if reporte['calidad_datos'] >= 60 else \
                           'calidad-problematica'
            
            html += f"""
    <div class="archivo {calidad_class}">
        <h3>📄 {reporte['archivo']}</h3>
        <p><strong>Calidad de Datos:</strong> {reporte['calidad_datos']}/100</p>
        
        <h4>Estadísticas:</h4>
        <ul>
            <li>Filas: {reporte['estadisticas'].get('filas_totales', 'N/A')}</li>
            <li>Ingresos Total: S/ {reporte['estadisticas'].get('ingresos_total', 0):,.2f}</li>
            <li>Egresos Total: S/ {reporte['estadisticas'].get('egresos_total', 0):,.2f}</li>
            <li>Balance: S/ {reporte['estadisticas'].get('balance', 0):,.2f}</li>
        </ul>
"""
            
            if reporte['problemas']:
                html += "<h4 class='problema'>❌ Problemas:</h4><ul>"
                for p in reporte['problemas']:
                    html += f"<li>{p}</li>"
                html += "</ul>"
            
            if reporte['advertencias']:
                html += "<h4 class='advertencia'>⚠️ Advertencias:</h4><ul>"
                for a in reporte['advertencias']:
                    html += f"<li>{a}</li>"
                html += "</ul>"
            
            html += "</div>"
        
        html += """
</body>
</html>
"""
        
        # Guardar archivo
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✅ Informe HTML generado: {ruta_salida}")
        return ruta_salida


# Ejecutar análisis
if __name__ == "__main__":
    analizador = AnalizadorExcelProfundo(r"C:\Users\FELIX\.gemini\antigravity\scratch\parroquia_huancane\datos")
    reportes = analizador.analizar_todos()
    
    if reportes:
        # Generar informe HTML
        analizador.generar_informe_html(
            r"C:\Users\FELIX\.gemini\antigravity\scratch\parroquia_huancane\informes\informe_analisis_datos.html"
        )
        
        print(f"\n{'='*80}")
        print(f"✅ ANÁLISIS COMPLETADO")
        print(f"{'='*80}")
