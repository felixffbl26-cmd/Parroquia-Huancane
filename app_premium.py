"""
Dashboard Premium - Parroquia Santiago Apóstol de Huancané
ENFOQUE PRINCIPAL: SACRAMENTOS Y ACTIVIDAD PASTORAL
Diseño Premium | Visualizaciones de Clase Mundial | Optimizado para Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import calendar
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="⛪ Parroquia Huancané | Dashboard Sacramental",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ESTILOS CSS PREMIUM
# ============================================================================

st.markdown("""
<style>
    /* Variables CSS */
    :root {
        --primary: #1e3a8a;
        --secondary: #3b82f6;
        --accent: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --gold: #f59e0b;
        --light: #f8fafc;
        --dark: #1e293b;
    }
    
    /* Fondo general con textura */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    
    /* Contenedor principal */
    .main .block-container {
        padding: 1rem 1.5rem;
        max-width: 100%;
    }
    
    /* Header Hero Premium */
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-header p {
        text-align: center;
        font-size: 1.1rem;
        opacity: 0.95;
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    /* Métricas Premium con Gradientes */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        background-size: 200% 100%;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(59, 130, 246, 0.2);
    }
    
    div[data-testid="metric-container"] label {
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Tabs Ultra Modernos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: white;
        padding: 0.75rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 28px;
        background: transparent;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.3s;
        color: #475569 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Gráficos con Sombra Premium */
    .js-plotly-plot {
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        background: white;
        padding: 1.5rem;
        transition: all 0.3s;
    }
    
    .js-plotly-plot:hover {
        box-shadow: 0 12px 32px rgba(0,0,0,0.12);
    }
    
    /* Alertas Mejoradas */
    .stAlert {
        border-radius: 16px;
        border: none;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        padding: 1.5rem;
        font-weight: 500;
    }
    
    /* Botones Premium */
    .stButton button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.3s;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
    }
    
    /* Secciones con Título */
    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        display: inline-block;
    }
    
    /* Footer Firma Sutil */
    .footer-signature {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 0.85rem;
        font-style: italic;
    }
    
    .footer-signature .name {
        color: #64748b;
        font-weight: 600;
        font-style: normal;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-header h1 {
            font-size: 1.8rem;
        }
        
        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0 16px;
            font-size: 0.95rem;
        }
    }
    
    /* Animaciones de entrada */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    div[data-testid="metric-container"] {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

@st.cache_data(ttl=300)
def cargar_datos():
    """Carga datos con precisión financiera"""
    import os
    
    # Lista de rutas posibles para encontrar el archivo
    rutas_posibles = [
        # Ruta 1: Directorio padre (para ejecución local)
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos_consolidados.csv"),
        # Ruta 2: Mismo directorio que el script (para Streamlit Cloud)
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_consolidados.csv"),
        # Ruta 3: Directorio actual de trabajo
        "datos_consolidados.csv",
        # Ruta 4: Ruta absoluta desde la raíz del proyecto
        os.path.join(os.getcwd(), "datos_consolidados.csv")
    ]
    
    df = None
    ruta_encontrada = None
    
    # Intentar cada ruta hasta encontrar el archivo
    for ruta_csv in rutas_posibles:
        try:
            if os.path.exists(ruta_csv):
                df = pd.read_csv(ruta_csv)
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
                df['ingreso'] = df['ingreso'].apply(lambda x: Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                df['egreso'] = df['egreso'].apply(lambda x: Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                ruta_encontrada = ruta_csv
                break
        except Exception as e:
            continue
    
    if df is not None:
        st.success(f"✅ Datos cargados correctamente desde: {os.path.basename(ruta_encontrada)}")
        return df
    else:
        st.error(f"❌ Error: No se pudo encontrar 'datos_consolidados.csv'")
        st.info(f"📁 Rutas intentadas:")
        for ruta in rutas_posibles:
            st.text(f"  • {ruta}")
        st.warning("⚠️ Verifica que el archivo 'datos_consolidados.csv' esté en la raíz del repositorio de GitHub")
        return None

def formatear_moneda(valor):
    """Formato de moneda con precisión"""
    if isinstance(valor, Decimal):
        return f"S/ {valor:,.2f}"
    return f"S/ {float(valor):,.2f}"

# ============================================================================
# CARGA DE DATOS
# ============================================================================

df = cargar_datos()

if df is None:
    st.error("❌ No se pudieron cargar los datos.")
    st.stop()

# ============================================================================
# HEADER HERO PREMIUM
# ============================================================================

st.markdown("""
<div class="hero-header">
    <h1>⛪ Parroquia Santiago Apóstol de Huancané</h1>
    <p>📊 Dashboard Sacramental Premium | Actualizado: {}</p>
</div>
""".format(datetime.now().strftime('%d/%m/%Y %H:%M')), unsafe_allow_html=True)

# ============================================================================
# FILTROS PRINCIPALES
# ============================================================================

with st.expander("🔍 FILTROS Y OPCIONES", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        años = sorted(df['año'].dropna().unique())
        año_seleccionado = st.selectbox("📅 Año", años, index=len(años)-1, key="año_filtro")
    
    with col2:
        meses_nombres = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', 
                        7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
        mes_seleccionado = st.selectbox("📆 Mes", ["Todos"] + list(meses_nombres.values()), key="mes_filtro")

# Filtrar datos
df_filtrado = df[df['año'] == año_seleccionado].copy()
if mes_seleccionado != "Todos":
    mes_num = [k for k, v in meses_nombres.items() if v == mes_seleccionado][0]
    df_filtrado = df_filtrado[df_filtrado['mes'] == mes_num]

# ============================================================================
# PESTAÑAS PRINCIPALES
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "⛪ SACRAMENTOS",
    "💰 FINANZAS", 
    "📋 DOCUMENTOS",
    "📊 REPORTES"
])

# ============================================================================
# TAB 1: SACRAMENTOS (PRINCIPAL - ENFOQUE PRINCIPAL)
# ============================================================================

with tab1:
    st.markdown('<p class="section-title">⛪ Actividad Sacramental</p>', unsafe_allow_html=True)
    
    # Filtrar datos sacramentales
    df_sacramentos = df_filtrado[df_filtrado['categoria'] == 'SACRAMENTO'].copy()
    df_misas = df_filtrado[df_filtrado['categoria'] == 'MISA'].copy()
    
    # ========== MÉTRICAS DESTACADAS DE SACRAMENTOS ==========
    st.markdown("### 📊 Resumen Sacramental del Año")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Contar sacramentos por tipo
    bautismos = len(df_sacramentos[df_sacramentos['subcategoria'].str.contains('BAUTISMO', na=False)])
    matrimonios = len(df_sacramentos[df_sacramentos['subcategoria'].str.contains('MATRIMONIO', na=False)])
    confirmaciones = len(df_sacramentos[df_sacramentos['subcategoria'].str.contains('CONFIRMACI', na=False)])
    total_sacramentos = len(df_sacramentos)
    
    with col1:
        st.metric(
            "👶 BAUTISMOS",
            f"{bautismos}",
            help="Total de bautismos administrados"
        )
    
    with col2:
        st.metric(
            "💑 MATRIMONIOS",
            f"{matrimonios}",
            help="Total de matrimonios celebrados"
        )
    
    with col3:
        st.metric(
            "✝️ CONFIRMACIONES",
            f"{confirmaciones}",
            help="Total de confirmaciones administradas"
        )
    
    with col4:
        st.metric(
            "⛪ TOTAL SACRAMENTOS",
            f"{total_sacramentos}",
            help="Total de sacramentos administrados"
        )
    
    st.divider()
    
    # ========== GRÁFICO 1: EVOLUCIÓN MENSUAL DE SACRAMENTOS ==========
    st.markdown("### 📈 Evolución Mensual de Sacramentos")
    
    if not df_sacramentos.empty:
        # Preparar datos mensuales por tipo de sacramento
        df_sac_mensual = df_sacramentos.groupby(['mes', 'subcategoria']).size().reset_index(name='cantidad')
        
        fig1 = go.Figure()
        
        colores_sacramentos = {
            'BAUTISMO': '#3b82f6',
            'MATRIMONIO': '#ec4899',
            'CONFIRMACIÓN': '#8b5cf6'
        }
        
        for sacramento in ['BAUTISMO', 'MATRIMONIO', 'CONFIRMACIÓN']:
            df_temp = df_sac_mensual[df_sac_mensual['subcategoria'] == sacramento]
            if not df_temp.empty:
                fig1.add_trace(go.Scatter(
                    x=df_temp['mes'],
                    y=df_temp['cantidad'],
                    mode='lines+markers',
                    name=sacramento,
                    line=dict(color=colores_sacramentos.get(sacramento, '#64748b'), width=3),
                    marker=dict(size=12, line=dict(width=2, color='white')),
                    fill='tonexty' if sacramento != 'BAUTISMO' else None,
                    hovertemplate=f'<b>{sacramento}</b><br>Mes: %{{x}}<br>Cantidad: %{{y}}<extra></extra>'
                ))
        
        fig1.update_layout(
            title={
                'text': f'📊 Sacramentos por Mes - {año_seleccionado}',
                'font': {'size': 22, 'color': '#1e293b', 'family': 'Arial Black'}
            },
            xaxis_title="Mes",
            yaxis_title="Cantidad",
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=list(meses_nombres.values()),
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("ℹ️ No hay datos de sacramentos para el período seleccionado.")
    
    # ========== GRÁFICO 2: DISTRIBUCIÓN DE SACRAMENTOS (DONUT) ==========
    st.markdown("### 🎯 Distribución de Sacramentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not df_sacramentos.empty:
            conteo_sac = df_sacramentos.groupby('subcategoria').size().reset_index(name='cantidad')
            
            fig2 = go.Figure(data=[go.Pie(
                labels=conteo_sac['subcategoria'],
                values=conteo_sac['cantidad'],
                hole=0.5,
                marker=dict(
                    colors=['#3b82f6', '#ec4899', '#8b5cf6', '#10b981', '#f59e0b'],
                    line=dict(color='white', width=3)
                ),
                textinfo='label+percent+value',
                textfont_size=14,
                hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>%{percent}<extra></extra>'
            )])
            
            fig2.update_layout(
                title={
                    'text': f'📊 Sacramentos {año_seleccionado}',
                    'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
                },
                height=450,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("ℹ️ No hay datos disponibles.")
    
    # ========== GRÁFICO 3: TIPOS DE MISAS ==========
    with col2:
        if not df_misas.empty:
            conteo_misas = df_misas.groupby('subcategoria').size().reset_index(name='cantidad')
            conteo_misas = conteo_misas.sort_values('cantidad', ascending=False)
            
            fig3 = go.Figure(data=[go.Bar(
                x=conteo_misas['cantidad'],
                y=conteo_misas['subcategoria'],
                orientation='h',
                marker=dict(
                    color=conteo_misas['cantidad'],
                    colorscale='Blues',
                    showscale=False,
                    line=dict(color='white', width=1)
                ),
                text=conteo_misas['cantidad'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<extra></extra>'
            )])
            
            fig3.update_layout(
                title={
                    'text': f'🙏 Tipos de Misas {año_seleccionado}',
                    'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
                },
                xaxis_title="Cantidad",
                yaxis_title="",
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(showgrid=False)
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("ℹ️ No hay datos de misas disponibles.")
    
    # ========== HEATMAP DE ACTIVIDAD SACRAMENTAL ==========
    st.markdown("### 🔥 Mapa de Calor - Actividad Sacramental")
    
    if not df_sacramentos.empty:
        # Crear matriz de actividad por mes y tipo
        pivot_data = df_sacramentos.groupby(['mes', 'subcategoria']).size().reset_index(name='cantidad')
        pivot_table = pivot_data.pivot(index='subcategoria', columns='mes', values='cantidad').fillna(0)
        
        fig4 = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=[meses_nombres.get(m, str(m)) for m in pivot_table.columns],
            y=pivot_table.index,
            colorscale='Blues',
            text=pivot_table.values,
            texttemplate='%{text}',
            textfont={"size": 14},
            hovertemplate='<b>%{y}</b><br>Mes: %{x}<br>Cantidad: %{z}<extra></extra>',
            colorbar=dict(title="Cantidad")
        ))
        
        fig4.update_layout(
            title={
                'text': '🗓️ Calendario de Actividad Sacramental',
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
            },
            xaxis_title="Mes",
            yaxis_title="Sacramento",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # ========== ANÁLISIS AUTOMÁTICO ==========
    st.markdown("### 💡 Análisis Automático")
    
    if total_sacramentos > 0:
        mes_mas_activo = df_sacramentos.groupby('mes').size().idxmax() if not df_sacramentos.empty else None
        sacramento_mas_comun = df_sacramentos['subcategoria'].mode()[0] if not df_sacramentos.empty else None
        
        col1, col2 = st.columns(2)
        
        with col1:
            if mes_mas_activo:
                st.success(f"""
                **📅 Mes más activo:** {meses_nombres.get(mes_mas_activo, 'N/A')}
                
                El mes con mayor actividad sacramental fue **{meses_nombres.get(mes_mas_activo, 'N/A')}** 
                con un total de **{df_sacramentos[df_sacramentos['mes'] == mes_mas_activo].shape[0]} sacramentos**.
                """)
        
        with col2:
            if sacramento_mas_comun:
                st.info(f"""
                **⛪ Sacramento más frecuente:** {sacramento_mas_comun}
                
                El sacramento más administrado en {año_seleccionado} fue **{sacramento_mas_comun}**.
                """)
    
    # ========== COMPARATIVA CON AÑO ANTERIOR ==========
    if len(años) > 1:
        st.markdown("### 📊 Comparativa con Año Anterior")
        
        año_anterior = año_seleccionado - 1
        if año_anterior in años:
            df_anterior = df[df['año'] == año_anterior]
            df_sac_anterior = df_anterior[df_anterior['categoria'] == 'SACRAMENTO']
            
            baut_anterior = len(df_sac_anterior[df_sac_anterior['subcategoria'].str.contains('BAUTISMO', na=False)])
            matr_anterior = len(df_sac_anterior[df_sac_anterior['subcategoria'].str.contains('MATRIMONIO', na=False)])
            conf_anterior = len(df_sac_anterior[df_sac_anterior['subcategoria'].str.contains('CONFIRMACI', na=False)])
            
            datos_comp = pd.DataFrame({
                'Sacramento': ['Bautismos', 'Matrimonios', 'Confirmaciones'],
                str(año_anterior): [baut_anterior, matr_anterior, conf_anterior],
                str(año_seleccionado): [bautismos, matrimonios, confirmaciones]
            })
            
            fig5 = go.Figure()
            
            fig5.add_trace(go.Bar(
                name=str(año_anterior),
                x=datos_comp['Sacramento'],
                y=datos_comp[str(año_anterior)],
                marker_color='#94a3b8',
                text=datos_comp[str(año_anterior)],
                textposition='outside'
            ))
            
            fig5.add_trace(go.Bar(
                name=str(año_seleccionado),
                x=datos_comp['Sacramento'],
                y=datos_comp[str(año_seleccionado)],
                marker_color='#3b82f6',
                text=datos_comp[str(año_seleccionado)],
                textposition='outside'
            ))
            
            fig5.update_layout(
                title={
                    'text': f'📊 Comparativa {año_anterior} vs {año_seleccionado}',
                    'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
                },
                xaxis_title="Sacramento",
                yaxis_title="Cantidad",
                barmode='group',
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
            )
            
            st.plotly_chart(fig5, use_container_width=True)
            
            # Análisis de variación
            var_baut = ((bautismos - baut_anterior) / baut_anterior * 100) if baut_anterior > 0 else 0
            var_matr = ((matrimonios - matr_anterior) / matr_anterior * 100) if matr_anterior > 0 else 0
            var_conf = ((confirmaciones - conf_anterior) / conf_anterior * 100) if conf_anterior > 0 else 0
            
            if var_baut > 0 or var_matr > 0 or var_conf > 0:
                st.success(f"""
                **📈 TENDENCIA POSITIVA**
                
                - Bautismos: {var_baut:+.1f}%
                - Matrimonios: {var_matr:+.1f}%
                - Confirmaciones: {var_conf:+.1f}%
                
                ✅ La actividad sacramental muestra crecimiento respecto al año anterior.
                """)
            else:
                st.warning(f"""
                **📉 ANÁLISIS**
                
                - Bautismos: {var_baut:+.1f}%
                - Matrimonios: {var_matr:+.1f}%
                - Confirmaciones: {var_conf:+.1f}%
                
                ⚠️ Se recomienda revisar estrategias pastorales para incrementar la actividad sacramental.
                """)

# ============================================================================
# TAB 2: FINANZAS
# ============================================================================

with tab2:
    st.markdown('<p class="section-title">💰 Gestión Financiera</p>', unsafe_allow_html=True)
    
    # KPIs Financieros
    total_ingresos = sum(df_filtrado['ingreso'])
    total_egresos = sum(df_filtrado['egreso'])
    balance = total_ingresos - total_egresos
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 INGRESOS", formatear_moneda(total_ingresos))
    
    with col2:
        st.metric("💸 EGRESOS", formatear_moneda(total_egresos))
    
    with col3:
        st.metric("📊 BALANCE", formatear_moneda(balance), 
                 "Positivo ✅" if balance >= 0 else "Negativo ⚠️")
    
    st.divider()
    
    # Gráfico de flujo mensual
    st.markdown("### 📈 Flujo de Caja Mensual")
    
    df_mensual = df_filtrado.groupby('mes').agg({
        'ingreso': lambda x: float(sum(x)),
        'egreso': lambda x: float(sum(x))
    }).reset_index()
    
    df_mensual['balance'] = df_mensual['ingreso'] - df_mensual['egreso']
    df_mensual['mes_nombre'] = df_mensual['mes'].apply(lambda x: meses_nombres.get(x, str(x)))
    
    fig_fin = go.Figure()
    
    fig_fin.add_trace(go.Bar(
        name='Ingresos',
        x=df_mensual['mes_nombre'],
        y=df_mensual['ingreso'],
        marker_color='#10b981',
        text=df_mensual['ingreso'].apply(lambda x: f'S/ {x:,.0f}'),
        textposition='outside'
    ))
    
    fig_fin.add_trace(go.Bar(
        name='Egresos',
        x=df_mensual['mes_nombre'],
        y=df_mensual['egreso'],
        marker_color='#ef4444',
        text=df_mensual['egreso'].apply(lambda x: f'S/ {x:,.0f}'),
        textposition='outside'
    ))
    
    fig_fin.update_layout(
        title={
            'text': f'💵 Ingresos y Egresos - {año_seleccionado}',
            'font': {'size': 22, 'color': '#1e293b', 'family': 'Arial Black'}
        },
        xaxis_title="Mes",
        yaxis_title="Monto (S/)",
        barmode='group',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    )
    
    st.plotly_chart(fig_fin, use_container_width=True)
    
    # Distribución de ingresos por categoría
    st.markdown("### 🏷️ Distribución de Ingresos")
    
    cat_data = df_filtrado.groupby('categoria').agg({
        'ingreso': lambda x: float(sum(x))
    }).reset_index()
    cat_data = cat_data.sort_values('ingreso', ascending=False)
    
    fig_cat = go.Figure(data=[go.Pie(
        labels=cat_data['categoria'],
        values=cat_data['ingreso'],
        hole=0.4,
        marker=dict(
            colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>S/ %{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    fig_cat.update_layout(
        title={
            'text': '📊 Composición de Ingresos por Categoría',
            'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
        },
        height=500
    )
    
    st.plotly_chart(fig_cat, use_container_width=True)

# ============================================================================
# TAB 3: DOCUMENTOS
# ============================================================================

with tab3:
    st.markdown('<p class="section-title">📋 Documentos Parroquiales</p>', unsafe_allow_html=True)
    
    df_docs = df_filtrado[df_filtrado['categoria'] == 'DOCUMENTO'].copy()
    
    if not df_docs.empty:
        # Métricas de documentos
        total_docs = len(df_docs)
        partidas = len(df_docs[df_docs['subcategoria'].str.contains('PARTIDA', na=False)])
        constancias = len(df_docs[df_docs['subcategoria'].str.contains('CONSTANCIA', na=False)])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📄 TOTAL DOCUMENTOS", f"{total_docs}")
        
        with col2:
            st.metric("📜 PARTIDAS", f"{partidas}")
        
        with col3:
            st.metric("📋 CONSTANCIAS", f"{constancias}")
        
        st.divider()
        
        # Gráfico de documentos por mes
        st.markdown("### 📊 Documentos Emitidos por Mes")
        
        df_docs_mes = df_docs.groupby('mes').size().reset_index(name='cantidad')
        df_docs_mes['mes_nombre'] = df_docs_mes['mes'].apply(lambda x: meses_nombres.get(x, str(x)))
        
        fig_docs = go.Figure(data=[go.Bar(
            x=df_docs_mes['mes_nombre'],
            y=df_docs_mes['cantidad'],
            marker_color='#8b5cf6',
            text=df_docs_mes['cantidad'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Documentos: %{y}<extra></extra>'
        )])
        
        fig_docs.update_layout(
            title={
                'text': f'📄 Documentos Emitidos - {año_seleccionado}',
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
            },
            xaxis_title="Mes",
            yaxis_title="Cantidad",
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        
        st.plotly_chart(fig_docs, use_container_width=True)
        
        # Distribución por tipo
        conteo_tipo = df_docs.groupby('subcategoria').size().reset_index(name='cantidad')
        
        fig_tipo = go.Figure(data=[go.Pie(
            labels=conteo_tipo['subcategoria'],
            values=conteo_tipo['cantidad'],
            hole=0.5,
            marker=dict(
                colors=['#8b5cf6', '#ec4899', '#f59e0b'],
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent+value',
            textfont_size=14
        )])
        
        fig_tipo.update_layout(
            title={
                'text': '📊 Distribución por Tipo de Documento',
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Arial Black'}
            },
            height=450
        )
        
        st.plotly_chart(fig_tipo, use_container_width=True)
    else:
        st.info("ℹ️ No hay datos de documentos para el período seleccionado.")

# ============================================================================
# TAB 4: REPORTES
# ============================================================================

with tab4:
    st.markdown('<p class="section-title">📊 Reportes y Análisis</p>', unsafe_allow_html=True)
    
    # Resumen general
    st.markdown("### 📈 Resumen General del Año")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⛪ Sacramentos", f"{len(df_filtrado[df_filtrado['categoria'] == 'SACRAMENTO'])}")
    
    with col2:
        st.metric("🙏 Misas", f"{len(df_filtrado[df_filtrado['categoria'] == 'MISA'])}")
    
    with col3:
        st.metric("📄 Documentos", f"{len(df_filtrado[df_filtrado['categoria'] == 'DOCUMENTO'])}")
    
    with col4:
        st.metric("📋 Total Registros", f"{len(df_filtrado)}")
    
    st.divider()
    
    # Tabla de datos detallados
    st.markdown("### 📋 Datos Detallados")
    
    df_display = df_filtrado[['fecha', 'detalle', 'categoria', 'subcategoria', 'ingreso', 'egreso']].copy()
    df_display['ingreso'] = df_display['ingreso'].apply(lambda x: float(x))
    df_display['egreso'] = df_display['egreso'].apply(lambda x: float(x))
    df_display = df_display.sort_values('fecha', ascending=False)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
        column_config={
            "fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "detalle": "Detalle",
            "categoria": "Categoría",
            "subcategoria": "Subcategoría",
            "ingreso": st.column_config.NumberColumn("Ingreso", format="S/ %.2f"),
            "egreso": st.column_config.NumberColumn("Egreso", format="S/ %.2f")
        }
    )
    
    # Botón de descarga
    csv = df_display.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Descargar Datos (CSV)",
        data=csv,
        file_name=f"parroquia_huancane_{año_seleccionado}.csv",
        mime="text/csv"
    )

# ============================================================================
# FOOTER CON FIRMA SUTIL
# ============================================================================

st.markdown("""
<div class="footer-signature">
    Desarrollado con dedicación por <span class="name">Araceli Victoria Cortez</span>
    <br>
    Dashboard Premium v1.0 | {} 
</div>
""".format(datetime.now().year), unsafe_allow_html=True)
