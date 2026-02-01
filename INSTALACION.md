# 🚀 INSTALACIÓN RÁPIDA - Dashboard Premium

## ⚡ Pasos para Ejecutar el Dashboard

### 1️⃣ Instalar Dependencias

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

O usa el script automático:
- Doble click en `INSTALAR.bat`

### 2️⃣ Ejecutar Dashboard

```bash
streamlit run dashboard/app_premium.py
```

O usa el script automático:
- Doble click en `ABRIR_DASHBOARD_PREMIUM.bat`

### 3️⃣ Abrir en Navegador

El dashboard se abrirá automáticamente en:
```
http://localhost:8501
```

---

## ✅ Verificar Instalación

Para verificar que todo está instalado correctamente:

```bash
# Verificar Python
python --version

# Verificar Streamlit
streamlit --version

# Si streamlit no está instalado:
pip install streamlit
```

---

## 📦 Dependencias Necesarias

- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.17.0
- openpyxl >= 3.1.0
- xlrd >= 2.0.1

---

## 🌐 Para Deploy en Streamlit Cloud

### Main File Path:
```
dashboard/app_premium.py
```

### Archivos necesarios en GitHub:
- `dashboard/app_premium.py`
- `datos_consolidados.csv`
- `requirements.txt`
- `.streamlit/config.toml` (opcional)

---

## 🎯 Solución de Problemas

### Error: "streamlit no reconocido"
```bash
pip install streamlit
```

### Error: "No such file or directory: datos_consolidados.csv"
El archivo ya existe. El dashboard usa rutas relativas y debería funcionar.

### Error al cargar datos
Verifica que `datos_consolidados.csv` esté en la carpeta raíz del proyecto.

---

## 📞 Ayuda Adicional

- **Documentación completa:** `README_PREMIUM.md`
- **Guía de deploy:** `GUIA_DEPLOY.md`
- **Inicio rápido:** `INICIO_RAPIDO.md`

---

**Desarrollado por:** Araceli Victoria Cortez  
**Versión:** Premium 1.0
