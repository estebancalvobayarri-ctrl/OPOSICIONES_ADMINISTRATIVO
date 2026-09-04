# 🔍 Oposiciones Administrativo - Valencia

Monitor automático de oposiciones de **Administrativo** y **Auxiliar Administrativo** publicado en:

- 📘 **DOGV** (Diari Oficial de la Generalitat Valenciana)
- 📗 **Boletí¬¡n Oficial de la Diputacií¿½ de Valè¿½ncia**

## 🌐 Web pública

La web está disponible en: **https://estebancalvobayarri-ctrl.github.io/OPOSICIONES_ADMINISTRATIVO/**

## ⚙️ Cómo funciona

1. **GitHub Actions** ejecuta diariamente (a las 10:00 hora Espaí¿½a) el script `scripts/check-oposiciones.py`
2. El script busca nuevas convocatorias relacionadas con administrativo/auxiliar
3. Se genera/actualiza el archivo `data/oposiciones.json` con los resultados
4. La web (`index.html`) lee ese JSON y muestra las novedades

## 📁 Estructura del repositorio

```
OPOSICIONES_ADMINISTRATIVO/
├── index.html              # Pí¿¡gina web principal
├── styles.css              # Estilos CSS
├── script.js               # Lí¿½gica del frontend
├── data/
│   └── oposiciones.json    # Datos actualizados diariamente
├── scripts/
│   └── check-oposiciones.py # Script de bíº¿squeda (Python)
└── .github/
    └── workflows/
        └── daily-check.yml  # GitHub Action diario
```

## 🚀 Prí¿¡ximos pasos

Para activar la web:

1. Ve a **Settings > Pages** en GitHub
2. En **Source**, selecciona `Deploy from a branch`
3. Elige la rama `main` y la carpeta `/ (root)`
4. Haz clic en **Save**

La web estarí¿½ disponible en unos minutos en la URL indicada arriba.

## 📝 Notas

- Los datos se actualizan automí¿½ticamente cada díƒa
- Si no hay novedades, la web mostrarí¿½ un mensaje indicí¿½ndolo
- Puedes forzar una actualizacií¿½n manual ejecutando el workflow `Check Oposiciones Daily` desde la pestaí¿½a **Actions**

---

Hecho con ❤️ para oposicionistas de Valencia
