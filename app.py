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
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f0 100%);
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
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* TODOS los textos en blanco */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2 {
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] li {
        color: white !important;
    }
    
    /* Separadores en sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3);
        margin: 20px 0;
    }
    
    /* Alertas en sidebar */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stAlert p {
        color: white !important;
        font-weight: 600;
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

@st.cache_data(ttl=60)  # Cache por solo 60 segundos
def cargar_datos():
    """Carga todos los archivos de predicciones y datos históricos"""
    datos = {}
    
    # Timestamp de carga
    datos['timestamp_carga'] = datetime.now()
    
    archivos = {
        'pred_precios': 'predicciones_futuras_2026.xlsx',
        'historico_precios': 'df_completo_procesado.csv',
        'historico_demanda': 'Data_Demanda.xlsx',  # Datos hasta enero 2026
    }
    
    # Métricas: Priorizar archivos del modelo original (correctos)
    # Las métricas de 3versiones son aproximadas y no representan la precisión real
    archivos_metricas = {
        'metricas_ensemble': ['metricas_ensemble.csv', 'metricas_3versiones.csv'],
        'metricas_resumen': ['metricas_resumen.csv', 'metricas_3versiones_resumen.csv'],
    }
    
    # Intentar cargar predicciones de demanda (primero COMPLETO, luego normal)
    try:
        # Intentar archivo COMPLETO con 3 versiones
        df_demanda = pd.read_excel('predicciones_2026_ensemble_COMPLETO.xlsx')
        df_demanda['Fecha'] = pd.to_datetime(df_demanda['Fecha'])
        datos['pred_demanda'] = df_demanda
        datos['tiene_3_versiones'] = True
    except:
        try:
            # Fallback: archivo normal (1 versión)
            df_demanda = pd.read_excel('predicciones_2026_ensemble.xlsx')
            df_demanda['Fecha'] = pd.to_datetime(df_demanda['Fecha'])
            datos['pred_demanda'] = df_demanda
            datos['tiene_3_versiones'] = False
        except Exception as e:
            st.sidebar.warning(f"⚠️ predicciones_2026_ensemble: {str(e)[:50]}")
            datos['pred_demanda'] = None
            datos['tiene_3_versiones'] = False
    
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
    
    # Cargar métricas (probar múltiples nombres)
    for key, filenames in archivos_metricas.items():
        cargado = False
        for filename in filenames:
            try:
                df = pd.read_csv(filename)
                datos[key] = df
                cargado = True
                break  # Usar el primero que funcione
            except:
                continue
        
        if not cargado:
            datos[key] = None
    
    return datos

def obtener_columna_con_nivel(columna_base, nivel, tiene_3_versiones):
    """
    Retorna el nombre de columna correcto según el nivel seleccionado
    
    Args:
        columna_base: Nombre base (ej: 'Demanda_Total_MBTUD')
        nivel: 'Conservador', 'Moderado', o 'Flexible'
        tiene_3_versiones: Bool indicando si hay 3 versiones disponibles
    
    Returns:
        Nombre de columna con sufijo si aplica
    """
    if not tiene_3_versiones:
        # Archivo antiguo, retornar nombre original
        return columna_base
    
    # Archivo nuevo, agregar sufijo
    return f"{columna_base}_{nivel}"

def obtener_intervalos_confianza(df, columna_base, nivel, tiene_3_versiones):
    """
    Obtiene los límites del intervalo de confianza si existen.
    
    Args:
        df: DataFrame con las predicciones
        columna_base: Nombre base de la columna (ej: 'Demanda_Total_MBTUD')
        nivel: 'Conservador', 'Moderado', o 'Flexible'
        tiene_3_versiones: Bool indicando si hay 3 versiones
    
    Returns:
        tuple: (Serie lower, Serie upper, str nivel_confianza) o (None, None, None) si no existen intervalos
        
    Niveles de confianza:
        - Conservador: ~68% (±1 desviación estándar)
        - Moderado: ~87% (±1.5 desviaciones estándar)
        - Flexible: ~95% (±2 desviaciones estándar)
    """
    if not tiene_3_versiones:
        return None, None, None
    
    col_lower = f"{columna_base}_{nivel}_Lower"
    col_upper = f"{columna_base}_{nivel}_Upper"
    
    if col_lower in df.columns and col_upper in df.columns:
        # Mapeo de nivel a confianza estadística
        confianza_map = {
            'Conservador': '68%',
            'Moderado': '87%',
            'Flexible': '95%'
        }
        nivel_confianza = confianza_map.get(nivel, 'desconocido')
        
        return df[col_lower], df[col_upper], nivel_confianza
    else:
        return None, None, None

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

def calcular_promedios_mensuales(df, columna):
    """Calcula promedios mensuales de una variable"""
    if df is None or columna not in df.columns:
        return None
    
    df_copy = df.copy()
    df_copy['Mes'] = pd.to_datetime(df_copy['Fecha']).dt.month
    df_copy['Mes_Nombre'] = pd.to_datetime(df_copy['Fecha']).dt.month_name()
    
    promedios = df_copy.groupby(['Mes', 'Mes_Nombre'])[columna].agg(['mean', 'min', 'max', 'std']).reset_index()
    promedios.columns = ['Mes', 'Mes_Nombre', 'Promedio', 'Minimo', 'Maximo', 'Std']
    
    return promedios

def filtrar_por_mes(df, mes_numero):
    """Filtra DataFrame por mes (1-12), None para todos"""
    if df is None or mes_numero is None:
        return df
    
    df_copy = df.copy()
    df_copy['Mes'] = pd.to_datetime(df_copy['Fecha']).dt.month
    return df_copy[df_copy['Mes'] == mes_numero].drop('Mes', axis=1)

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
            
            # Usar add_shape en lugar de add_vline (más compatible)
            try:
                # Convertir a timestamp
                if hasattr(fecha_corte, 'to_pydatetime'):
                    fecha_ts = fecha_corte.to_pydatetime()
                elif hasattr(fecha_corte, 'timestamp'):
                    fecha_ts = fecha_corte
                else:
                    fecha_ts = pd.to_datetime(fecha_corte)
                
                # Agregar línea vertical con add_shape
                fig.add_shape(
                    type="line",
                    x0=fecha_ts,
                    x1=fecha_ts,
                    y0=0,
                    y1=1,
                    yref="paper",
                    line=dict(color="gray", width=2, dash="dash")
                )
                
                # Agregar anotación separada
                fig.add_annotation(
                    x=fecha_ts,
                    y=1,
                    yref="paper",
                    text="Inicio Predicción",
                    showarrow=False,
                    yshift=10,
                    font=dict(size=12, color="gray")
                )
            except Exception as e:
                # Si falla, continuar sin la línea
                pass
    
    # Calcular rango apropiado del eje Y (enfocado en datos relevantes)
    all_values = []
    
    # Usar solo los últimos 180 días del histórico (ya filtrados)
    if df_hist is not None and columna_hist in df_hist.columns:
        hist_filtrado_temp = df_hist.tail(180)
        hist_valores = hist_filtrado_temp[columna_hist].dropna().values
        all_values.extend(hist_valores)
    
    # Agregar predicciones
    if df_pred is not None and columna_pred in df_pred.columns:
        pred_valores = df_pred[columna_pred].dropna().values
        all_values.extend(pred_valores)
    
    if all_values:
        y_min = min(all_values)
        y_max = max(all_values)
        y_range = y_max - y_min
        
        # Margen reducido para ver mejor fluctuaciones (5% en lugar de 10%)
        margen = y_range * 0.05
        y_min_plot = max(0, y_min - margen)  # No permitir negativos
        y_max_plot = y_max + margen
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
        
        archivos_ok = sum(1 for k, v in datos.items() if k != 'timestamp_carga' and v is not None)
        total_archivos = len([k for k in datos.keys() if k != 'timestamp_carga'])
        
        if archivos_ok == total_archivos:
            st.success(f"✅ {archivos_ok}/{total_archivos} archivos cargados")
        else:
            st.warning(f"⚠️ {archivos_ok}/{total_archivos} archivos cargados")
        
        # Mostrar timestamp de carga
        if 'timestamp_carga' in datos:
            st.caption(f"🕒 Última actualización: {datos['timestamp_carga'].strftime('%H:%M:%S')}")
        
        # Selector de nivel de ajuste (solo si tiene 3 versiones)
        nivel_ajuste = 'Moderado'  # Valor por defecto
        if datos.get('tiene_3_versiones', False):
            st.markdown("---")
            st.markdown("### 🎯 Nivel de Ajuste")
            
            nivel_ajuste = st.selectbox(
                "Selecciona nivel de predicción:",
                options=['Conservador', 'Moderado', 'Flexible'],
                index=1,  # Moderado por defecto
                help="""
                **Conservador**: Intervalo estrecho (~68% confianza, ±1 desviación estándar)
                **Moderado**: Balance óptimo (~87% confianza, ±1.5 desviaciones estándar)
                **Flexible**: Intervalo amplio (~95% confianza, ±2 desviaciones estándar)
                
                ℹ️ Los 3 niveles muestran la MISMA predicción óptima del modelo.
                Solo cambia el rango de incertidumbre estadístico.
                """
            )
            
            # Explicación del nivel seleccionado
            if nivel_ajuste == 'Conservador':
                st.caption("📊 Intervalo: ±1 desviación estándar (~68% confianza)")
            elif nivel_ajuste == 'Moderado':
                st.caption("📊 Intervalo: ±1.5 desviaciones estándar (~87% confianza)")
            else:
                st.caption("📊 Intervalo: ±2 desviaciones estándar (~95% confianza)")
        else:
            st.markdown("---")
            st.info("""
            💡 **Tip**: Para habilitar intervalos de confianza y selector de nivel, 
            ejecuta las celdas adicionales del notebook:
            `08_ENSEMBLE_FINAL_CON_INTERVALOS_CONFIANZA.ipynb`
            """)
        
        # Botón para limpiar cache y forzar recarga
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.info("""
        **Características:**
        - ✅ Comparación con datos reales
        - ✅ Unidades visibles
        - ✅ Rangos optimizados
        - ✅ Métricas de precisión
        """)
    
    # Definir diccionario de meses (usado en todos los tabs)
    meses_dict = {
        'Todos los meses': None,
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Resumen Mensual", 
        "💵 Precios Internacionales", 
        "📊 Demanda Total", 
        "🏭 Sectores", 
        "📈 Métricas del Modelo"
    ])
    
    # ========================================================================
    # TAB 1: RESUMEN MENSUAL (NUEVO)
    # ========================================================================
    with tab1:
        st.markdown("### 📅 Resumen Mensual - Todas las Variables")
        st.markdown("Selecciona un mes para ver el promedio de todas las variables predichas")
        
        # Selector de mes prominente
        col_sel1, col_sel2, col_sel3 = st.columns([1, 2, 1])
        with col_sel2:
            mes_resumen = st.selectbox(
                "🗓️ Selecciona el mes:",
                options=list(meses_dict.keys()),
                key='mes_resumen',
                index=0
            )
        
        mes_numero_resumen = meses_dict[mes_resumen]
        
        if mes_numero_resumen is None:
            st.warning("⚠️ Por favor selecciona un mes específico para ver el resumen")
        else:
            # Filtrar todos los datos
            pred_precios_mes = filtrar_por_mes(datos['pred_precios'], mes_numero_resumen) if datos['pred_precios'] is not None else None
            pred_demanda_mes = filtrar_por_mes(datos['pred_demanda'], mes_numero_resumen) if datos['pred_demanda'] is not None else None
            
            if pred_precios_mes is not None or pred_demanda_mes is not None:
                dias_mes = len(pred_precios_mes) if pred_precios_mes is not None else len(pred_demanda_mes)
                st.success(f"📊 Mostrando promedios de **{mes_resumen} 2026** (basado en {dias_mes} días)")
                
                st.markdown("---")
                
                # ============================================================
                # SECCIÓN 1: PRECIOS INTERNACIONALES
                # ============================================================
                st.markdown("### 💵 Precios Internacionales")
                
                col_precio1, col_precio2 = st.columns(2)
                
                with col_precio1:
                    if pred_precios_mes is not None:
                        col_hh = None
                        for c in ['HenryHub_USD_MMBtu_Predicho', 'HenryHub_USD_MMBtu', 'HenryHub']:
                            if c in pred_precios_mes.columns:
                                col_hh = c
                                break
                        
                        if col_hh:
                            prom_hh = pred_precios_mes[col_hh].mean()
                            min_hh = pred_precios_mes[col_hh].min()
                            max_hh = pred_precios_mes[col_hh].max()
                            
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 25px; border-radius: 15px; color: white; text-align: center;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <h3 style='margin: 0; color: white; font-size: 1.2em;'>💰 Henry Hub (USA)</h3>
                                <h1 style='margin: 15px 0; color: white; font-size: 2.5em; font-weight: bold;'>
                                    ${prom_hh:.2f}
                                </h1>
                                <p style='margin: 0; color: white; font-size: 1.1em; opacity: 0.95;'>USD/MMBtu</p>
                                <hr style='border-color: rgba(255,255,255,0.3); margin: 15px 0;'>
                                <div style='display: flex; justify-content: space-around; margin-top: 10px;'>
                                    <div>
                                        <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9em;'>Mínimo</p>
                                        <p style='margin: 5px 0; color: white; font-size: 1.1em; font-weight: bold;'>${min_hh:.2f}</p>
                                    </div>
                                    <div>
                                        <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9em;'>Máximo</p>
                                        <p style='margin: 5px 0; color: white; font-size: 1.1em; font-weight: bold;'>${max_hh:.2f}</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                with col_precio2:
                    if pred_precios_mes is not None:
                        col_ttf = None
                        for c in ['TTF_USD_MMBtu_Predicho', 'TTF_USD_MMBtu', 'TTF']:
                            if c in pred_precios_mes.columns:
                                col_ttf = c
                                break
                        
                        if col_ttf:
                            prom_ttf = pred_precios_mes[col_ttf].mean()
                            min_ttf = pred_precios_mes[col_ttf].min()
                            max_ttf = pred_precios_mes[col_ttf].max()
                            
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                        padding: 25px; border-radius: 15px; color: white; text-align: center;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <h3 style='margin: 0; color: white; font-size: 1.2em;'>💰 TTF (Europa)</h3>
                                <h1 style='margin: 15px 0; color: white; font-size: 2.5em; font-weight: bold;'>
                                    ${prom_ttf:.2f}
                                </h1>
                                <p style='margin: 0; color: white; font-size: 1.1em; opacity: 0.95;'>USD/MMBtu</p>
                                <hr style='border-color: rgba(255,255,255,0.3); margin: 15px 0;'>
                                <div style='display: flex; justify-content: space-around; margin-top: 10px;'>
                                    <div>
                                        <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9em;'>Mínimo</p>
                                        <p style='margin: 5px 0; color: white; font-size: 1.1em; font-weight: bold;'>${min_ttf:.2f}</p>
                                    </div>
                                    <div>
                                        <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9em;'>Máximo</p>
                                        <p style='margin: 5px 0; color: white; font-size: 1.1em; font-weight: bold;'>${max_ttf:.2f}</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # ============================================================
                # SECCIÓN 2: DEMANDA TOTAL
                # ============================================================
                st.markdown("### 📊 Demanda de Gas Natural")
                
                if pred_demanda_mes is not None:
                    # Buscar columna con nivel seleccionado
                    col_dem = obtener_columna_con_nivel(
                        'Demanda_Total_MBTUD', 
                        nivel_ajuste,
                        datos.get('tiene_3_versiones', False)
                    )
                    
                    # Fallback si no existe
                    if col_dem not in pred_demanda_mes.columns:
                        for c in ['Demanda_Total_MBTUD', 'Total_MBTUD', 'Demanda_Total']:
                            if c in pred_demanda_mes.columns:
                                col_dem = c
                                break
                    
                    if col_dem and col_dem in pred_demanda_mes.columns:
                        prom_dem = pred_demanda_mes[col_dem].mean()
                        min_dem = pred_demanda_mes[col_dem].min()
                        max_dem = pred_demanda_mes[col_dem].max()
                        std_dem = pred_demanda_mes[col_dem].std()
                        
                        # Card grande para demanda total
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                    padding: 30px; border-radius: 15px; color: white; text-align: center;
                                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                            <h3 style='margin: 0; color: white; font-size: 1.3em;'>🔥 Demanda Total Nacional</h3>
                            <h1 style='margin: 15px 0; color: white; font-size: 3em; font-weight: bold;'>
                                {prom_dem:,.0f}
                            </h1>
                            <p style='margin: 0; color: white; font-size: 1.2em; opacity: 0.95;'>MBTUD</p>
                            <hr style='border-color: rgba(255,255,255,0.3); margin: 20px 0;'>
                            <div style='display: flex; justify-content: space-around; margin-top: 15px;'>
                                <div>
                                    <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.95em;'>Mínimo</p>
                                    <p style='margin: 5px 0; color: white; font-size: 1.2em; font-weight: bold;'>{min_dem:,.0f}</p>
                                </div>
                                <div>
                                    <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.95em;'>Máximo</p>
                                    <p style='margin: 5px 0; color: white; font-size: 1.2em; font-weight: bold;'>{max_dem:,.0f}</p>
                                </div>
                                <div>
                                    <p style='margin: 0; color: rgba(255,255,255,0.8); font-size: 0.95em;'>Desv. Est.</p>
                                    <p style='margin: 5px 0; color: white; font-size: 1.2em; font-weight: bold;'>{std_dem:,.0f}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # ============================================================
                # SECCIÓN 3: DEMANDA POR SECTORES
                # ============================================================
                st.markdown("### 🏭 Demanda por Sectores y Regiones")
                
                if pred_demanda_mes is not None:
                    sectores_dict = {
                        "Costa": "Demanda_Costa_Total_MBTUD",
                        "Interior": "Demanda_Interior_Total_MBTUD",
                        "Industrial": "Demanda_Industrial_Total_MBTUD",
                        "Refinería": "Demanda_Refineria_Total_MBTUD",
                        "Petrolero": "Demanda_Petrolero_Total_MBTUD",
                        "Generación Térmica": "Demanda_GeneracionTermica_Total_MBTUD",
                        "Residencial": "Demanda_Residencial_Total_MBTUD",
                        "Comercial": "Demanda_Comercial_Total_MBTUD",
                        "GNVC": "Demanda_GNVC_Total_MBTUD",
                        "Compresora": "Demanda_Compresora_Total_MBTUD"
                    }
                    
                    # Crear tabla de sectores
                    data_tabla = []
                    for sector, columna_base in sectores_dict.items():
                        # Obtener nombre de columna con nivel
                        columna = obtener_columna_con_nivel(
                            columna_base,
                            nivel_ajuste,
                            datos.get('tiene_3_versiones', False)
                        )
                        
                        # Fallback a columna original si no existe
                        if columna not in pred_demanda_mes.columns:
                            columna = columna_base
                        
                        if columna in pred_demanda_mes.columns:
                            prom = pred_demanda_mes[columna].mean()
                            minimo = pred_demanda_mes[columna].min()
                            maximo = pred_demanda_mes[columna].max()
                            data_tabla.append({
                                'Sector': sector,
                                'Promedio': f"{prom:,.0f}",
                                'Mínimo': f"{minimo:,.0f}",
                                'Máximo': f"{maximo:,.0f}",
                                'Promedio_Num': prom
                            })
                    
                    if data_tabla:
                        df_tabla = pd.DataFrame(data_tabla)
                        df_tabla = df_tabla.sort_values('Promedio_Num', ascending=False)
                        df_tabla = df_tabla[['Sector', 'Promedio', 'Mínimo', 'Máximo']]
                        
                        st.markdown(f"**Promedios de demanda por sector en {mes_resumen} 2026** (en MBTUD)")
                        st.dataframe(
                            df_tabla,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Sector": st.column_config.TextColumn("🏭 Sector", width="medium"),
                                "Promedio": st.column_config.TextColumn("📊 Promedio", width="medium"),
                                "Mínimo": st.column_config.TextColumn("📉 Mínimo", width="medium"),
                                "Máximo": st.column_config.TextColumn("📈 Máximo", width="medium"),
                            }
                        )
                        
                        # Gráfico de barras
                        st.markdown("#### 📊 Comparación Visual por Sector")
                        fig_sectores = go.Figure()
                        
                        sectores_ordenados = [row['Sector'] for _, row in df_tabla.iterrows()]
                        promedios_num = [float(row['Promedio'].replace(',', '')) for _, row in df_tabla.iterrows()]
                        
                        fig_sectores.add_trace(go.Bar(
                            x=sectores_ordenados,
                            y=promedios_num,
                            marker_color='rgb(79, 172, 254)',
                            text=[f"{p:,.0f}" for p in promedios_num],
                            textposition='outside',
                            hovertemplate='<b>%{x}</b><br>Promedio: %{y:,.0f} MBTUD<extra></extra>'
                        ))
                        
                        fig_sectores.update_layout(
                            title=f"Demanda Promedio por Sector - {mes_resumen} 2026",
                            xaxis_title="Sector",
                            yaxis_title="Demanda (MBTUD)",
                            height=500,
                            showlegend=False,
                            hovermode='x'
                        )
                        
                        st.plotly_chart(fig_sectores, use_container_width=True)
            else:
                st.error("❌ No hay datos disponibles para mostrar el resumen mensual")
    
    # ========================================================================
    # TAB 2: PRECIOS (antes Tab 1)
    # ========================================================================
    with tab2:
        st.markdown("### 💵 Predicción de Precios Internacionales")
        st.markdown("Predicciones para Henry Hub (USA) y TTF (Europa) - Año 2026")
        
        # Filtro de mes
        st.markdown("---")
        mes_seleccionado = st.selectbox(
            "📅 Filtrar por mes:",
            options=list(meses_dict.keys()),
            key='mes_precios'
        )
        mes_numero = meses_dict[mes_seleccionado]
        
        # Filtrar datos
        if mes_numero is not None and datos['pred_precios'] is not None:
            pred_precios_filtrado = filtrar_por_mes(datos['pred_precios'], mes_numero)
            st.info(f"📊 Mostrando promedios de **{mes_seleccionado}** (basado en {len(pred_precios_filtrado)} días)")
            
            # PANEL DE RESUMEN MENSUAL
            st.markdown("---")
            st.markdown(f"### 📋 Resumen de Precios - {mes_seleccionado} 2026")
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                # Henry Hub
                if 'HenryHub_USD_MMBtu_Predicho' in pred_precios_filtrado.columns:
                    prom_hh = pred_precios_filtrado['HenryHub_USD_MMBtu_Predicho'].mean()
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                        <h4 style='margin: 0; color: white;'>💰 Henry Hub</h4>
                        <h2 style='margin: 10px 0; color: white;'>${prom_hh:.2f} USD/MMBtu</h2>
                        <p style='margin: 0; color: rgba(255,255,255,0.9);'>Promedio {mes_seleccionado}</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif 'HenryHub_USD_MMBtu' in pred_precios_filtrado.columns:
                    prom_hh = pred_precios_filtrado['HenryHub_USD_MMBtu'].mean()
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                        <h4 style='margin: 0; color: white;'>💰 Henry Hub</h4>
                        <h2 style='margin: 10px 0; color: white;'>${prom_hh:.2f} USD/MMBtu</h2>
                        <p style='margin: 0; color: rgba(255,255,255,0.9);'>Promedio {mes_seleccionado}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_res2:
                # TTF
                if 'TTF_USD_MMBtu_Predicho' in pred_precios_filtrado.columns:
                    prom_ttf = pred_precios_filtrado['TTF_USD_MMBtu_Predicho'].mean()
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                        <h4 style='margin: 0; color: white;'>💰 TTF</h4>
                        <h2 style='margin: 10px 0; color: white;'>${prom_ttf:.2f} USD/MMBtu</h2>
                        <p style='margin: 0; color: rgba(255,255,255,0.9);'>Promedio {mes_seleccionado}</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif 'TTF_USD_MMBtu' in pred_precios_filtrado.columns:
                    prom_ttf = pred_precios_filtrado['TTF_USD_MMBtu'].mean()
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                        <h4 style='margin: 0; color: white;'>💰 TTF</h4>
                        <h2 style='margin: 10px 0; color: white;'>${prom_ttf:.2f} USD/MMBtu</h2>
                        <p style='margin: 0; color: rgba(255,255,255,0.9);'>Promedio {mes_seleccionado}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
        else:
            pred_precios_filtrado = datos['pred_precios']
            if pred_precios_filtrado is not None:
                st.info(f"📊 Mostrando promedio anual 2026 (basado en {len(pred_precios_filtrado)} días)")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Henry Hub (USD/MMBtu)")
            
            if pred_precios_filtrado is not None:
                col_hh_pred = None
                for c in ['HenryHub_USD_MMBtu_Predicho', 'HenryHub_USD_MMBtu', 'HenryHub']:
                    if c in pred_precios_filtrado.columns:
                        col_hh_pred = c
                        break
                
                col_hh_hist = None
                if datos['historico_precios'] is not None:
                    for c in ['HenryHub_USD_MMBtu', 'HenryHub']:
                        if c in datos['historico_precios'].columns:
                            col_hh_hist = c
                            break
                
                if col_hh_pred:
                    # Solo mostrar gráfica si es "Todos los meses"
                    if mes_numero is None:
                        fig_hh = crear_grafico_con_historico(
                            datos['pred_precios'],
                            datos['historico_precios'],
                            col_hh_pred,
                            col_hh_hist,
                            "Henry Hub - Predicción 2026",
                            unidad="USD/MMBtu"
                        )
                        st.plotly_chart(fig_hh, use_container_width=True)
                    
                    # Métricas con datos filtrados
                    metricas_hh = calcular_metricas(pred_precios_filtrado[col_hh_pred])
                    
                    if metricas_hh:
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("📊 Promedio", f"${metricas_hh['promedio']:.2f}")
                        col_b.metric("📉 Mínimo", f"${metricas_hh['minimo']:.2f}")
                        col_c.metric("📈 Máximo", f"${metricas_hh['maximo']:.2f}")
        
        with col2:
            st.markdown("#### TTF (USD/MMBtu)")
            
            if pred_precios_filtrado is not None:
                col_ttf_pred = None
                for c in ['TTF_USD_MMBtu_Predicho', 'TTF_USD_MMBtu', 'TTF']:
                    if c in pred_precios_filtrado.columns:
                        col_ttf_pred = c
                        break
                
                col_ttf_hist = None
                if datos['historico_precios'] is not None:
                    for c in ['TTF_USD_MMBtu', 'TTF']:
                        if c in datos['historico_precios'].columns:
                            col_ttf_hist = c
                            break
                
                if col_ttf_pred:
                    # Solo mostrar gráfica si es "Todos los meses"
                    if mes_numero is None:
                        fig_ttf = crear_grafico_con_historico(
                            datos['pred_precios'],
                            datos['historico_precios'],
                            col_ttf_pred,
                            col_ttf_hist,
                            "TTF - Predicción 2026",
                            unidad="USD/MMBtu"
                        )
                        st.plotly_chart(fig_ttf, use_container_width=True)
                    
                    # Métricas con datos filtrados
                    metricas_ttf = calcular_metricas(pred_precios_filtrado[col_ttf_pred])
                    
                    if metricas_ttf:
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("📊 Promedio", f"${metricas_ttf['promedio']:.2f}")
                        col_b.metric("📉 Mínimo", f"${metricas_ttf['minimo']:.2f}")
                        col_c.metric("📈 Máximo", f"${metricas_ttf['maximo']:.2f}")
        
        # Tablas de promedios mensuales
        if mes_numero is None:  # Solo mostrar si es "Todos los meses"
            st.markdown("---")
            with st.expander("📅 Ver Promedios Mensuales Detallados"):
                col_tabla1, col_tabla2 = st.columns(2)
                
                with col_tabla1:
                    st.markdown("##### Henry Hub por Mes")
                    if col_hh_pred and datos['pred_precios'] is not None:
                        prom_hh = calcular_promedios_mensuales(datos['pred_precios'], col_hh_pred)
                        if prom_hh is not None:
                            tabla_hh = prom_hh.copy()
                            tabla_hh['Promedio'] = tabla_hh['Promedio'].apply(lambda x: f"${x:.2f}")
                            tabla_hh['Minimo'] = tabla_hh['Minimo'].apply(lambda x: f"${x:.2f}")
                            tabla_hh['Maximo'] = tabla_hh['Maximo'].apply(lambda x: f"${x:.2f}")
                            tabla_hh = tabla_hh[['Mes_Nombre', 'Promedio', 'Minimo', 'Maximo']]
                            tabla_hh.columns = ['Mes', 'Promedio', 'Mín', 'Máx']
                            st.dataframe(tabla_hh, use_container_width=True, hide_index=True)
                
                with col_tabla2:
                    st.markdown("##### TTF por Mes")
                    if col_ttf_pred and datos['pred_precios'] is not None:
                        prom_ttf = calcular_promedios_mensuales(datos['pred_precios'], col_ttf_pred)
                        if prom_ttf is not None:
                            tabla_ttf = prom_ttf.copy()
                            tabla_ttf['Promedio'] = tabla_ttf['Promedio'].apply(lambda x: f"${x:.2f}")
                            tabla_ttf['Minimo'] = tabla_ttf['Minimo'].apply(lambda x: f"${x:.2f}")
                            tabla_ttf['Maximo'] = tabla_ttf['Maximo'].apply(lambda x: f"${x:.2f}")
                            tabla_ttf = tabla_ttf[['Mes_Nombre', 'Promedio', 'Minimo', 'Maximo']]
                            tabla_ttf.columns = ['Mes', 'Promedio', 'Mín', 'Máx']
                            st.dataframe(tabla_ttf, use_container_width=True, hide_index=True)

    # ========================================================================
    # TAB 3: DEMANDA TOTAL
    # ========================================================================
    with tab3:
        st.markdown("### 📊 Predicción de Demanda Total de Gas Natural")
        st.markdown("Demanda agregada nacional - Año 2026")
        
        # Filtro de mes
        st.markdown("---")
        mes_seleccionado_dem = st.selectbox(
            "📅 Filtrar por mes:",
            options=list(meses_dict.keys()),
            key='mes_demanda'
        )
        mes_numero_dem = meses_dict[mes_seleccionado_dem]
        
        # Filtrar datos
        if mes_numero_dem is not None and datos['pred_demanda'] is not None:
            pred_demanda_filtrado = filtrar_por_mes(datos['pred_demanda'], mes_numero_dem)
            st.info(f"📊 Mostrando promedios de **{mes_seleccionado_dem}** (basado en {len(pred_demanda_filtrado)} días)")
        else:
            pred_demanda_filtrado = datos['pred_demanda']
            if pred_demanda_filtrado is not None:
                st.info(f"📊 Mostrando promedio anual 2026 (basado en {len(pred_demanda_filtrado)} días)")
        
        st.markdown("---")
        
        if pred_demanda_filtrado is not None:
            # Buscar columna con nivel seleccionado
            col_dem_pred = obtener_columna_con_nivel(
                'Demanda_Total_MBTUD',
                nivel_ajuste,
                datos.get('tiene_3_versiones', False)
            )
            
            # Fallback si no existe
            if col_dem_pred not in pred_demanda_filtrado.columns:
                for c in ['Demanda_Total_MBTUD', 'Total_MBTUD', 'Demanda_Total']:
                    if c in pred_demanda_filtrado.columns:
                        col_dem_pred = c
                        break
            
            col_dem_hist = None
            if datos['historico_demanda'] is not None:
                for c in ['Demanda_Total_MBTUD', 'Total_MBTUD', 'Demanda_Total']:
                    if c in datos['historico_demanda'].columns:
                        col_dem_hist = c
                        break
            
            if col_dem_pred and col_dem_pred in pred_demanda_filtrado.columns:
                # Solo mostrar gráfica si es "Todos los meses"
                if mes_numero_dem is None:
                    fig_dem = crear_grafico_con_historico(
                        datos['pred_demanda'],
                        datos['historico_demanda'],
                        col_dem_pred,
                        col_dem_hist,
                        "Demanda Total - Predicción 2026",
                        unidad="MBTUD"
                    )
                    st.plotly_chart(fig_dem, use_container_width=True)
                
                # Métricas con datos filtrados
                metricas_dem = calcular_metricas(pred_demanda_filtrado[col_dem_pred])
                
                if metricas_dem:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📊 Promedio", f"{metricas_dem['promedio']:,.0f} MBTUD")
                    col2.metric("📉 Mínimo", f"{metricas_dem['minimo']:,.0f} MBTUD")
                    col3.metric("📈 Máximo", f"{metricas_dem['maximo']:,.0f} MBTUD")
                    col4.metric("📊 Desv. Est.", f"{metricas_dem['std']:,.0f} MBTUD")
                
                # Análisis de tendencia solo si es "Todos los meses"
                if mes_numero_dem is None:
                    st.markdown("#### 📈 Análisis de Tendencia")
                    valores = datos['pred_demanda'][col_dem_pred].values
                    primer_trimestre = np.mean(valores[:90])
                    ultimo_trimestre = np.mean(valores[-90:])
                    cambio_pct = ((ultimo_trimestre - primer_trimestre) / primer_trimestre) * 100
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Q1 2026", f"{primer_trimestre:,.0f} MBTUD")
                    col_b.metric("Q4 2026", f"{ultimo_trimestre:,.0f} MBTUD")
                    col_c.metric("Variación", f"{cambio_pct:+.2f}%")
                
                # Tabla de promedios mensuales
                st.markdown("---")
                with st.expander("📅 Ver Promedios Mensuales Detallados"):
                    promedios_mensuales = calcular_promedios_mensuales(datos['pred_demanda'], col_dem_pred)
                    if promedios_mensuales is not None:
                        st.markdown("##### Demanda Total por Mes - 2026")
                        
                        # Formatear tabla
                        tabla_display = promedios_mensuales.copy()
                        tabla_display['Promedio'] = tabla_display['Promedio'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_display['Minimo'] = tabla_display['Minimo'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_display['Maximo'] = tabla_display['Maximo'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_display['Std'] = tabla_display['Std'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_display = tabla_display[['Mes_Nombre', 'Promedio', 'Minimo', 'Maximo', 'Std']]
                        tabla_display.columns = ['Mes', 'Promedio', 'Mínimo', 'Máximo', 'Desv. Est.']
                        
                        st.dataframe(tabla_display, use_container_width=True, hide_index=True)

    # ========================================================================
    # TAB 4: SECTORES
    # ========================================================================
    with tab4:
        st.markdown("### 🏭 Predicción por Sectores y Regiones")
        
        # Filtro de mes
        st.markdown("---")
        col_filtro1, col_filtro2 = st.columns(2)
        
        with col_filtro1:
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
                "🏭 Seleccionar sector:",
                list(sectores_disponibles.keys())
            )
        
        with col_filtro2:
            mes_seleccionado_sector = st.selectbox(
                "📅 Filtrar por mes:",
                options=list(meses_dict.keys()),
                key='mes_sector'
            )
        
        mes_numero_sector = meses_dict[mes_seleccionado_sector]
        columna_sector_base = sectores_disponibles[sector_seleccionado]
        
        # Obtener columna con nivel seleccionado
        columna_sector = obtener_columna_con_nivel(
            columna_sector_base,
            nivel_ajuste,
            datos.get('tiene_3_versiones', False)
        )
        
        # Filtrar datos
        if mes_numero_sector is not None and datos['pred_demanda'] is not None:
            pred_sector_filtrado = filtrar_por_mes(datos['pred_demanda'], mes_numero_sector)
            st.info(f"📊 Mostrando promedios de **{sector_seleccionado}** en **{mes_seleccionado_sector}** (basado en {len(pred_sector_filtrado)} días)")
        else:
            pred_sector_filtrado = datos['pred_demanda']
            if pred_sector_filtrado is not None:
                st.info(f"📊 Mostrando promedio anual 2026 de **{sector_seleccionado}** (basado en {len(pred_sector_filtrado)} días)")
        
        st.markdown("---")
        
        # Fallback si columna con nivel no existe
        if pred_sector_filtrado is not None:
            if columna_sector not in pred_sector_filtrado.columns:
                columna_sector = columna_sector_base
        
        if pred_sector_filtrado is not None and columna_sector in pred_sector_filtrado.columns:
            # Solo mostrar gráfica si es "Todos los meses"
            if mes_numero_sector is None:
                fig_sector = crear_grafico_con_historico(
                    datos['pred_demanda'],
                    None,
                    columna_sector,
                    None,
                    f"Sector {sector_seleccionado} - Predicción 2026",
                    unidad="MBTUD"
                )
                st.plotly_chart(fig_sector, use_container_width=True)
            
            # Métricas con datos filtrados
            metricas_sector = calcular_metricas(pred_sector_filtrado[columna_sector])
            
            if metricas_sector:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📊 Promedio", f"{metricas_sector['promedio']:,.0f} MBTUD")
                col2.metric("📉 Mínimo", f"{metricas_sector['minimo']:,.0f} MBTUD")
                col3.metric("📈 Máximo", f"{metricas_sector['maximo']:,.0f} MBTUD")
                col4.metric("📊 Coef. Var.", f"{metricas_sector['cv']:.2f}%")
            
            # Tabla de promedios mensuales
            if mes_numero_sector is None:  # Solo si es "Todos los meses"
                st.markdown("---")
                with st.expander(f"📅 Ver Promedios Mensuales de {sector_seleccionado}"):
                    promedios_sector = calcular_promedios_mensuales(datos['pred_demanda'], columna_sector)
                    if promedios_sector is not None:
                        st.markdown(f"##### {sector_seleccionado} por Mes - 2026")
                        
                        tabla_sector = promedios_sector.copy()
                        tabla_sector['Promedio'] = tabla_sector['Promedio'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_sector['Minimo'] = tabla_sector['Minimo'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_sector['Maximo'] = tabla_sector['Maximo'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_sector['Std'] = tabla_sector['Std'].apply(lambda x: f"{x:,.0f} MBTUD")
                        tabla_sector = tabla_sector[['Mes_Nombre', 'Promedio', 'Minimo', 'Maximo', 'Std']]
                        tabla_sector.columns = ['Mes', 'Promedio', 'Mínimo', 'Máximo', 'Desv. Est.']
                        
                        st.dataframe(tabla_sector, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # TAB 5: MÉTRICAS DEL MODELO
    # ========================================================================
    with tab5:
        st.markdown("### 📈 Métricas de Precisión del Modelo")
        st.markdown("Evaluación del desempeño de los modelos de predicción")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Métricas por Variable (Demanda)")
            
            if datos['metricas_ensemble'] is not None:
                df_metricas = datos['metricas_ensemble'].copy()
                
                # Verificar qué columnas tiene el archivo
                if 'MAPE' in df_metricas.columns:
                    # Nuevo formato del notebook (con 3 versiones)
                    df_display = df_metricas[['Variable', 'MAPE', 'Promedio_Predicho', 'Promedio_Historico']].copy()
                    df_display.columns = ['Variable', 'MAPE', 'Prom. Predicho', 'Prom. Histórico']
                elif 'MAPE_Test' in df_metricas.columns:
                    # Formato antiguo
                    df_display = df_metricas.copy()
                    df_display['MAPE_Test'] = df_display['MAPE_Test'].apply(lambda x: f"{x:.2f}%")
                    if 'R2_Test' in df_display.columns:
                        df_display['R2_Test'] = df_display['R2_Test'].apply(lambda x: f"{x:.3f}")
                        df_display.columns = ['Variable', 'MAPE (%)', 'R² Score', 'Ensemble']
                    else:
                        df_display.columns = ['Variable', 'MAPE (%)']
                else:
                    df_display = df_metricas
                
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("""
                **Interpretación:**
                - **MAPE**: Error porcentual medio absoluto (menor = mejor)
                  - < 2%: Excelente
                  - 2-5%: Muy bueno
                  - 5-10%: Bueno
                  - > 10%: Necesita mejora
                """)
        
        with col2:
            st.markdown("#### 💎 Calidad de las Predicciones")
            
            if datos['metricas_resumen'] is not None:
                df_resumen = datos['metricas_resumen'].copy()
                
                # Detectar formato del archivo
                if 'Modelo' in df_resumen.columns and 'MAPE_Promedio' in df_resumen.columns:
                    # FORMATO NUEVO (Notebook 08 con 3 versiones)
                    st.info(f"""
                    **Modelo:** {df_resumen['Modelo'].iloc[0]}  
                    **MAPE Promedio:** {df_resumen['MAPE_Promedio'].iloc[0]}  
                    **Variables Evaluadas:** {df_resumen['Variables_Evaluadas'].iloc[0]}  
                    **Nivel de Ajuste:** {df_resumen['Nivel_Ajuste'].iloc[0]}
                    """)
                    
                elif 'Variable' in df_resumen.columns:
                    # FORMATO ANTIGUO (Notebook 07)
                    # Mostrar métricas como cards mejoradas
                    for idx, row in df_resumen.iterrows():
                        variable = row['Variable']
                        # Usar nombres correctos de columnas
                        mape = row.get('MAPE_Test', row.get('MAPE', 0))
                        r2 = row.get('R2_Test', row.get('R²', 0))
                        
                        # Si mape es string, convertir
                        if isinstance(mape, str):
                            mape = float(mape.replace('%', ''))
                        if isinstance(r2, str):
                            r2 = float(r2)
                        
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
                else:
                    st.warning("Formato de métricas no reconocido")
        
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
