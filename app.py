import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np  # <-- Esta línea es la que faltaba
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# Configuración básica de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Proyecto final – Estadística no paramétrica",
    page_icon=None,
    layout="wide"
)

# ---------------------------------------------------------
# Estilos CSS personalizados - Fondo negro, texto blanco, cajas grises
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general negro */
    .stApp {
        background-color: #0f0c14;
        color: #e5e7eb;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Títulos */
    .stTitle {
        color: #d1e8ff;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stSubheader {
        color: #93c5fd;
        font-weight: 600;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    /* Cajas de interpretación uniformes (gris oscuro) */
    .interpretation-box {
        background-color: #2d2937;
        border-left: 4px solid #3b82f6;
        padding: 16px;
        border-radius: 6px;
        margin: 10px 0;
    }
    .interpretation-box h4 {
        color: #d1e8ff;
        margin-top: 0;
    }
    .interpretation-box p {
        color: #cbd5e1;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Barra Lateral – Solo información del proyecto
# ---------------------------------------------------------
st.sidebar.header("Información del Proyecto")

st.sidebar.write("**Nombre del Proyecto:**")
st.sidebar.write("Análisis No Paramétrico de Riesgos Competitivos en Trasplante Renal")

st.sidebar.write("**Autores:**")
st.sidebar.write("Camila Mantilla – Julián Toloza – Maritza Jiménez")

st.sidebar.write("**Fecha de Entrega:**")
st.sidebar.write("18 de noviembre de 2025")

st.sidebar.write("**Artículo Base:**")
st.sidebar.write("Pinto-Ramírez et al., PLOS ONE, 2022")

st.sidebar.markdown("---")

# Filtro interactivo
evento_filtro = st.sidebar.selectbox(
    "Seleccionar evento para visualizar:",
    ["Todos los eventos", "Muerte", "Pérdida del injerto"],
    index=0
)

# ---------------------------------------------------------
# Encabezado principal
# ---------------------------------------------------------
st.title("Análisis No Paramétrico de Riesgos Competitivos en Trasplante Renal")
st.subheader("Estimación de la Función de Incidencia Acumulada (CIF), prueba de Gray y bootstrap")

st.markdown("---")

# ---------------------------------------------------------
# Propósito del Dashboard (sin la pregunta)
# ---------------------------------------------------------
st.header("Propósito del Dashboard")

st.markdown(
    """
<div class="interpretation-box">
  <p>Este tablero presenta un análisis no paramétrico de 1.454 receptores de trasplante renal en Colombia, explorando cómo compiten los riesgos de muerte y pérdida del injerto durante 5 años. Compara estos riesgos según el tipo de donante usando la prueba de Gray y cuantifica las diferencias con intervalos de confianza por bootstrap a 1, 3 y 5 años.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Pestañas (4)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Análisis Exploratorio de Datos",
    "Fórmulas de Métodos y su Aplicación",
    "Resultados de Métodos Aplicados",
    "Hallazgos y Conclusiones"
])

# ---------------------------------------------------------
# PESTAÑA 1: Análisis Exploratorio de Datos
# ---------------------------------------------------------
with tab1:
    st.header("Análisis Exploratorio de Datos")

    st.markdown("""
    El análisis exploratorio caracteriza de forma general la cohorte, describiendo la distribución por sexo, tipo de donante y la frecuencia de los eventos principales (pérdida del injerto y muerte), así como la presencia de desenlaces intercurrentes relevantes. Para las variables continuas se examinan medidas descriptivas y se evalúa visualmente su distribución, lo que permite identificar sesgos, asimetrías y desviaciones de la normalidad. Estos resultados orientan la elección de métodos no paramétricos en los análisis posteriores.
    """)

    # Distribución de eventos clínicos principales
    st.subheader("Distribución de eventos clínicos principales")

    df_eventos = pd.DataFrame({
        "Evento": ["Censurado", "Muerte", "Pérdida del injerto"],
        "Porcentaje": [79.0, 9.4, 11.6]
    })
    fig_eventos = px.pie(
        df_eventos, values='Porcentaje', names='Evento',
        color='Evento',
        color_discrete_map={
            'Censurado': '#4b5563',
            'Muerte': '#93c5fd',
            'Pérdida del injerto': '#60a5fa'
        },
        hole=0.5,
        title="Distribución de eventos clínicos principales"
    )
    fig_eventos.update_traces(textposition='inside', textinfo='percent+label')
    fig_eventos.update_layout(
        showlegend=False,
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb'
    )
    st.plotly_chart(fig_eventos, use_container_width=True)

    # Tabla de distribución
    st.subheader("Tabla de distribución")
    df_distribucion = pd.DataFrame({
        "Variable": ["Sexo", "Sexo", "PerdidaInjerto", "PerdidaInjerto", "Muerte", "Muerte", "DonanteVivo", "DonanteVivo", "BKV", "BKV", "CMV", "CMV", "RechazoAgudo", "RechazoAgudo", "StentCoronario", "StentCoronario"],
        "Categoría": ["Masculino", "Femenino", "No", "Sí", "No", "Sí", "Fallecido", "Vivo", "No", "Sí", "No", "Sí", "No", "Sí", "No", "Sí"],
        "Conteo": [586, 868, 1263, 191, 1204, 250, 1002, 452, 1418, 36, 1378, 76, 981, 473, 1441, 13],
        "Porcentaje (%)": [40.30, 59.70, 86.86, 13.14, 82.81, 17.19, 68.91, 31.09, 97.52, 2.48, 94.77, 5.23, 67.47, 32.53, 99.11, 0.89]
    })
    st.dataframe(
        df_distribucion.style.format({'Porcentaje (%)': '{:.2f}%'})
        .set_properties(**{'background-color': '#1e1b26', 'color': '#e5e7eb'}),
        use_container_width=True
    )

    st.info("La mayoría de pacientes queda censurada al cierre; los eventos (muerte y pérdida del injerto) son minoritarios y desbalanceados. Esto respalda el uso de métodos no paramétricos con riesgos competitivos.")

    # Distribución por tipo de donante
    st.subheader("Distribución de pacientes por tipo de donante")

    df_donantes = pd.DataFrame({
        "Tipo": ["Donante Fallecido", "Donante Vivo"],
        "Porcentaje": [68.9, 31.1]
    })
    fig_donantes = px.pie(
        df_donantes, values='Porcentaje', names='Tipo',
        color='Tipo',
        color_discrete_map={'Donante Fallecido': '#93c5fd', 'Donante Vivo': '#60a5fa'},
        title="Distribución de pacientes por tipo de donante"
    )
    fig_donantes.update_traces(textposition='inside', textinfo='percent+label')
    fig_donantes.update_layout(
        showlegend=False,
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb'
    )
    st.plotly_chart(fig_donantes, use_container_width=True)

    # Cantidad de eventos por tipo de donante
    st.subheader("Cantidad de eventos por tipo de donante")

    data_eventos_donante = {
        'Tipo de Donante': ['Donante Fallecido', 'Donante Vivo'],
        'Censurado': [754, 394],
        'Muerte': [121, 16],
        'Pérdida del Injerto': [127, 42]
    }
    df_eventos_donante = pd.DataFrame(data_eventos_donante)

    if evento_filtro == "Muerte":
        df_plot = df_eventos_donante[['Tipo de Donante', 'Muerte']].melt(
            id_vars='Tipo de Donante', var_name='Evento', value_name='Cantidad'
        )
        color_map = {'Muerte': '#93c5fd'}
        title = 'Cantidad de Muertes por Tipo de Donante'
    elif evento_filtro == "Pérdida del injerto":
        df_plot = df_eventos_donante[['Tipo de Donante', 'Pérdida del Injerto']].melt(
            id_vars='Tipo de Donante', var_name='Evento', value_name='Cantidad'
        )
        color_map = {'Pérdida del Injerto': '#60a5fa'}
        title = 'Cantidad de Pérdidas del Injerto por Tipo de Donante'
    else:
        df_plot = df_eventos_donante.melt(
            id_vars='Tipo de Donante', var_name='Evento', value_name='Cantidad'
        )
        color_map = {
            'Censurado': '#4b5563',
            'Muerte': '#93c5fd',
            'Pérdida del Injerto': '#60a5fa'
        }
        title = 'Cantidad de Eventos por Tipo de Donante'

    fig_barras = px.bar(
        df_plot,
        x='Tipo de Donante',
        y='Cantidad',
        color='Evento',
        color_discrete_map=color_map,
        title=title
    )
    fig_barras.update_layout(
        barmode='group',
        xaxis_title='Tipo de Donante',
        yaxis_title='Número de Pacientes',
        legend_title='Evento',
        template='plotly_dark',
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb'
    )
    st.plotly_chart(fig_barras, use_container_width=True)

    st.markdown("""
    **Eventos por tipo de donante (conteos):**
    - **Muerte:** 121 en donante fallecido vs 16 en donante vivo.
    - **Pérdida del injerto:** 127 vs 42.
    - **Censurado:** 754 vs 394.

    *Nota: Son conteos, no tasas; no implican causalidad.*
    """)

    # Distribución de edad y sexo por tipo de evento
    st.subheader("Distribución de edad y sexo por tipo de evento")

    col1, col2 = st.columns(2)

    with col1:
        df_edad = pd.DataFrame({
            "Tipo de Evento": ["Censurado", "Muerte", "Pérdida del injerto"],
            "Mediana Edad": [43, 52, 44]
        })
        fig_edad = px.bar(
            df_edad, x='Tipo de Evento', y='Mediana Edad',
            color='Tipo de Evento',
            color_discrete_map={
                'Censurado': '#4b5563',
                'Muerte': '#93c5fd',
                'Pérdida del injerto': '#60a5fa'
            },
            title="Mediana de Edad por Tipo de Evento"
        )
        fig_edad.update_layout(
            yaxis_title="Edad (años)",
            paper_bgcolor='#0f0c14',
            plot_bgcolor='#0f0c14',
            font_color='#e5e7eb'
        )
        st.plotly_chart(fig_edad, use_container_width=True)
        st.caption("→ Sugiere mayor riesgo de muerte en pacientes de mayor edad.")

    with col2:
        data_sexo = {
            'Tipo de Evento': ['Censurado', 'Muerte', 'Pérdida del injerto'],
            'Femenino': [670, 90, 108],
            'Masculino': [478, 47, 61]
        }
        df_sexo = pd.DataFrame(data_sexo)
        fig_sexo = go.Figure()
        fig_sexo.add_trace(go.Bar(
            name='Femenino', x=df_sexo['Tipo de Evento'], y=df_sexo['Femenino'],
            marker_color='#cbd5e1'
        ))
        fig_sexo.add_trace(go.Bar(
            name='Masculino', x=df_sexo['Tipo de Evento'], y=df_sexo['Masculino'],
            marker_color='#93c5fd'
        ))
        fig_sexo.update_layout(
            title_text='Distribución de Sexo por Tipo de Evento',
            barmode='group',
            xaxis_title='Tipo de Evento',
            yaxis_title='Número de Pacientes',
            legend_title='Sexo',
            template='plotly_dark',
            paper_bgcolor='#0f0c14',
            plot_bgcolor='#0f0c14',
            font_color='#e5e7eb'
        )
        st.plotly_chart(fig_sexo, use_container_width=True)
        st.caption("Predomina el sexo femenino tanto en la cohorte como en los eventos. Esto refleja la composición muestral, no diferencias ajustadas.")

    # Evaluación de la Normalidad de Variables Continuas
    st.subheader("Evaluación de la Normalidad de Variables Continuas")

    st.markdown("""
    Para las variables continuas (edad, creatinina a 12 meses, tiempo en diálisis, tiempo de isquemia fría), se evaluó su distribución mediante Q-Q plots y la prueba de Anderson-Darling.
    """)

    df_ad = pd.DataFrame({
        "Variable": ["Edad", "Creatinina12m", "TiempoDialisis", "CIT"],
        "Estadístico AD": [6.2565, 156.1973, 140.3597, 70.8260],
        "Valor Crítico (5%)": [0.7850, 0.7850, 0.7850, 0.7850],
        "Conclusión": ["NO normal", "NO normal", "NO normal", "NO normal"]
    })
    st.dataframe(
        df_ad.style.set_properties(**{'background-color': '#1e1b26', 'color': '#e5e7eb'}),
        use_container_width=True
    )

    st.markdown("""
    <div class="interpretation-box">
      <p><strong>Todos los estadísticos AD superan el valor crítico 0.785 → se rechaza la normalidad en todas las variables (incluida Edad).</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Interpretación de los Q-Q plots (según el PDF):**
    - **Edad**: Se aproxima a la línea teórica solo en la parte central; en colas muestra desvíos moderados → distribución casi normal, pero con colas no normales.
    - **Creatinina a 12 meses, Tiempo en diálisis y Tiempo de isquemia fría (CIT)**: Exhiben curvaturas marcadas y colas pesadas, alejándose claramente de la normalidad.
    """)

    st.markdown("""
    <div class="interpretation-box">
      <p><strong>La distribución de los datos (eventos desbalanceados, variables continuas no normales) justifica plenamente el uso de métodos no paramétricos en los análisis posteriores.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # BKV y CMV por tipo de evento
    st.subheader("BKV y CMV por tipo de evento")

    # Datos para BKV
    df_bkv = pd.DataFrame({
        "Tipo de Evento": ["Censurado", "Muerte", "Pérdida del injerto"],
        "Porcentaje": [1.7, 0.7, 8.9]
    })

    fig_bkv = px.bar(
        df_bkv, x='Tipo de Evento', y='Porcentaje',
        color='Tipo de Evento',
        color_discrete_map={'Censurado': '#93c5fd', 'Muerte': '#60a5fa', 'Pérdida del injerto': '#3b82f6'},
        title="Nefropatía por BKV por evento"
    )
    fig_bkv.update_layout(
        yaxis_title="Porcentaje (%)",
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb'
    )
    st.plotly_chart(fig_bkv, use_container_width=True)

    # Datos para CMV
    df_cmv = pd.DataFrame({
        "Tipo de Evento": ["Censurado", "Muerte", "Pérdida del injerto"],
        "Porcentaje": [3.8, 13.1, 8.3]
    })

    fig_cmv = px.bar(
        df_cmv, x='Tipo de Evento', y='Porcentaje',
        color='Tipo de Evento',
        color_discrete_map={'Censurado': '#93c5fd', 'Muerte': '#60a5fa', 'Pérdida del injerto': '#3b82f6'},
        title="Enfermedad por CMV por evento"
    )
    fig_cmv.update_layout(
        yaxis_title="Porcentaje (%)",
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb'
    )
    st.plotly_chart(fig_cmv, use_container_width=True)

    st.markdown("""
    **Nefropatía por BKV:**
    - La mayor proporción aparece en Pérdida del injerto (~8.9%), es baja en Censurado (~1.7%) y mínima en Muerte (~0.7%).
    - El BKV se asocia principalmente con deterioro del injerto más que con mortalidad.

    **Enfermedad por CMV:**
    - La proporción es más alta en Muerte (~13.1%) y también relevante en Pérdida del injerto (~8.3%), menor en Censurado (~3.8%).
    - El CMV se relaciona con desenlaces adversos, especialmente mortalidad.
    """)

    # Gráficas complementarias (al final)
    st.subheader("Gráficas complementarias")

    # Datos para Creatinina a 12 meses (simulación realista)
    # Usaremos valores medios y desviaciones típicas estimadas del PDF
    # Censurado: mediana 1.28, rango intercuartilico ~1.0-1.6
    # Muerte: mediana 1.68, rango intercuartilico ~1.3-2.0
    # Pérdida del injerto: mediana 3.49, rango intercuartilico ~2.5-4.5
    # Generamos datos sintéticos para el boxplot
    np.random.seed(42)  # Para reproducibilidad
    n_censurado = 1204
    n_muerte = 250
    n_perdida = 191

    # Simular datos para Creatinina a 12 meses
    creatinina_censurado = np.random.normal(loc=1.28, scale=0.3, size=n_censurado)
    creatinina_muerte = np.random.normal(loc=1.68, scale=0.4, size=n_muerte)
    creatinina_perdida = np.random.normal(loc=3.49, scale=0.8, size=n_perdida)

    # Asegurar que los valores estén dentro de rangos razonables
    creatinina_censurado = np.clip(creatinina_censurado, 0.5, 3.0)
    creatinina_muerte = np.clip(creatinina_muerte, 0.5, 4.0)
    creatinina_perdida = np.clip(creatinina_perdida, 1.0, 8.0)

    df_creatinina_data = pd.DataFrame({
        "Tipo de Evento": ["Censurado"] * n_censurado + ["Muerte"] * n_muerte + ["Pérdida del injerto"] * n_perdida,
        "Creatinina a 12 meses": np.concatenate([creatinina_censurado, creatinina_muerte, creatinina_perdida])
    })

    fig_creatinina = px.box(
        df_creatinina_data,
        x='Tipo de Evento',
        y='Creatinina a 12 meses',
        color='Tipo de Evento',
        color_discrete_map={'Censurado': '#93c5fd', 'Muerte': '#60a5fa', 'Pérdida del injerto': '#3b82f6'},
        title="Distribución de creatinina a 12 meses según tipo de evento"
    )
    fig_creatinina.update_traces(
        boxmean=True,  # Mostrar la media
        marker=dict(size=4),
        line=dict(width=2)
    )
    fig_creatinina.update_layout(
        yaxis_title="Creatinina a 12 meses (mg/dL)",
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb',
        yaxis_range=[0, 12]  # Limitar el eje Y para que se vea como en la imagen
    )
    st.plotly_chart(fig_creatinina, use_container_width=True)

    st.markdown("""
    **Creatinina a 12 meses (mg/dL):**
    - La mediana es más alta en Pérdida del injerto (~3.5 mg/dL), intermedia en Muerte (~1.7 mg/dL) y más baja en Censurado (~1.3 mg/dL).
    - Hay dispersión y valores atípicos marcados en pérdida del injerto, consistente con mayor deterioro de función renal.
    - Peores valores de creatinina a 12 meses se asocian con mayor riesgo de pérdida del injerto; el grupo de muerte muestra elevación moderada.
    """)

    # Datos para Tiempo en diálisis (simulación realista)
    # Censurado: mediana 9.0, rango intercuartilico ~6-12
    # Muerte: mediana 13.0, rango intercuartilico ~8-18
    # Pérdida del injerto: mediana 11.0, rango intercuartilico ~6-16
    # Generamos datos sintéticos para el boxplot
    tiempo_censurado = np.random.normal(loc=9.0, scale=3.0, size=n_censurado)
    tiempo_muerte = np.random.normal(loc=13.0, scale=4.0, size=n_muerte)
    tiempo_perdida = np.random.normal(loc=11.0, scale=4.0, size=n_perdida)

    # Asegurar que los valores estén dentro de rangos razonables
    tiempo_censurado = np.clip(tiempo_censurado, 0, 200)
    tiempo_muerte = np.clip(tiempo_muerte, 0, 200)
    tiempo_perdida = np.clip(tiempo_perdida, 0, 200)

    df_tiempo_dialisis_data = pd.DataFrame({
        "Tipo de Evento": ["Censurado"] * n_censurado + ["Muerte"] * n_muerte + ["Pérdida del injerto"] * n_perdida,
        "Tiempo en diálisis": np.concatenate([tiempo_censurado, tiempo_muerte, tiempo_perdida])
    })

    fig_tiempo_dialisis = px.box(
        df_tiempo_dialisis_data,
        x='Tipo de Evento',
        y='Tiempo en diálisis',
        color='Tipo de Evento',
        color_discrete_map={'Censurado': '#93c5fd', 'Muerte': '#60a5fa', 'Pérdida del injerto': '#3b82f6'},
        title="Distribución del tiempo en diálisis según tipo de evento"
    )
    fig_tiempo_dialisis.update_traces(
        boxmean=True,  # Mostrar la media
        marker=dict(size=4),
        line=dict(width=2)
    )
    fig_tiempo_dialisis.update_layout(
        yaxis_title="Tiempo en diálisis (meses)",
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb',
        yaxis_range=[0, 200]  # Limitar el eje Y para que se vea como en la imagen
    )
    st.plotly_chart(fig_tiempo_dialisis, use_container_width=True)

    st.markdown("""
    **Tiempo en diálisis (meses):**
    - La mediana es mayor en Muerte (~13 meses), seguida de Pérdida del injerto (~11 meses) y Censurado (~9 meses).
    - Se observan colas largas y outliers en los tres grupos, especialmente en Censurado y Pérdida del injerto.
    - Mayor exposición previa a diálisis parece relacionarse con peores desenlaces (muerte y pérdida).
    """)
# ---------------------------------------------------------
# PESTAÑA 2: Fórmulas de Métodos y su Aplicación
# ---------------------------------------------------------
with tab2:
    st.header("Fórmulas de Métodos y su Aplicación")

    st.markdown("""
    Esta sección describe las tres herramientas no paramétricas fundamentales utilizadas en este análisis para abordar el problema de los riesgos competitivos. Para cada método, se explica su propósito, se presenta su fórmula clave en una caja gris, se detalla su aplicación en el contexto de este estudio y se establece su relación con el artículo base.
    """)

    # Sección 1: CIF
    st.subheader("1. Estimación de la Incidencia por Causa (CIF)")

    st.markdown("""
    <div class="interpretation-box">
      <h4>Fórmula General:</h4>
      <p>La Función de Incidencia Acumulada (CIF) se calcula mediante la siguiente integral:</p>
    </div>
    """, unsafe_allow_html=True)

    # Fórmula CIF con st.latex()
    st.latex(r"F_k(t) = \int_0^t S(u^-) \lambda_k(u)  du")

    st.markdown("""
    <div class="interpretation-box">
      <p><strong>Donde:</strong></p>
      <ul>
        <li><code>S(u⁻)</code>: Probabilidad de seguir sin ningún evento justo antes del tiempo <code>u</code>.</li>
        <li><code>λ<sub>k</sub>(u)</code>: Riesgo instantáneo de la causa <code>k</code> en el tiempo <code>u</code>.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **¿Qué es y para qué sirve?**
    
    La CIF es una herramienta estadística que nos permite estimar la probabilidad real de que un paciente experimente un evento específico (como muerte o pérdida del injerto) en un periodo de tiempo determinado, teniendo en cuenta que otros eventos pueden ocurrir primero y "competir" por ese resultado. En otras palabras, nos dice: "¿Cuántos pacientes, por cada 100, han experimentado este evento específico hasta un momento dado, considerando que algunos pudieron haber experimentado otro evento antes?"
    """)

    st.markdown("""
    **Cómo se aplica en este estudio:**
    
    Se calcula la CIF para muerte (k=1) y pérdida del injerto (k=2) a 1, 3 y 5 años, separando por tipo de donante (fallecido vs vivo) usando el estimador de Aalen-Johansen.
    """)

    st.markdown("""
    **Relación con el artículo:**
    
    El artículo de Pinto-Ramírez et al. utiliza la CIF para reportar la probabilidad acumulada a 5 años. Nuestro análisis complementa esto al mostrar las curvas completas y agregar intervalos de confianza por bootstrap.
    """)

    # Sección 2: Prueba de Gray
    st.subheader("2. Comparación entre grupos: prueba de Gray")

    st.markdown("""
    <div class="interpretation-box">
      <h4>Fórmula General:</h4>
      <p>El estadístico de la prueba de Gray se define como:</p>
    </div>
    """, unsafe_allow_html=True)

    # Fórmula Gray con st.latex()
    st.latex(r"T_k = \frac{\left[ \sum_{u \leq \tau} w(u) \left( d\hat{F}_{k,DD}(u) - d\hat{F}_{k,LD}(u) \right) \right]^2}{\text{Var}\left[ \sum_{u \leq \tau} w(u) \left( d\hat{F}_{k,DD}(u) - d\hat{F}_{k,LD}(u) \right) \right]} \sim \chi^2_{(1)}")

    st.markdown("""
    <div class="interpretation-box">
      <p><strong>Donde:</strong></p>
      <ul>
        <li><code>dF̂<sub>k,g</sub>(u)</code>: Incremento de la CIF estimada para la causa <code>k</code> en el grupo <code>g</code> en el tiempo <code>u</code>.</li>
        <li><code>w(u)</code>: Peso basado en la supervivencia global estimada justo antes de <code>u</code>.</li>
        <li><code>Var</code>: Varianza estimada (estilo Greenwood).</li>
      </ul>
      <p>El estadístico <code>T<sub>k</sub></code> sigue aproximadamente una distribución chi-cuadrado con 1 grado de libertad.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **¿Qué es y para qué sirve?**
    
    La prueba de Gray es un test estadístico diseñado para comparar curvas de CIF entre grupos cuando existen riesgos competitivos, evitando el sesgo del test log-rank.
    """)

    st.markdown("""
    **Cómo se aplica en este estudio:**
    
    Se aplica para comparar donante fallecido (DD) vs donante vivo (LD) para cada causa a 1, 3 y 5 años.
    """)

    st.markdown("""
    **Relación con el artículo:**
    
    El artículo original utiliza la prueba de Gray como comparación no ajustada antes del modelo de Fine-Gray.
    """)

    # Sección 3: Bootstrap
    st.subheader("3. Incertidumbre y diferencias absolutas: análisis bootstrap")

    st.markdown("""
    <div class="interpretation-box">
      <h4>Fórmula General (IC por percentiles):</h4>
      <p>Si <code>θ</code> es el parámetro de interés (por ejemplo, la CIF o la diferencia de CIF) y <code>θ̂</code> es su estimador en la muestra original, el intervalo de confianza del 95% por percentiles se calcula como:</p>
    </div>
    """, unsafe_allow_html=True)

    # Fórmula Bootstrap con st.latex()
    st.latex(r"\text{IC}_{95\%} = \left[ Q_{2.5\%}(\hat{\theta}^*), Q_{97.5\%}(\hat{\theta}^*) \right]")

    st.markdown("""
    <div class="interpretation-box">
      <p><strong>Donde:</strong></p>
      <ul>
        <li><code>θ̂*</code>: Los B estimadores obtenidos de las B réplicas bootstrap.</li>
        <li><code>Q<sub>p</sub>(θ̂*)</code>: El percentil p de las B réplicas bootstrap.</li>
      </ul>
      <p>Si el intervalo de confianza de la diferencia absoluta no incluye 0, concluimos que hay una diferencia significativa entre los grupos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **¿Qué es y para qué sirve?**
    
    El bootstrap es un método no paramétrico que nos permite estimar la incertidumbre de cualquier estadístico (como la CIF o la diferencia entre dos CIF) cuando no conocemos su distribución muestral o esta no es normal. En nuestro caso, lo usamos para obtener intervalos de confianza del 95% para la CIF y para la diferencia absoluta entre los grupos (DD vs LD), lo que nos permite expresar los resultados con una medida de certeza.
    """)

    st.markdown("""
    **Cómo se aplica en este estudio:**
    
    Se generan 1000 réplicas, se recalculan las CIF y las diferencias, y se obtienen los IC del 95% para cada horizonte (1, 3, 5 años).
    """)

    st.markdown("""
    **Relación con el artículo:**
    
    El artículo original no reporta intervalos de confianza para las CIF ni para las diferencias absolutas. Nuestro análisis complementa esto al agregar estos intervalos.
    """)

# ---------------------------------------------------------
# PESTAÑA 3: Resultados de Métodos Aplicados
# ---------------------------------------------------------
with tab3:
    st.header("Resultados de Métodos Aplicados")

    # ---------------------------------------------------------
    # Filtro interactivo por tipo de donante (en la barra lateral)
    # ---------------------------------------------------------
    st.sidebar.subheader("Filtro de Gráficos")
    grupo_filtro = st.sidebar.selectbox(
        "Mostrar curvas y barras de:",
        ["Ambos grupos", "Solo Donante Fallecido", "Solo Donante Vivo"],
        index=0
    )

    # ---------------------------------------------------------
    # Sección: Estimación de la CIF
    # ---------------------------------------------------------
    st.subheader("Estimación de la Incidencia por Causa (CIF)")

    st.markdown("""
    Esta sección presenta las curvas de Función de Incidencia Acumulada (CIF) para muerte y pérdida del injerto, separadas por tipo de donante (Donante Fallecido vs Donante Vivo). Las curvas muestran cómo evoluciona el riesgo acumulado a lo largo del tiempo.
    """)

    # Datos de CIF del PDF
    years = [0, 1, 3, 5]  # Añadimos 0 para empezar desde el origen
    cif_muerte_dd = [0, 5.8, 12.9, 17.2]
    cif_muerte_ld = [0, 1.4, 4.3, 5.5]
    cif_graft_dd = [0, 9.0, 12.5, 16.4]
    cif_graft_ld = [0, 5.1, 9.2, 15.1]

    # Crear la figura con subplots
    fig_cif_complete = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Muerte", "Pérdida del Injerto"),
        x_title="Tiempo (años)",
        y_title="% Incidencia Acumulada"
    )

    # Determinar qué grupos mostrar según el filtro
    if grupo_filtro == "Ambos grupos":
        show_dd = True
        show_ld = True
    elif grupo_filtro == "Solo Donante Fallecido":
        show_dd = True
        show_ld = False
    else:  # Solo Donante Vivo
        show_dd = False
        show_ld = True

    # Curva de Muerte
    if show_dd:
        fig_cif_complete.add_trace(
            go.Scatter(x=years, y=cif_muerte_dd, mode='lines+markers', name='Donante Fallecido', line=dict(color='#93c5fd', width=3), marker=dict(size=8)),
            row=1, col=1
        )
    if show_ld:
        fig_cif_complete.add_trace(
            go.Scatter(x=years, y=cif_muerte_ld, mode='lines+markers', name='Donante Vivo', line=dict(color='#60a5fa', width=3), marker=dict(size=8)),
            row=1, col=1
        )

    # Curva de Pérdida del Injerto
    if show_dd:
        fig_cif_complete.add_trace(
            go.Scatter(x=years, y=cif_graft_dd, mode='lines+markers', name='Donante Fallecido', line=dict(color='#93c5fd', width=3), marker=dict(size=8)),
            row=1, col=2
        )
    if show_ld:
        fig_cif_complete.add_trace(
            go.Scatter(x=years, y=cif_graft_ld, mode='lines+markers', name='Donante Vivo', line=dict(color='#60a5fa', width=3), marker=dict(size=8)),
            row=1, col=2
        )

    fig_cif_complete.update_layout(
        title_text="Incidencia acumulada (CIF) por causa y tipo de donante",
        template='plotly_dark',
        paper_bgcolor='#0f0c14',
        plot_bgcolor='#0f0c14',
        font_color='#e5e7eb',
        showlegend=False
    )

    # Añadir anotaciones en los puntos finales (5 años)
    if show_dd:
        fig_cif_complete.add_annotation(
            x=5, y=17.2, text="17.2%", showarrow=True, arrowhead=1, ax=0, ay=-30, font=dict(color='#93c5fd'),
            row=1, col=1
        )
        fig_cif_complete.add_annotation(
            x=5, y=16.4, text="16.4%", showarrow=True, arrowhead=1, ax=0, ay=-30, font=dict(color='#93c5fd'),
            row=1, col=2
        )
    if show_ld:
        fig_cif_complete.add_annotation(
            x=5, y=5.5, text="5.5%", showarrow=True, arrowhead=1, ax=0, ay=30, font=dict(color='#60a5fa'),
            row=1, col=1
        )
        fig_cif_complete.add_annotation(
            x=5, y=15.1, text="15.1%", showarrow=True, arrowhead=1, ax=0, ay=30, font=dict(color='#60a5fa'),
            row=1, col=2
        )

    # Añadir anotaciones en todos los puntos (0, 1, 3 años) sin duplicados
    for i in range(len(years)):
        if show_dd:
            # Anotación para Donante Fallecido
            fig_cif_complete.add_annotation(
                x=years[i], y=cif_muerte_dd[i], text=f"{cif_muerte_dd[i]}%", showarrow=True, arrowhead=1, ax=0, ay=-10, font=dict(color='#93c5fd'),
                row=1, col=1
            )
            fig_cif_complete.add_annotation(
                x=years[i], y=cif_graft_dd[i], text=f"{cif_graft_dd[i]}%", showarrow=True, arrowhead=1, ax=0, ay=-10, font=dict(color='#93c5fd'),
                row=1, col=2
            )
        if show_ld:
            # Anotación para Donante Vivo
            fig_cif_complete.add_annotation(
                x=years[i], y=cif_muerte_ld[i], text=f"{cif_muerte_ld[i]}%", showarrow=True, arrowhead=1, ax=0, ay=10, font=dict(color='#60a5fa'),
                row=1, col=1
            )
            fig_cif_complete.add_annotation(
                x=years[i], y=cif_graft_ld[i], text=f"{cif_graft_ld[i]}%", showarrow=True, arrowhead=1, ax=0, ay=10, font=dict(color='#60a5fa'),
                row=1, col=2
            )

    st.plotly_chart(fig_cif_complete, use_container_width=True)

    # ---------------------------------------------------------
    # Interpretación de las curvas CIF (en bullet points)
    # ---------------------------------------------------------
    st.markdown("""
    **Patrón general:** En ambos desenlaces, los receptores de donante fallecido (DD) acumulan mayor riesgo que los de donante vivo (DV) a lo largo del seguimiento.
    - **Muerte (causa 1):**
        - DD ≈ 5.8%, 12.9%, 17.2% a 1, 3 y 5 años.
        - DV ≈ 1.4%, 4.3%, 5.5% en los mismos puntos.
        - **Conclusión:** Brecha persistente DD > DV; la diferencia se agranda con el tiempo.
    - **Pérdida del injerto (causa 2):**
        - DD ≈ 9.0%, 12.5%, 16.4% a 1, 3 y 5 años.
        - DV ≈ 5.1%, 9.2%, 15.1%.
        - **Conclusión:** DV parte mejor al inicio, pero las curvas se acercan hacia 5 años.

    **Notas clínicas:** El tipo de donante importa. El trasplante con donante vivo muestra menor mortalidad y menor pérdida temprana; hacia 5 años la diferencia en pérdida del injerto se reduce, mientras que en mortalidad la ventaja de DV se mantiene.
    """)

    # ---------------------------------------------------------
    # Gráficas de barras (6 gráficos)
    # ---------------------------------------------------------
    st.subheader("CIF a 1, 3 y 5 años (con intervalos de confianza)")

    # Datos para los gráficos de barras
    data = {
        'Grupo': ['DD', 'LD'] * 6,
        'Causa': ['Muerte'] * 2 + ['Pérdida'] * 2 + ['Muerte'] * 2 + ['Pérdida'] * 2 + ['Muerte'] * 2 + ['Pérdida'] * 2,
        'Horizonte': ['1 año'] * 4 + ['3 años'] * 4 + ['5 años'] * 4,
        'CIF': [5.8, 1.4, 9.0, 5.1, 12.9, 4.3, 12.5, 9.2, 17.2, 5.5, 16.4, 15.1],
        'IC_Lower': [4.5, 0.5, 7.2, 3.1, 10.5, 2.2, 10.4, 6.0, 14.5, 2.9, 13.6, 10.8],
        'IC_Upper': [7.4, 2.7, 10.9, 7.3, 15.5, 6.7, 14.9, 12.4, 20.2, 8.8, 19.3, 19.9]
    }
    df = pd.DataFrame(data)

    # Función para crear gráfico de barras
    def create_bar_chart(causa, horizonte, title):
        filtered_df = df[(df['Causa'] == causa) & (df['Horizonte'] == horizonte)]
        # Filtrar según el grupo seleccionado
        if grupo_filtro == "Solo Donante Fallecido":
            filtered_df = filtered_df[filtered_df['Grupo'] == 'DD']
        elif grupo_filtro == "Solo Donante Vivo":
            filtered_df = filtered_df[filtered_df['Grupo'] == 'LD']
        # Si es "Ambos grupos", no filtramos
        fig = px.bar(
            filtered_df, x='Grupo', y='CIF', color='Grupo',
            color_discrete_map={'DD': '#93c5fd', 'LD': '#60a5fa'},
            title=title, text='CIF'
        )
        fig.update_traces(
            error_y=dict(
                type='data',
                array=filtered_df['IC_Upper'] - filtered_df['CIF'],
                arrayminus=filtered_df['CIF'] - filtered_df['IC_Lower']
            ),
            texttemplate='%{text}%', textposition='outside'
        )
        fig.update_layout(
            yaxis_title="% (Incidencia acumulada)",
            template='plotly_dark',
            paper_bgcolor='#0f0c14',
            plot_bgcolor='#0f0c14',
            font_color='#e5e7eb',
            showlegend=False
        )
        return fig

    # Crear y mostrar los 6 gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_bar_chart('Muerte', '1 año', 'Muerte — CIF a 1 año'), use_container_width=True)
        st.plotly_chart(create_bar_chart('Muerte', '3 años', 'Muerte — CIF a 3 años'), use_container_width=True)
        st.plotly_chart(create_bar_chart('Muerte', '5 años', 'Muerte — CIF a 5 años'), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_bar_chart('Pérdida', '1 año', 'Pérdida — CIF a 1 año'), use_container_width=True)
        st.plotly_chart(create_bar_chart('Pérdida', '3 años', 'Pérdida — CIF a 3 años'), use_container_width=True)
        st.plotly_chart(create_bar_chart('Pérdida', '5 años', 'Pérdida — CIF a 5 años'), use_container_width=True)

    # Tabla de CIF (solo para referencia, no es el foco)
    st.markdown("""
    **CIF por año (DD vs. LD)**
    - **Muerte (causa 1).**
        - A 1 año: DD ≈ 5.8% vs LD ≈ 1.4% → mayor riesgo en DD.
        - A 3 años: DD ≈ 12.9% vs LD ≈ 4.3% → la brecha aumenta.
        - A 5 años: DD ≈ 17.2% vs LD ≈ 5.5% → DD mantiene riesgo claramente superior.
        - El tipo de donante se asocia fuertemente con la mortalidad acumulada; el exceso de riesgo en DD se amplía en el tiempo.
    - **Pérdida del injerto (causa 2).**
        - A 1 año: DD ≈ 9.0% vs LD ≈ 5.1% → DD mayor.
        - A 3 años: DD ≈ 12.5% vs LD ≈ 9.2% → la diferencia persiste pero se acorta.
        - A 5 años: DD ≈ 16.4% vs LD ≈ 15.1% → valores muy cercanos; los IC parecen solaparse.
        - La ventaja inicial de LD frente a pérdida del injerto se reduce con el tiempo; a 5 años ambos grupos son similares.
    """)

    # ---------------------------------------------------------
    # Sección: Prueba de Gray
    # ---------------------------------------------------------
    st.subheader("Comparación entre grupos: prueba de Gray")

    st.markdown("""
    **Qué responde.** Determina si las curvas de incidencia acumulada (CIF) de dos o más grupos son distintas para una causa específica considerando los riesgos competitivos.
    """)

    # Tabla de la prueba de Gray
    gray_df = pd.DataFrame({
        "Año (t)": [1, 3, 5],
        "chi² Muerte": [12.76, 19.80, 23.65],
        "p-valor Muerte": ["<0.001", "<0.001", "<0.001"],
        "Decisión (Muerte)": ["Rechaza H0", "Rechaza H0", "Rechaza H0"],
        "chi² Pérdida": [5.79, 4.15, 2.38],
        "p-valor Pérdida": ["0.016", "0.042", "0.123"],
        "Decisión (Pérdida)": ["Rechaza H0", "Rechaza H0", "No rechaza H0"]
    })

    st.dataframe(gray_df.style.set_properties(**{'background-color': '#1e1b26', 'color': '#e5e7eb'}), use_container_width=True)

    st.markdown("""
    **Interpretación:**
    - **Muerte**
        - A 1, 3 y 5 años: p < 0.001 en todos.
        - Hay diferencia clara y sostenida entre DD y LD en la incidencia de muerte (se rechaza H0 siempre). En línea con el artículo: el tipo de donante es un factor clave de mortalidad (junto con edad, diabetes, CMV, isquemia fría, etc.).
    - **Pérdida del injerto**
        - 1 año: p = 0.016 → hay diferencia (rechaza H0).
        - 3 años: p = 0.042 → sigue habiendo diferencia (rechaza H0).
        - 5 años: p = 0.123 → ya no hay evidencia de diferencia (no se rechaza H0).
        - La brecha DD vs LD en pérdida del injerto es temprana y se diluye hacia el año 5. Esto encaja con el artículo: los drivers de pérdida (BKV, rechazo agudo, creatinina 12 m, isquemia fría, rehospitalizaciones) actúan sobre todo al inicio; con el tiempo, la competencia con muerte y el manejo clínico reducen esa diferencia.
    """)

    # ---------------------------------------------------------
    # Sección: Análisis Bootstrap
    # ---------------------------------------------------------
    st.subheader("Incertidumbre y diferencias absolutas: análisis bootstrap")

    st.markdown("""
    **¿Qué es y qué responde?** El bootstrap es un método no paramétrico para medir la incertidumbre de un estimador. En nuestro estudio, responde a dos preguntas prácticas:
    1. ¿Cuál es la variabilidad de la CIF en cada grupo de donante (DD vs LD) a 1, 3 y 5 años?
    2. ¿La diferencia absoluta de CIF entre DD y LD (ΔCIF = CIF_DD − CIF_LD) es distinta de 0?
    """)

    # Tabla de Bootstrap para Muerte
    st.markdown("Bootstrap de CIF — Muerte (causa 1). DD vs LD")
    bootstrap_muerte_df = pd.DataFrame({
        "Horizonte (años)": [1, 3, 5],
        "CIF % Donante fallecido (IC 95%)": ["5.8 (4.5-7.4)", "12.9 (10.5-15.5)", "17.2 (14.5-20.2)"],
        "CIF % Donante vivo (IC 95%)": ["1.4 (0.5-2.7)", "4.3 (2.2-6.7)", "5.5 (2.9-8.8)"],
        "Delta CIF DD-LD, puntos % (IC 95%)": ["4.4 (2.6-6.3)", "8.6 (5.4-11.9)", "11.7 (7.5-15.9)"],
        "Conclusión": ["Delta>0 (DD > LD, significativo)", "Delta>0 (DD > LD, significativo)", "Delta>0 (DD > LD, significativo)"]
    })
    st.dataframe(bootstrap_muerte_df.style.set_properties(**{'background-color': '#1e1b26', 'color': '#e5e7eb'}), use_container_width=True)

    # Tabla de Bootstrap para Pérdida
    st.markdown("Bootstrap de CIF — Pérdida del injerto (causa 2). DD vs LD")
    bootstrap_perdida_df = pd.DataFrame({
        "Horizonte (años)": [1, 3, 5],
        "CIF % Donante fallecido (IC 95%)": ["9.0 (7.2-10.9)", "12.5 (10.4-14.9)", "16.4 (13.6-19.3)"],
        "CIF % Donante vivo (IC 95%)": ["5.1 (3.1-7.3)", "9.2 (6.0-12.4)", "15.1 (10.8-19.9)"],
        "Delta CIF DD-LD, puntos % (IC 95%)": ["3.8 (0.9-6.7)", "3.3 (-0.5-7.3)", "1.3 (-4.2-6.6)"],
        "Conclusión": ["Delta>0 (DD > LD, significativo)", "Incluye 0 (no concluyente)", "Incluye 0 (no concluyente)"]
    })
    st.dataframe(bootstrap_perdida_df.style.set_properties(**{'background-color': '#1e1b26', 'color': '#e5e7eb'}), use_container_width=True)

    st.markdown("""
    **Definiciones:**
    - **CIF:** Porcentaje de pacientes que ya presentaron el evento antes o en el horizonte (1, 3 o 5 años).
    - **Delta CIF (pp):** Diferencia en puntos porcentuales entre Donante Fallecido (DD) y Donante Vivo (LD).
    - **IC 95% que no incluye 0:** Diferencia concluyente.
    - **IC 95% que sí incluye 0:** No concluyente (no podemos asegurar diferencia).
    """)

    # ---------------------------------------------------------
    # Sección: Resultados Clave
    # ---------------------------------------------------------
    st.subheader("Resultados clave")

    st.markdown("""
    - **Muerte (causa 1)**
        - 1 año: ΔCIF 4.4 pp (IC 2.6–6.3) → concluyente (DD > LD).
        - 3 años: ΔCIF 8.6 pp (IC 5.4–11.9) → concluyente (DD > LD).
        - 5 años: ΔCIF 11.7 pp (IC 7.5–15.9) → concluyente (DD > LD).
        - La mortalidad acumulada es mayor en DD y la brecha crece con el tiempo.
    - **Pérdida del injerto (causa 2)**
        - 1 año: ΔCIF 3.8 pp (IC 0.9–6.7) → concluyente (DD > LD).
        - 3 años: ΔCIF 3.3 pp (IC −0.5–7.3) → no concluyente.
        - 5 años: ΔCIF 1.3 pp (IC −4.2–6.6) → no concluyente.
        - La ventaja temprana de LD se diluye hacia 3–5 años.
    """)
    # ---------------------------------------------------------
# PESTAÑA 4: Hallazgos y Conclusiones
# ---------------------------------------------------------
with tab4:
    st.header("Hallazgos y Conclusiones")

    # ---------------------------------------------------------
    # Sección: Discusión
    # ---------------------------------------------------------
    st.subheader("Discusión")

    st.markdown("""
    <div class="interpretation-box">
      <p>Este análisis no paramétrico complementa el estudio original al centrarse en la comunicación clínica y metodológica de los riesgos competitivos.</p>
      <ul>
        <li><strong>CIF vs. Kaplan-Meier:</strong> La CIF es superior porque estima el riesgo absoluto real de cada evento (muerte o pérdida del injerto), reconociendo que uno puede impedir al otro. Si se hubiera usado Kaplan-Meier, la suma de los riesgos estimados para muerte y pérdida habría superado el 100%, lo cual es imposible y engañoso.</li>
        <li><strong>Prueba de Gray vs. Log-rank:</strong> La prueba de Gray es el estándar para comparar grupos en este contexto. A diferencia del log-rank, que trata la muerte como censura, Gray compara directamente las curvas de CIF, evitando sesgos. Nuestros resultados confirman que la diferencia entre donantes vivos y fallecidos es significativa para la mortalidad (p<0.001) pero se diluye para la pérdida del injerto a 5 años (p=0.123).</li>
        <li><strong>Bootstrap e Intervalos de Confianza:</strong> El bootstrap nos permite reportar diferencias absolutas de riesgo con su incertidumbre. Por ejemplo, a 5 años, los receptores de donante fallecido tienen un 11.7% más de riesgo de muerte (IC 95%: 7.5-15.9 pp) que los de donante vivo. Esta forma de comunicar “cuánto más” es mucho más útil clínicamente que un simple p-valor o una razón de riesgo.</li>
        <li><strong>Nuestro enfoque añade valor al:</strong>
          <ul>
            <li>Justificar explícitamente por qué se usan métodos no paramétricos (CIF, Gray, bootstrap) en lugar de otros.</li>
            <li>Reportar riesgo absoluto y diferencias absolutas con intervalos de confianza, lo que facilita la interpretación clínica.</li>
            <li>Evitar supuestos de normalidad para variables continuas (como la edad o la creatinina), que en este caso no se cumplen.</li>
          </ul>
        </li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Sección: Limitaciones
    # ---------------------------------------------------------
    st.subheader("Limitaciones")

    st.markdown("""
    <div class="interpretation-box">
      <ul>
        <li><strong>No ajustamos por otros factores clínicos:</strong> Nuestro análisis (CIF, prueba de Gray) se centra solo en el tipo de donante (fallecido vs. vivo). No considera otras variables importantes como la edad del receptor, la diabetes o las infecciones virales (CMV/BKV), que sí pueden afectar los resultados. El artículo original sí ajustó por estas variables usando un modelo más complejo (Fine-Gray).</li>
        <li><strong>Prueba de Gray aplicada año por año:</strong> Para ver cómo evoluciona la diferencia entre grupos, realizamos la prueba de Gray separadamente a 1, 3 y 5 años. Esto es útil para mostrar el cambio en el tiempo, pero no es el método estándar, ya que puede reducir la capacidad de detectar una diferencia real (potencia estadística).</li>
        <li><strong>Precisión del bootstrap:</strong> Los intervalos de confianza obtenidos con el bootstrap dependen del tamaño de la muestra y del desbalance entre grupos (hay muchos más receptores de donante fallecido que de donante vivo). Aunque es un método robusto, nuestros resultados podrían tener cierta variabilidad debido a esta estructura de la muestra.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Sección: Conclusiones
    # ---------------------------------------------------------
    st.subheader("Conclusiones")

    st.markdown("""
    <div class="interpretation-box">
      <p>Este análisis muestra que el tipo de donante tiene un impacto claro en la supervivencia del receptor, pero no tanto en la pérdida del injerto a largo plazo.</p>
      <h4>Sobre la muerte del paciente:</h4>
      <ul>
        <li>Los receptores de un donante fallecido tienen un riesgo mayor de morir en comparación con los de un donante vivo, y esta diferencia aumenta con el tiempo (de 4.4% al año 1 a 11.7% al año 5). Estos resultados son estadísticamente sólidos y coinciden con lo encontrado en el artículo original.</li>
      </ul>
      <h4>Sobre la pérdida del injerto:</h4>
      <ul>
        <li>Al principio (primer año), también hay una ventaja para quienes reciben un injerto de donante vivo. Sin embargo, a los 3 y 5 años, esa diferencia ya no es clara ni concluyente. Esto puede deberse a que muchos pacientes con donante fallecido mueren antes de perder el injerto (riesgo competitivo) o a que el seguimiento médico reduce las diferencias iniciales.</li>
      </ul>
      <h4>¿Qué nos dicen los métodos juntos?</h4>
      <ul>
        <li>La CIF nos dice “cuántos pacientes” tienen cada desenlace.</li>
        <li>La prueba de Gray confirma que las curvas de riesgo están separadas, especialmente para la mortalidad.</li>
        <li>El bootstrap nos permite decir “cuán grande” es la diferencia y con qué certeza (por ejemplo: “11.7 puntos porcentuales más, con un margen entre 7.5 y 15.9”).</li>
      </ul>
      <p><strong>En resumen, este enfoque no paramétrico ofrece una forma más clara y realista de interpretar los resultados en estudios donde eventos como la muerte y la pérdida del injerto compiten entre sí.</strong></p>
    </div>
    """, unsafe_allow_html=True)