# ⚡ ProyectaGAS Dashboard - TPLGas

Dashboard web para predicción de demanda y precios de gas natural en Colombia.

🌐 **Demo en vivo:** [Ver Dashboard](https://tu-usuario-proyectagas.streamlit.app)

---

## 🚀 DESPLIEGUE RÁPIDO EN WEB (10 MINUTOS)

### ✅ Paso 1: Preparar Archivos

Asegúrate de tener esta estructura:

```
proyectagas-dashboard/
├── app.py                              ← Aplicación principal
├── requirements.txt                    ← Dependencias
├── .streamlit/
│   └── config.toml                    ← Configuración de tema
├── .gitignore                         ← Archivos a ignorar
├── README.md                          ← Este archivo
│
├── predicciones_futuras_2026.xlsx     ← Datos de precios
├── predicciones_2026_ensemble.xlsx    ← Datos de demanda
├── df_completo_procesado.csv          ← Histórico de precios
└── train.csv                          ← Histórico de demanda
```

### ✅ Paso 2: Crear Repositorio en GitHub

1. **Ve a GitHub:** https://github.com
2. **Click en "New repository"**
3. **Configuración:**
   - Repository name: `proyectagas-dashboard`
   - Description: `Dashboard de predicción de demanda y precios de gas natural`
   - Public (para usar Streamlit Cloud gratis)
4. **NO marcar** "Initialize with README" (ya lo tienes)
5. **Click "Create repository"**

### ✅ Paso 3: Subir Código a GitHub

Abre la terminal en la carpeta del proyecto y ejecuta:

```bash
# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Dashboard ProyectaGAS - Primera versión"

# Conectar con GitHub (reemplaza TU_USUARIO y NOMBRE_REPO)
git remote add origin https://github.com/TU_USUARIO/proyectagas-dashboard.git

# Subir código
git branch -M main
git push -u origin main
```

**Alternativa sin terminal:**
1. Ve a tu repositorio en GitHub
2. Click "uploading an existing file"
3. Arrastra todos los archivos
4. Click "Commit changes"

### ✅ Paso 4: Desplegar en Streamlit Cloud

1. **Ve a:** https://share.streamlit.io
2. **Sign in con GitHub**
3. **Click "New app"**
4. **Configuración:**
   - Repository: `tu-usuario/proyectagas-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click "Deploy!"**

**⏳ Espera 2-3 minutos mientras se despliega...**

### ✅ Paso 5: ¡Listo! 🎉

Tu dashboard estará disponible en:
```
https://tu-usuario-proyectagas-dashboard.streamlit.app
```

Comparte esta URL con tu equipo.

---

## 📦 ARCHIVOS INCLUIDOS

### Código Principal
- **`app.py`** - Aplicación principal del dashboard
- **`requirements.txt`** - Dependencias de Python

### Configuración
- **`.streamlit/config.toml`** - Tema y colores
- **`.gitignore`** - Archivos a ignorar en Git

### Datos
- **`predicciones_futuras_2026.xlsx`** - Predicciones de precios (Henry Hub, TTF)
- **`predicciones_2026_ensemble.xlsx`** - Predicciones de demanda desagregada
- **`df_completo_procesado.csv`** - Histórico de precios
- **`train.csv`** - Histórico de demanda

---

## ✨ CARACTERÍSTICAS

### ✅ Comparación con Datos Reales
- Muestra últimos 6 meses de datos históricos
- Predicciones para todo 2026
- Línea vertical que separa histórico de predicción

### ✅ Unidades Visibles
- Ejes Y con unidades: **USD/MMBtu** y **MBTUD**
- Tooltips informativos

### ✅ Rangos Optimizados
- Márgenes de ±10% para ver fluctuaciones
- Grid visible para mejor lectura

### ✅ 3 Tabs Principales
1. **💵 Precios** - Henry Hub y TTF
2. **📊 Demanda Total** - Nacional con análisis de tendencia
3. **🏭 Sectores** - 10 sectores de consumo

---

## 🔄 ACTUALIZAR EL DASHBOARD

### Actualizar Datos

1. **Reemplaza los archivos Excel/CSV** con nuevas predicciones
2. **Sube los cambios:**

```bash
git add .
git commit -m "Actualizar predicciones"
git push
```

3. **Streamlit Cloud actualizará automáticamente** en 1-2 minutos

### Cambiar Código

1. **Edita `app.py`**
2. **Sube los cambios:**

```bash
git add app.py
git commit -m "Mejoras en dashboard"
git push
```

3. **Streamlit Cloud se actualizará automáticamente**

---

## 🎨 PERSONALIZACIÓN

### Cambiar Colores

Edita `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1E88E5"      # ← Tu color principal
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#1a1a1a"
```

### Agregar Logo

En `app.py`, agrega en el sidebar:

```python
st.sidebar.image("tu_logo.png", use_column_width=True)
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "App failed to deploy"

**Causa:** Archivo faltante o error en requirements.txt

**Solución:**
1. Ve a los logs en Streamlit Cloud
2. Verifica que todos los archivos estén en GitHub
3. Revisa que `requirements.txt` esté correcto

### ❌ Error: "No such file or directory"

**Causa:** Archivos de datos no están en GitHub

**Solución:**
```bash
# Asegúrate de subir los archivos .xlsx y .csv
git add *.xlsx *.csv
git commit -m "Agregar datos"
git push
```

### ❌ Dashboard carga lento

**Causa:** Archivos muy grandes

**Solución:**
- Reduce el tamaño de los CSV (solo últimos 2 años de histórico)
- Usa compresión: `df.to_csv('archivo.csv.gz', compression='gzip')`

### ❌ Gráficos vacíos

**Causa:** Nombres de columnas incorrectos

**Solución:**
Verifica que tus archivos tengan estas columnas:
- Precios: `HenryHub_USD_MMBtu`, `TTF_USD_MMBtu`
- Demanda: `Demanda_Total_MBTUD`

---

## 💡 TIPS AVANZADOS

### Usar un Dominio Personalizado

1. **Actualiza tu plan** en Streamlit Cloud (opcional)
2. **Configura DNS** apuntando a Streamlit
3. **Tu URL:** `dashboard.tplgas.com`

### Proteger con Contraseña

Agrega al inicio de `app.py`:

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "tplgas2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        st.error("❌ Contraseña incorrecta")
        return False
    else:
        return True

if not check_password():
    st.stop()
```

### Agregar Google Analytics

1. Crea cuenta en Google Analytics
2. Agrega tracking code en `app.py`

---

## 📊 COMPARACIÓN: Local vs Web

| Característica | Local (Notebook) | Web (GitHub + Streamlit) |
|----------------|------------------|--------------------------|
| **Acceso** | Solo tu PC | Desde cualquier lugar |
| **Compartir** | Difícil | ✅ Solo envía URL |
| **Actualizar** | Manual | ✅ Automático con `git push` |
| **Costo** | Gratis | ✅ Gratis (Streamlit Cloud) |
| **Requiere Python** | Sí | ❌ No (solo navegador) |
| **Siempre disponible** | No | ✅ 24/7 |

---

## 📞 RECURSOS

### Documentación
- **Streamlit:** https://docs.streamlit.io
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **GitHub:** https://docs.github.com

### Soporte
- **Streamlit Community:** https://discuss.streamlit.io
- **GitHub Issues:** En tu repositorio

---

## 📝 CHECKLIST DE DESPLIEGUE

- [ ] Crear repositorio en GitHub
- [ ] Subir código con `git push`
- [ ] Verificar que archivos .xlsx y .csv están en GitHub
- [ ] Conectar GitHub con Streamlit Cloud
- [ ] Desplegar app
- [ ] Verificar que funciona la URL pública
- [ ] Compartir URL con equipo
- [ ] Probar actualización de datos

---

## 🎯 PRÓXIMOS PASOS

1. **Prueba local primero:**
   ```bash
   streamlit run app.py
   ```

2. **Sube a GitHub** (pasos arriba)

3. **Despliega en Streamlit Cloud** (pasos arriba)

4. **Comparte con tu equipo:**
   ```
   https://tu-usuario-proyectagas.streamlit.app
   ```

---

## ✅ VENTAJAS DE ESTE SETUP

✅ **Gratis** - Streamlit Cloud es gratuito  
✅ **Rápido** - Despliegue en 10 minutos  
✅ **Automático** - Actualiza con `git push`  
✅ **Profesional** - URL pública compartible  
✅ **Seguro** - Código en GitHub  
✅ **Escalable** - Soporta múltiples usuarios  

---

**¡Dashboard listo para el mundo! 🚀**

**TPLGas - Sistema ProyectaGAS**  
**Febrero 2026**

---

## 📄 LICENCIA

© 2026 TPLGas - Todos los derechos reservados
