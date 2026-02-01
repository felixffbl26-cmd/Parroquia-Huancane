# 🚀 Guía de Deploy - Dashboard Parroquia Huancané

## Preparación para Streamlit Cloud

### Paso 1: Preparar el Repositorio en GitHub

1. **Crear un nuevo repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre sugerido: `parroquia-huancane-dashboard`
   - Descripción: "Dashboard Sacramental - Parroquia Santiago Apóstol de Huancané"
   - Selecciona "Public" o "Private" según prefieras
   - Click en "Create repository"

2. **Subir los archivos necesarios:**

   Archivos OBLIGATORIOS para el deploy:
   ```
   ├── dashboard/
   │   └── app_premium.py          ← Dashboard principal
   ├── datos_consolidados.csv      ← Datos procesados
   ├── requirements.txt            ← Dependencias
   └── .streamlit/
       └── config.toml             ← Configuración
   ```

3. **Comandos Git para subir:**

   ```bash
   # Inicializar repositorio (si no existe)
   git init
   
   # Agregar archivos
   git add dashboard/app_premium.py
   git add datos_consolidados.csv
   git add requirements.txt
   git add .streamlit/config.toml
   
   # Crear commit
   git commit -m "Dashboard Premium con enfoque en sacramentos"
   
   # Conectar con GitHub (reemplaza con tu URL)
   git remote add origin https://github.com/TU_USUARIO/parroquia-huancane-dashboard.git
   
   # Subir a GitHub
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Deploy en Streamlit Cloud

1. **Ir a Streamlit Cloud:**
   - Visita: https://share.streamlit.io/
   - Click en "Sign up" o "Sign in" con tu cuenta de GitHub

2. **Crear nueva app:**
   - Click en "New app"
   - Selecciona tu repositorio: `parroquia-huancane-dashboard`
   - Branch: `main`
   - Main file path: `dashboard/app_premium.py`
   - App URL (personalizada): `parroquia-huancane` (o el nombre que prefieras)

3. **Configuración avanzada (opcional):**
   - Python version: 3.11
   - Click en "Deploy!"

4. **Esperar el deploy:**
   - El proceso toma 2-5 minutos
   - Verás logs en tiempo real
   - Cuando termine, tendrás tu URL pública

### Paso 3: Actualizar Datos

Para actualizar los datos en el futuro:

```bash
# Procesar nuevos datos
python procesador_datos.py

# Subir datos actualizados
git add datos_consolidados.csv
git commit -m "Actualización de datos - [FECHA]"
git push

# Streamlit Cloud se actualizará automáticamente
```

---

## 🎯 Archivo Principal

El dashboard principal está en: `dashboard/app_premium.py`

**Características:**
- ⛪ Enfoque principal en SACRAMENTOS
- 📊 Visualizaciones premium con Plotly
- 📱 Diseño responsive (móvil y desktop)
- 💡 Análisis automáticos e insights
- 🎨 Diseño moderno con gradientes
- ✍️ Firma de Araceli Victoria Cortez

---

## 📋 Checklist Pre-Deploy

Antes de hacer deploy, verifica:

- [ ] `datos_consolidados.csv` está actualizado
- [ ] `requirements.txt` existe
- [ ] `.streamlit/config.toml` existe
- [ ] `dashboard/app_premium.py` funciona localmente
- [ ] Todos los archivos están en GitHub
- [ ] No hay datos sensibles en el repositorio

---

## 🧪 Probar Localmente Primero

Antes de hacer deploy, prueba localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run dashboard/app_premium.py
```

Abre tu navegador en: http://localhost:8501

---

## 🔧 Solución de Problemas

### Error: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Error: "File not found: datos_consolidados.csv"
- Asegúrate de que el archivo CSV esté en la raíz del proyecto
- Verifica la ruta en `app_premium.py` (línea ~280)

### Error en Streamlit Cloud
- Revisa los logs en la consola de Streamlit Cloud
- Verifica que `requirements.txt` tenga todas las dependencias
- Asegúrate de que la ruta del archivo principal sea correcta

---

## 📱 Compartir el Dashboard

Una vez deployado, tu URL será algo como:
```
https://parroquia-huancane.streamlit.app
```

Puedes compartir esta URL con:
- El padre de la parroquia
- Miembros del consejo parroquial
- Feligreses autorizados

---

## 🔐 Seguridad

**IMPORTANTE:** Si tus datos son sensibles:

1. Haz el repositorio PRIVADO en GitHub
2. En Streamlit Cloud, solo usuarios autorizados podrán ver la app
3. Considera agregar autenticación (requiere código adicional)

---

## 🎉 ¡Listo!

Tu dashboard estará disponible 24/7 en la nube, accesible desde cualquier dispositivo.

**Desarrollado por:** Araceli Victoria Cortez
**Fecha:** Febrero 2026
