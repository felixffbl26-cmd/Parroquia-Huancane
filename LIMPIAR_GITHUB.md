# 🧹 Limpieza de Repositorio GitHub

## ❌ Archivos que DEBES ELIMINAR del Repositorio

### 1. Archivos Python Cache
```bash
git rm -r --cached dashboard/__pycache__
git commit -m "Eliminar cache de Python"
```

### 2. Archivos Temporales (si existen)
- `*.tmp`
- `*.bak`
- `~$*.xlsx`

### 3. Archivos Innecesarios para Deploy

**Archivos .bat (son solo para Windows local):**
```bash
git rm --cached ABRIR_DASHBOARD.bat
git rm --cached ABRIR_DASHBOARD_PREMIUM.bat
git rm --cached ABRIR_EN_NAVEGADOR.bat
git rm --cached ABRIR_WORD.bat
git rm --cached CONFIGURAR_FIREWALL.bat
git rm --cached DASHBOARD_V3.bat
git rm --cached INICIAR.bat
git rm --cached INSTALAR.bat
git rm --cached OBTENER_IP.bat
git rm --cached SOLUCION_CELULAR.bat
git rm --cached URL_PARA_CELULAR.bat
git commit -m "Eliminar scripts .bat innecesarios para deploy"
```

**Archivos de documentación duplicados:**
```bash
git rm --cached COMO_ABRIR_EN_CELULAR.md
git rm --cached RESUMEN_ACCESO_CELULAR.md
git rm --cached SOLUCION_COMPLETA_CELULAR.md
git rm --cached SOLUCION_PROBLEMAS.md
git rm --cached INSTRUCCIONES_RAPIDAS.md
git rm --cached GUIA_PARA_EL_PADRE.md
git commit -m "Eliminar documentación redundante"
```

---

## ✅ Archivos que SÍ DEBEN ESTAR en GitHub

### Esenciales para Streamlit Cloud:
- ✅ `dashboard/app_premium.py` (archivo principal)
- ✅ `datos_consolidados.csv` (datos procesados)
- ✅ `requirements.txt` (dependencias)
- ✅ `.streamlit/config.toml` (configuración)
- ✅ `.gitignore` (nuevo archivo creado)

### Documentación útil:
- ✅ `README_PREMIUM.md` (renombrar a README.md)
- ✅ `GUIA_DEPLOY.md`
- ✅ `INICIO_RAPIDO.md`
- ✅ `INSTALACION.md`

### Opcionales (puedes mantener):
- ⚠️ `dashboard/app.py` (versión anterior - backup)
- ⚠️ `dashboard/app_v3.py` (versión anterior - backup)
- ⚠️ `procesador_datos.py` (útil para actualizar datos)
- ⚠️ `analizar_datos.py` (útil para análisis)
- ⚠️ `generar_informe.py` (útil para reportes)

### NO necesarios para deploy:
- ❌ Todos los archivos `.bat`
- ❌ Carpeta `informes/` (si tiene archivos generados)
- ❌ Carpeta `datos/` con archivos Excel originales (opcional)
- ❌ `__pycache__/`
- ❌ Archivos `.xlsx` temporales

---

## 🚀 Comandos para Limpiar el Repositorio

### Paso 1: Agregar .gitignore
```bash
git add .gitignore
git commit -m "Agregar .gitignore"
```

### Paso 2: Eliminar cache de Python
```bash
git rm -r --cached dashboard/__pycache__
git commit -m "Eliminar cache de Python"
```

### Paso 3: Eliminar archivos .bat (opcional pero recomendado)
```bash
git rm --cached *.bat
git commit -m "Eliminar scripts .bat para Windows"
```

### Paso 4: Renombrar README principal
```bash
git mv README_PREMIUM.md README.md
git commit -m "Renombrar README principal"
```

### Paso 5: Subir cambios
```bash
git push origin main
```

---

## 📁 Estructura Recomendada Final

```
parroquia-huancane/
├── .gitignore                  ← NUEVO
├── README.md                   ← Renombrado de README_PREMIUM.md
├── GUIA_DEPLOY.md
├── INICIO_RAPIDO.md
├── INSTALACION.md
├── requirements.txt
├── datos_consolidados.csv
├── .streamlit/
│   └── config.toml
├── dashboard/
│   └── app_premium.py          ← Archivo principal
└── (opcional)
    ├── procesador_datos.py
    ├── analizar_datos.py
    └── generar_informe.py
```

---

## ⚠️ IMPORTANTE: Datos Sensibles

Si `datos_consolidados.csv` contiene información sensible de la parroquia:

1. **Opción 1:** Hacer el repositorio PRIVADO en GitHub
2. **Opción 2:** Excluir el CSV y usar datos de ejemplo
3. **Opción 3:** Anonimizar los datos antes de subir

---

## 🎯 Configuración en Streamlit Cloud

Después de limpiar, en Streamlit Cloud usa:

- **Repository:** tu-usuario/parroquia-huancane
- **Branch:** main
- **Main file path:** `dashboard/app_premium.py`

---

## 📝 Resumen de Acciones

1. ✅ Crear `.gitignore`
2. ❌ Eliminar `__pycache__/`
3. ❌ Eliminar archivos `.bat`
4. ❌ Eliminar documentación redundante
5. ✅ Renombrar `README_PREMIUM.md` a `README.md`
6. ✅ Push de cambios

---

**Nota:** Los archivos `.bat` solo funcionan en Windows y no son necesarios para Streamlit Cloud (que usa Linux).
