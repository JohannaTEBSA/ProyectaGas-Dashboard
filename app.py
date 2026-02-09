"""
ProyectaGAS Dashboard - TPLGas
Dashboard web para predicción de demanda y precios de gas natural
Desplegado en Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="ProyectaGAS - TPLGas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

st.markdown("""
<style>
    /* ===== ESTILOS GENERALES ===== */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* ===== HEADER PRINCIPAL ===== */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* ===== SUBTÍTULO ===== */
    .subtitle {
        text-align: center;
        color: #5a6c7d;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e6ed;
    }
    
    /* ===== LOGO EN SIDEBAR ===== */
    .css-1d391kg img, [data-testid="stImage"] img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        background: white;
        padding: 15px;
        max-width: 180px !important;
        margin: 0 auto;
        display: block;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f8f9fa;
        border-radius: 8px;
        color: #5a6c7d;
        font-weight: 600;
        padding: 0 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
        transform: translateY(-2px);
    }
    
    /* ===== TARJETAS DE MÉTRICAS ===== */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        color: #667eea;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #2d3748;
        margin: 0.5rem 0;
    }
    
    /* ===== INFO BOX ===== */
    .info-box {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
        border-left: 5px solid #00acc1;
        padding: 1.2rem;
        margin: 1.5rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* ===== CARDS DE CALIDAD ===== */
    .quality-excellent {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    
    .quality-good {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
    }
    
    .quality-fair {
        background: linear-gradient(135deg, #ffe5d0 0%, #ffd8b8 100%);
        border-left: 5px solid #fd7e14;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(253, 126, 20, 0.2);
    }
    
    .quality-poor {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.2);
    }
    
    /* ===== BOTONES ===== */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4);
    }
    
    /* ===== ALERTAS ===== */
    .stAlert {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* ===== TABLAS ===== */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    /* ===== ANIMACIONES ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_datos():
    """Carga todos los archivos de predicciones y datos históricos"""
    datos = {}
    
    archivos = {
        'pred_precios': 'predicciones_futuras_2026.xlsx',
        'pred_demanda': 'predicciones_2026_ensemble.xlsx',
        'historico_precios': 'df_completo_procesado.csv',
        'historico_demanda': 'Data_Demanda.xlsx',  # Datos hasta enero 2026
        'metricas_ensemble': 'metricas_ensemble.csv',  # Métricas de precisión por variable
        'metricas_resumen': 'metricas_resumen.csv',  # Métricas generales
    }
    
    for key, filename in archivos.items():
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filename)
            else:
                df = pd.read_csv(filename)
            
            if 'Fecha' in df.columns:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
            
            # Procesamiento especial para Data_Demanda.xlsx
            if key == 'historico_demanda' and 'Zona' in df.columns:
                # Agrupar por fecha (suma Costa + Interior)
                df = df.groupby('Fecha')['Cantidad diaria promedio (MBTUD)'].sum().reset_index()
                df.columns = ['Fecha', 'Demanda_Total_MBTUD']
            
            datos[key] = df
        except Exception as e:
            st.sidebar.warning(f"⚠️ {filename}: {str(e)[:50]}")
            datos[key] = None
    
    return datos

# ============================================================================
# FUNCIONES DE MÉTRICAS
# ============================================================================

def calcular_metricas(valores):
    """Calcula métricas estadísticas"""
    if valores is None or len(valores) == 0:
        return None
    
    return {
        'promedio': np.mean(valores),
        'minimo': np.min(valores),
        'maximo': np.max(valores),
        'std': np.std(valores),
        'mediana': np.median(valores),
        'cv': (np.std(valores) / np.mean(valores)) * 100
    }

# ============================================================================
# FUNCIÓN DE VISUALIZACIÓN PRINCIPAL
# ============================================================================

def crear_grafico_con_historico(df_pred, df_hist, columna_pred, columna_hist, titulo, unidad=""):
    """
    Crea gráfico con predicciones Y datos históricos
    Con unidades visibles y rangos apropiados
    """
    fig = go.Figure()
    
    # Histórico
    if df_hist is not None and columna_hist in df_hist.columns:
        df_hist_filtrado = df_hist.tail(180)
        
        fig.add_trace(go.Scatter(
            x=df_hist_filtrado['Fecha'],
            y=df_hist_filtrado[columna_hist],
            mode='lines',
            name='Histórico (Real)',
            line=dict(color='#424242', width=2),
            hovertemplate=f'<b>Real</b><br>Fecha: %{{x}}<br>Valor: %{{y:.2f}} {unidad}<extra></extra>'
        ))
    
    # Predicciones
    if df_pred is not None and columna_pred in df_pred.columns:
        fig.add_trace(go.Scatter(
            x=df_pred['Fecha'],
            y=df_pred[columna_pred],
            mode='lines',
            name='Predicción 2026',
            line=dict(color='#1E88E5', width=2.5),
            fill='tonexty',
            fillcolor='rgba(30, 136, 229, 0.15)',
            hovertemplate=f'<b>Predicción</b><br>Fecha: %{{x}}<br>Valor: %{{y:.2f}} {unidad}<extra></extra>'
        ))
        
        # Línea vertical separando histórico de predicción
        if df_hist is not None and len(df_hist) > 0:
            fecha_corte = df_hist['Fecha'].max()
            
            # Convertir a string ISO format para máxima compatibilidad con plotly
            if hasattr(fecha_corte, 'to_pydatetime'):
                fecha_corte_str = fecha_corte.to_pydatetime().strftime('%Y-%m-%d')
            elif hasattr(fecha_corte, 'strftime'):
                fecha_corte_str = fecha_corte.strftime('%Y-%m-%d')
            else:
                fecha_corte_str = str(fecha_corte)
            
            fig.add_vline(
                x=fecha_corte_str,
                line_dash="dash",
                line_color="gray",
                annotation_text="Inicio Predicción",
                annotation_position="top"
            )
    
    # Calcular rango apropiado del eje Y
    all_values = []
    if df_hist is not None and columna_hist in df_hist.columns:
        all_values.extend(df_hist[columna_hist].dropna().values)
    if df_pred is not None and columna_pred in df_pred.columns:
        all_values.extend(df_pred[columna_pred].dropna().values)
    
    if all_values:
        y_min = min(all_values)
        y_max = max(all_values)
        y_range = y_max - y_min
        y_min_plot = y_min - (y_range * 0.1)
        y_max_plot = y_max + (y_range * 0.1)
    else:
        y_min_plot = None
        y_max_plot = None
    
    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=20, color='#1a1a1a')
        ),
        xaxis_title='Fecha',
        yaxis_title=f'Valor ({unidad})',
        hovermode='x unified',
        height=550,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            range=[y_min_plot, y_max_plot]
        )
    )
    
    return fig

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">⚡ ProyectaGAS - Dashboard Empresarial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema de Predicción de Demanda y Precios de Gas Natural | TPLGas</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Logo - Más pequeño y centrado
        try:
            # Contenedor centrado para el logo
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("logo.jpg", width=180)
            st.markdown("---")
        except:
            pass
        
        st.markdown("### 📁 Estado de Datos")
        datos = cargar_datos()
        
        archivos_ok = sum(1 for v in datos.values() if v is not None)
        total_archivos = len(datos)
        
        if archivos_ok == total_archivos:
            st.success(f"✅ {archivos_ok}/{total_archivos} archivos cargados")
        else:
            st.warning(f"⚠️ {archivos_ok}/{total_archivos} archivos cargados")
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.info("""
        **Características:**
        - ✅ Comparación con datos reales
        - ✅ Unidades visibles
        - ✅ Rangos optimizados
        - ✅ Métricas de precisión
        """)
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["💵 Precios Internacionales", "📊 Demanda Total", "🏭 Sectores", "📈 Métricas del Modelo"])
    
    # ========================================================================
    # TAB 1: PRECIOS
    # ========================================================================
    with tab1:
        st.markdown("### 💵 Predicción de Precios Internacionales")
        st.markdown("Predicciones para Henry Hub (USA) y TTF (Europa) - Año 2026")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Henry Hub (USD/MMBtu)")
            
            if datos['pred_precios'] is not None:
                col_hh_pred = None
                for c in ['HenryHub_USD_MMBtu_Predicho', 'HenryHub_USD_MMBtu', 'HenryHub']:
                    if c in datos['pred_precios'].columns:
                        col_hh_pred = c
                        break
                
                col_hh_hist = None
                if datos['historico_precios'] is not None:
                    for c in ['HenryHub_USD_MMBtu', 'HenryHub']:
                        if c in datos['historico_precios'].columns:
                            col_hh_hist = c
                            break
                
                if col_hh_pred:
                    fig_hh = crear_grafico_con_historico(
                        datos['pred_precios'],
                        datos['historico_precios'],
                        col_hh_pred,
                        col_hh_hist,
                        "Henry Hub - Predicción 2026",
                        unidad="USD/MMBtu"
                    )
                    st.plotly_chart(fig_hh, use_container_width=True)
                    
                    metricas_hh = calcular_metricas(datos['pred_precios'][col_hh_pred])
                    
                    if metricas_hh:
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("📊 Promedio", f"${metricas_hh['promedio']:.2f}")
                        col_b.metric("📉 Mínimo", f"${metricas_hh['minimo']:.2f}")
                        col_c.metric("📈 Máximo", f"${metricas_hh['maximo']:.2f}")
        
        with col2:
            st.markdown("#### TTF (USD/MMBtu)")
            
            if datos['pred_precios'] is not None:
                col_ttf_pred = None
                for c in ['TTF_USD_MMBtu_Predicho', 'TTF_USD_MMBtu', 'TTF']:
                    if c in datos['pred_precios'].columns:
                        col_ttf_pred = c
                        break
                
                col_ttf_hist = None
                if datos['historico_precios'] is not None:
                    for c in ['TTF_USD_MMBtu', 'TTF']:
                        if c in datos['historico_precios'].columns:
                            col_ttf_hist = c
                            break
                
                if col_ttf_pred:
                    fig_ttf = crear_grafico_con_historico(
                        datos['pred_precios'],
                        datos['historico_precios'],
                        col_ttf_pred,
                        col_ttf_hist,
                        "TTF - Predicción 2026",
                        unidad="USD/MMBtu"
                    )
                    st.plotly_chart(fig_ttf, use_container_width=True)
                    
                    metricas_ttf = calcular_metricas(datos['pred_precios'][col_ttf_pred])
                    
                    if metricas_ttf:
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("📊 Promedio", f"${metricas_ttf['promedio']:.2f}")
                        col_b.metric("📉 Mínimo", f"${metricas_ttf['minimo']:.2f}")
                        col_c.metric("📈 Máximo", f"${metricas_ttf['maximo']:.2f}")

    # ========================================================================
    # TAB 2: DEMANDA TOTAL
    # ========================================================================
    with tab2:
        st.markdown("### 📊 Predicción de Demanda Total de Gas Natural")
        st.markdown("Demanda agregada nacional - Año 2026")
        
        if datos['pred_demanda'] is not None:
            col_dem_pred = None
            for c in ['Demanda_Total_MBTUD', 'Total_MBTUD', 'Demanda_Total']:
                if c in datos['pred_demanda'].columns:
                    col_dem_pred = c
                    break
            
            col_dem_hist = None
            if datos['historico_demanda'] is not None:
                for c in ['Demanda_Total_MBTUD', 'Total_MBTUD', 'Demanda_Total']:
                    if c in datos['historico_demanda'].columns:
                        col_dem_hist = c
                        break
            
            if col_dem_pred:
                fig_dem = crear_grafico_con_historico(
                    datos['pred_demanda'],
                    datos['historico_demanda'],
                    col_dem_pred,
                    col_dem_hist,
                    "Demanda Total - Predicción 2026",
                    unidad="MBTUD"
                )
                st.plotly_chart(fig_dem, use_container_width=True)
                
                metricas_dem = calcular_metricas(datos['pred_demanda'][col_dem_pred])
                
                if metricas_dem:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📊 Promedio", f"{metricas_dem['promedio']:,.0f} MBTUD")
                    col2.metric("📉 Mínimo", f"{metricas_dem['minimo']:,.0f} MBTUD")
                    col3.metric("📈 Máximo", f"{metricas_dem['maximo']:,.0f} MBTUD")
                    col4.metric("📊 Desv. Est.", f"{metricas_dem['std']:,.0f} MBTUD")
                
                st.markdown("#### 📈 Análisis de Tendencia")
                valores = datos['pred_demanda'][col_dem_pred].values
                primer_trimestre = np.mean(valores[:90])
                ultimo_trimestre = np.mean(valores[-90:])
                cambio_pct = ((ultimo_trimestre - primer_trimestre) / primer_trimestre) * 100
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Q1 2026", f"{primer_trimestre:,.0f} MBTUD")
                col_b.metric("Q4 2026", f"{ultimo_trimestre:,.0f} MBTUD")
                col_c.metric("Variación", f"{cambio_pct:+.2f}%")

    # ========================================================================
    # TAB 3: SECTORES
    # ========================================================================
    with tab3:
        st.markdown("### 🏭 Predicción por Sectores y Regiones")
        
        sectores_disponibles = {
            "Costa": "Demanda_Costa_Total_MBTUD",
            "Interior": "Demanda_Interior_Total_MBTUD",
            "Industrial": "Demanda_Industrial_Total_MBTUD",
            "Comercial": "Demanda_Comercial_Total_MBTUD",
            "Residencial": "Demanda_Residencial_Total_MBTUD",
            "Petrolero": "Demanda_Petrolero_Total_MBTUD",
            "Generación Térmica": "Demanda_GeneracionTermica_Total_MBTUD",
            "GNVC": "Demanda_GNVC_Total_MBTUD",
            "Refinería": "Demanda_Refineria_Total_MBTUD",
            "Compresora": "Demanda_Compresora_Total_MBTUD"
        }
        
        sector_seleccionado = st.selectbox(
            "Seleccionar sector:",
            list(sectores_disponibles.keys())
        )
        
        columna_sector = sectores_disponibles[sector_seleccionado]
        
        if datos['pred_demanda'] is not None and columna_sector in datos['pred_demanda'].columns:
            fig_sector = crear_grafico_con_historico(
                datos['pred_demanda'],
                None,
                columna_sector,
                None,
                f"Sector {sector_seleccionado} - Predicción 2026",
                unidad="MBTUD"
            )
            st.plotly_chart(fig_sector, use_container_width=True)
            
            metricas_sector = calcular_metricas(datos['pred_demanda'][columna_sector])
            
            if metricas_sector:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📊 Promedio", f"{metricas_sector['promedio']:,.0f} MBTUD")
                col2.metric("📉 Mínimo", f"{metricas_sector['minimo']:,.0f} MBTUD")
                col3.metric("📈 Máximo", f"{metricas_sector['maximo']:,.0f} MBTUD")
                col4.metric("📊 Coef. Var.", f"{metricas_sector['cv']:.2f}%")
    
    # ========================================================================
    # TAB 4: MÉTRICAS DEL MODELO
    # ========================================================================
    with tab4:
        st.markdown("### 📈 Métricas de Precisión del Modelo")
        st.markdown("Evaluación del desempeño de los modelos de predicción")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Métricas por Variable (Demanda)")
            
            if datos['metricas_ensemble'] is not None:
                df_metricas = datos['metricas_ensemble'].copy()
                
                # Formatear para mostrar
                df_display = df_metricas.copy()
                df_display['MAPE_Test'] = df_display['MAPE_Test'].apply(lambda x: f"{x:.2f}%")
                df_display['R2_Test'] = df_display['R2_Test'].apply(lambda x: f"{x:.3f}")
                df_display.columns = ['Variable', 'MAPE (%)', 'R² Score', 'Ensemble']
                
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("""
                **Interpretación:**
                - **MAPE**: Error promedio (menor = mejor)
                  - < 2%: Excelente
                  - 2-5%: Muy bueno
                  - 5-10%: Bueno
                  - > 10%: Necesita mejora
                - **R²**: Capacidad de ajuste (1.0 = perfecto)
                  - > 0.9: Excelente
                  - 0.7-0.9: Bueno
                  - < 0.7: Regular
                """)
        
        with col2:
            st.markdown("#### 💎 Calidad de las Predicciones")
            
            if datos['metricas_resumen'] is not None:
                df_resumen = datos['metricas_resumen'].copy()
                
                # Mostrar métricas como cards mejoradas
                for idx, row in df_resumen.iterrows():
                    variable = row['Variable']
                    mape = row['MAPE']
                    r2 = row['R²']
                    
                    # Determinar clase CSS según MAPE
                    if mape < 2:
                        clase = "quality-excellent"
                        emoji = "🌟"
                        calificacion = "Excelente"
                    elif mape < 5:
                        clase = "quality-good"
                        emoji = "✨"
                        calificacion = "Muy bueno"
                    elif mape < 10:
                        clase = "quality-fair"
                        emoji = "📊"
                        calificacion = "Bueno"
                    else:
                        clase = "quality-poor"
                        emoji = "⚠️"
                        calificacion = "Necesita mejora"
                    
                    st.markdown(f"""
                    <div class='{clase}'>
                        <h4 style='margin: 0; display: flex; align-items: center; gap: 8px;'>
                            <span>{emoji}</span>
                            <span>{variable.replace('_', ' ')}</span>
                        </h4>
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                            <div>
                                <p style='margin: 0; font-size: 0.85em; color: #5a6c7d; font-weight: 600;'>MAPE</p>
                                <p style='margin: 5px 0 0 0; font-size: 1.8em; font-weight: 800;'>{mape:.2f}%</p>
                            </div>
                            <div>
                                <p style='margin: 0; font-size: 0.85em; color: #5a6c7d; font-weight: 600;'>R² Score</p>
                                <p style='margin: 5px 0 0 0; font-size: 1.8em; font-weight: 800;'>{r2:.3f}</p>
                            </div>
                        </div>
                        <p style='margin: 12px 0 0 0; font-size: 1em; font-weight: 700; text-align: center;'>
                            {calificacion}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Explicación adicional
        st.markdown("---")
        st.markdown("### ℹ️ Sobre las Métricas")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info("""
            **MAPE (Mean Absolute Percentage Error)**
            
            Mide el error promedio de las predicciones en porcentaje.
            
            Ejemplo: MAPE de 3% significa que en promedio las predicciones 
            se desvían ±3% del valor real.
            """)
        
        with col_b:
            st.info("""
            **R² (Coeficiente de Determinación)**
            
            Indica qué tan bien el modelo explica la variabilidad de los datos.
            
            R² = 1.0 significa ajuste perfecto.
            R² = 0.0 significa que el modelo no explica nada.
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-top: 40px;'>
        <h3 style='color: white; margin: 0; font-weight: 700;'>⚡ ProyectaGAS</h3>
        <p style='color: rgba(255,255,255,0.9); margin: 10px 0; font-size: 1.1em;'>
            Sistema Inteligente de Predicción de Demanda y Precios
        </p>
        <p style='color: rgba(255,255,255,0.8); margin: 5px 0;'>
            TPLGas | Febrero 2026
        </p>
        <p style='color: rgba(255,255,255,0.7); margin: 5px 0; font-size: 0.9em;'>
            Powered by Machine Learning & Streamlit Cloud
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
