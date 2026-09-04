// URL del JSON con los datos de oposiciones
const DATA_URL = 'data/oposiciones.json';

// Elementos del DOM
const lastUpdateEl = document.getElementById('lastUpdate');
const resultsContainer = document.getElementById('resultsContainer');

// Formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('es-ES', options);
}

// Formatear fecha corta
function formatDateShort(dateString) {
    const date = new Date(dateString);
    const options = { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric'
    };
    return date.toLocaleDateString('es-ES', options);
}

// Cargar y mostrar datos
async function loadOposiciones() {
    try {
        const response = await fetch(DATA_URL);
        
        if (!response.ok) {
            throw new Error('No se pudieron cargar los datos');
        }
        
        const data = await response.json();
        
        // Actualizar íƒltima actualizacií¿½n
        lastUpdateEl.textContent = formatDate(data.lastUpdated);
        
        // Mostrar resultados
        displayResults(data.oposiciones);
        
    } catch (error) {
        console.error('Error loading data:', error);
        resultsContainer.innerHTML = `
            <div class="no-results">
                <h3>⚠️ Error al cargar los datos</h3>
                <p>No se pudo conectar con el archivo de datos. Asegíº¿rate de que GitHub Actions se haya ejecutado correctamente.</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #999;">${error.message}</p>
            </div>
        `;
    }
}

// Mostrar resultados en el DOM
function displayResults(oposiciones) {
    if (!oposiciones || oposiciones.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <h3>✅ Sin novedades</h3>
                <p>No se han encontrado oposiciones de administrativo o auxiliar en las íƒltimas 24 horas.</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #999;">Los datos se actualizan automí¿½ticamente cada díƒa.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    oposiciones.forEach(opo => {
        const sourceClass = opo.source.toLowerCase();
        html += `
            <div class="result-card ${sourceClass}">
                <div class="result-header">
                    <div class="result-title">${opo.title}</div>
                    <div class="result-date">${formatDateShort(opo.date)}</div>
                </div>
                <div class="result-meta">
                    <span class="result-source ${sourceClass}">${opo.source}</span>
                    ${opo.category ? `<span class="result-category">${opo.category}</span>` : ''}
                </div>
                ${opo.description ? `<p class="result-description">${opo.description}</p>` : ''}
                ${opo.url ? `<a href="${opo.url}" target="_blank" class="result-link">Ver publicacií¿½n oficial →</a>` : ''}
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Cargar datos al iniciar
loadOposiciones();
