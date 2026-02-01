"""
Procesador de Datos - Parroquia Santiago Apóstol de Huancané
Procesa archivos Excel de caja parroquial y genera datos consolidados
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ProcesadorParroquial:
    def __init__(self, ruta_datos):
        self.ruta_datos = Path(ruta_datos)
        self.datos_consolidados = []
        self.categorias = {
            'MISA': ['MISA', 'EXEQUIA'],
            'SACRAMENTO': ['BAUTISMO', 'MATRIMONIO', 'CONFIRMACION', 'CONFIRMACIÓN'],
            'DOCUMENTO': ['PARTIDA', 'CONSTANCIA', 'FUT', 'CERTIFICADO'],
            'OTROS': []
        }
        
    def categorizar_servicio(self, detalle):
        """Categoriza el tipo de servicio basado en el detalle"""
        if pd.isna(detalle):
            return 'OTROS'
        
        detalle_upper = str(detalle).upper()
        
        for categoria, palabras_clave in self.categorias.items():
            if any(palabra in detalle_upper for palabra in palabras_clave):
                return categoria
        
        return 'OTROS'
    
    def subcategorizar_misa(self, detalle):
        """Subcategoriza los tipos de misa"""
        if pd.isna(detalle):
            return 'OTROS'
        
        detalle_upper = str(detalle).upper()
        
        if 'ALMA' in detalle_upper:
            return 'MISA DE ALMA'
        elif 'SALUD' in detalle_upper:
            return 'MISA DE SALUD'
        elif 'CHACRA' in detalle_upper:
            return 'MISA DE CHACRA'
        elif 'EXEQUIA' in detalle_upper:
            return 'MISA DE EXEQUIAS'
        elif 'ANIVERSARIO' in detalle_upper:
            return 'MISA DE ANIVERSARIO'
        elif 'FIESTA' in detalle_upper:
            return 'MISA DE FIESTA'
        else:
            return 'MISA PARTICULAR'
    
    def limpiar_fecha(self, fecha_raw, archivo_nombre=None):
        """
        Limpia y estandariza las fechas con lógica avanzada de recuperación.
        Propaga el año si falta, basándose en el nombre del archivo.
        """
        if pd.isna(fecha_raw):
            return None
            
        # Intentar determinar año desde el nombre del archivo
        año_archivo = None
        if archivo_nombre:
            if '2024' in archivo_nombre:
                año_archivo = 2024
            elif '2025' in archivo_nombre:
                año_archivo = 2025

        fecha_dt = None

        # Caso 1: Es un objeto datetime
        if isinstance(fecha_raw, datetime):
            fecha_dt = fecha_raw

        # Caso 2: Es un string (texto)
        elif isinstance(fecha_raw, str):
            fecha_limpia = str(fecha_raw).strip()
            # Patrones comunes
            formatos = [
                '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', 
                '%d/%m/%y', '%d-%m-%y',
                '%d.%m.%Y', '%Y.%m.%d'
            ]
            
            for fmt in formatos:
                try:
                    fecha_dt = datetime.strptime(fecha_limpia.split()[0], fmt) # Split por si tiene hora
                    break
                except:
                    continue
            
            # Intento de corrección inteligente si falla formato (ej: excel a veces pone comas)
            if not fecha_dt:
                try:
                    tokens = re.findall(r'\d+', fecha_limpia)
                    if len(tokens) >= 3:
                        d, m, y = int(tokens[0]), int(tokens[1]), int(tokens[2])
                        # Ajuste de año corto
                        if y < 100: y += 2000
                        fecha_dt = datetime(y, m, d)
                except:
                    pass

        # Caso 3: Es un número (Excel serial date)
        elif isinstance(fecha_raw, (int, float)):
            try:
                # Excel base date (win)
                fecha_dt = pd.to_datetime(fecha_raw, origin='1899-12-30', unit='D')
            except:
                pass

        # VALIDACIÓN Y CORRECCIÓN DE AÑO
        if fecha_dt:
            # Si la fecha se leyó pero el año parece incorrecto (ej: 1900) y sabemos el año del archivo
            if año_archivo and (fecha_dt.year < 2000 or fecha_dt.year != año_archivo):
                 # Forzamos el año correcto si el mes coincide o es razonable
                 try:
                    fecha_dt = fecha_dt.replace(year=año_archivo)
                 except ValueError:
                    pass # Caso bisiesto fallido, etc.
            
            return fecha_dt

        return None
    
    def procesar_archivo(self, archivo_path):
        """Procesa un archivo Excel individual con mayor tolerancia a formatos"""
        print(f"Procesando: {archivo_path.name}")
        
        try:
            # Leer archivo con pandas (auto-detect engine)
            # Usamos header=None primero para detectar donde empieza la tabla real
            if archivo_path.suffix == '.xls':
                df_raw = pd.read_excel(archivo_path, engine='xlrd', header=None)
            else:
                df_raw = pd.read_excel(archivo_path, engine='openpyxl', header=None)
            
            # Buscar la fila de encabezado
            fila_encabezado = -1
            columnas_detectadas = {}
            
            for idx, row in df_raw.iterrows():
                row_str = row.astype(str).str.upper().tolist()
                # Buscamos palabras clave
                if any('FECHA' in str(x) for x in row_str) and \
                   (any('DETALLE' in str(x) for x in row_str) or any('CONCEPTO' in str(x) for x in row_str)):
                    fila_encabezado = idx
                    break
            
            if fila_encabezado == -1:
                # Si no encuentra encabezados claros, asume estructura fija típica (fila 7 u 8)
                fila_encabezado = 7 
            
            # Recargar con el encabezado correcto
            if archivo_path.suffix == '.xls':
                df = pd.read_excel(archivo_path, engine='xlrd', header=fila_encabezado)
            else:
                df = pd.read_excel(archivo_path, engine='openpyxl', header=fila_encabezado)

            # Normalizar columnas
            cols_map = {}
            for col in df.columns:
                col_str = str(col).upper().strip()
                if 'FECHA' in col_str: cols_map['fecha'] = col
                elif 'DETALLE' in col_str or 'CONCEPTO' in col_str: cols_map['detalle'] = col
                elif 'INGRESO' in col_str: cols_map['ingreso'] = col
                elif 'EGRESO' in col_str: cols_map['egreso'] = col
            
            if not 'detalle' in cols_map: # Fallback posicional
                cols = df.columns
                if len(cols) > 0: cols_map['fecha'] = cols[0]
                if len(cols) > 2: cols_map['detalle'] = cols[2]
                if len(cols) > 3: cols_map['ingreso'] = cols[3]
                if len(cols) > 4: cols_map['egreso'] = cols[4]

            # Procesar filas
            registros = []
            ultimo_dia_valido = None # Para rellenar fechas vacías (fill down)
            
            # Detectar año/mes del archivo para validación
            nombre_archivo = archivo_path.stem.upper()
            año_archivo = 2024 if '2024' in nombre_archivo else 2025
            mes_archivo = None
            for m_nombre, m_num in {
                'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4,
                'MAYO': 5, 'JUNIO': 6, 'JULIO': 7, 'AGOSTO': 8,
                'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
            }.items():
                if m_nombre in nombre_archivo:
                    mes_archivo = m_num
                    break

            for idx, row in df.iterrows():
                # Obtener detalle
                col_det = cols_map.get('detalle')
                detalle = row[col_det] if col_det in row else None
                
                # Descartar filas irrelevantes
                if pd.isna(detalle) or str(detalle).strip() == '': continue
                det_upper = str(detalle).upper()
                if 'TOTAL' in det_upper or 'SALDO' in det_upper or 'ANTERIOR' in det_upper: continue
                if 'VACACIONES' in det_upper: continue # Probable fila administrativa sin monto

                # Obtener montos
                col_ing = cols_map.get('ingreso')
                col_egr = cols_map.get('egreso')
                
                ingreso = pd.to_numeric(row[col_ing], errors='coerce') if col_ing in row else 0
                egreso = pd.to_numeric(row[col_egr], errors='coerce') if col_egr in row else 0
                
                ingreso = ingreso if not pd.isna(ingreso) else 0
                egreso = egreso if not pd.isna(egreso) else 0
                
                if ingreso == 0 and egreso == 0: continue

                # Procesar Fecha
                col_fec = cols_map.get('fecha')
                fecha_raw = row[col_fec] if col_fec in row else None
                fecha = self.limpiar_fecha(fecha_raw, archivo_nombre=nombre_archivo)
                
                # Lógica de "Fill Down" para fechas vacías en grupos
                if fecha:
                    ultimo_dia_valido = fecha
                elif ultimo_dia_valido and pd.isna(fecha_raw):
                    fecha = ultimo_dia_valido
                
                # Fallback final de fecha: usar el mes/año del archivo y día 1 (o último dia mes)
                # Solo si es crítico, pero mejor dejar None si no estamos seguros para no ensuciar data.
                if not fecha and mes_archivo and año_archivo:
                     # Si no hay fecha, asignamos al mes del archivo para que al menos cuente en el mes
                     fecha = datetime(año_archivo, mes_archivo, 1)

                if fecha:
                    categoria = self.categorizar_servicio(detalle)
                    subcategoria = None
                    if categoria == 'MISA': subcategoria = self.subcategorizar_misa(detalle)
                    elif categoria == 'SACRAMENTO':
                         if 'BAUTISMO' in det_upper: subcategoria = 'BAUTISMO'
                         elif 'MATRIMONIO' in det_upper: subcategoria = 'MATRIMONIO'
                         elif 'CONFIRMACI' in det_upper: subcategoria = 'CONFIRMACIÓN'
                    elif categoria == 'DOCUMENTO':
                         if 'PARTIDA' in det_upper: subcategoria = 'PARTIDA'
                         elif 'CONSTANCIA' in det_upper: subcategoria = 'CONSTANCIA'

                    registros.append({
                        'fecha': fecha,
                        'año': fecha.year,
                        'mes': fecha.month,
                        'detalle': str(detalle).strip(),
                        'categoria': categoria,
                        'subcategoria': subcategoria if subcategoria else categoria, # Fallback
                        'ingreso': ingreso,
                        'egreso': egreso,
                        'archivo': archivo_path.name
                    })

            print(f"  ✓ {len(registros)} registros recuperados")
            return registros
            
        except Exception as e:
            print(f"  ✗ Error crítico en {archivo_path.name}: {str(e)}")
            return []
    
    def procesar_todos(self):
        """Procesa todos los archivos Excel en la carpeta"""
        archivos = sorted(self.ruta_datos.glob("*.xls*"))
        
        print(f"\n{'='*60}")
        print(f"PROCESANDO {len(archivos)} ARCHIVOS")
        print(f"{'='*60}\n")
        
        for archivo in archivos:
            registros = self.procesar_archivo(archivo)
            self.datos_consolidados.extend(registros)
        
        # Crear DataFrame consolidado
        df = pd.DataFrame(self.datos_consolidados)
        
        print(f"\n{'='*60}")
        print(f"RESUMEN DE PROCESAMIENTO")
        print(f"{'='*60}")
        print(f"Total de registros: {len(df)}")
        print(f"Período: {df['año'].min()} - {df['año'].max()}")
        print(f"Total ingresos: S/ {df['ingreso'].sum():,.2f}")
        print(f"Total egresos: S/ {df['egreso'].sum():,.2f}")
        print(f"Balance: S/ {(df['ingreso'].sum() - df['egreso'].sum()):,.2f}")
        
        return df
    
    def generar_estadisticas(self, df):
        """Genera estadísticas detalladas"""
        stats = {}
        
        # Por año
        stats['por_año'] = df.groupby('año').agg({
            'ingreso': 'sum',
            'egreso': 'sum'
        }).round(2)
        stats['por_año']['balance'] = stats['por_año']['ingreso'] - stats['por_año']['egreso']
        
        # Por mes
        stats['por_mes'] = df.groupby(['año', 'mes']).agg({
            'ingreso': 'sum',
            'egreso': 'sum'
        }).round(2)
        
        # Por categoría
        stats['por_categoria'] = df.groupby('categoria').agg({
            'ingreso': 'sum',
            'egreso': 'sum'
        }).round(2)
        stats['por_categoria']['cantidad'] = df.groupby('categoria').size()
        
        # Por subcategoría
        stats['por_subcategoria'] = df[df['subcategoria'].notna()].groupby('subcategoria').agg({
            'ingreso': 'sum',
            'egreso': 'sum'
        }).round(2)
        stats['por_subcategoria']['cantidad'] = df[df['subcategoria'].notna()].groupby('subcategoria').size()
        
        return stats

# Ejecutar procesamiento
if __name__ == "__main__":
    procesador = ProcesadorParroquial(r"C:\Users\FELIX\.gemini\antigravity\scratch\parroquia_huancane\datos")
    df = procesador.procesar_todos()
    
    # Guardar datos consolidados
    df.to_csv(r"C:\Users\FELIX\.gemini\antigravity\scratch\parroquia_huancane\datos_consolidados.csv", 
              index=False, encoding='utf-8-sig')
    df.to_excel(r"C:\Users\FELIX\.gemini\antigravity\scratch\parroquia_huancane\datos_consolidados.xlsx", 
                index=False)
    
    # Generar estadísticas
    stats = procesador.generar_estadisticas(df)
    
    print(f"\n{'='*60}")
    print("ESTADÍSTICAS POR AÑO")
    print(f"{'='*60}")
    print(stats['por_año'])
    
    print(f"\n{'='*60}")
    print("ESTADÍSTICAS POR CATEGORÍA")
    print(f"{'='*60}")
    print(stats['por_categoria'])
    
    print(f"\n✓ Datos guardados en 'datos_consolidados.csv' y 'datos_consolidados.xlsx'")
