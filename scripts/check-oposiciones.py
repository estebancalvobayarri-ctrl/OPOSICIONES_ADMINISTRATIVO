#!/usr/bin/env python3
"""
Script para buscar oposiciones de administrativo/auxiliar en:
- DOGV (Diari Oficial de la Generalitat Valenciana)
- BOP de la Diputació¹¿½ de Valè¿½ncia

Genera un archivo JSON con los resultados.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import re

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  Advertencia: requests y beautifulsoup4 no están disponibles")

# Palabras clave para filtrar
KEYWORDS_ADMIN = [
    "administrativo",
    "auxiliar administrativo",
    "auxiliar de administrativo",
    "administració¹¿½",
    "auxiliar administratiu",
]

KEYWORDS_OPOSICIONES = [
    "oposició¹¿½",
    "oposiciones",
    "convocatí¿½ria",
    "convocatoria",
    "concurs-oposició¹¿½",
    "concurso-oposició¹¿½",
    "proceso selectivo",
    "procí¿½s selectiu",
    "oferta d'ocupació¹¿½ píº¿blica",
    "oferta de empleo píº¿blico",
    "bases",
    "plaí¿½es",
    "plazas",
]

def es_relevante(texto):
    """Comprueba si el texto contiene palabras clave de administrativo y oposiciones"""
    texto_lower = texto.lower()
    
    # Debe tener al menos una keyword de administrativo
    tiene_admin = any(kw in texto_lower for kw in KEYWORDS_ADMIN)
    
    # Y al menos una de oposiciones
    tiene_opo = any(kw in texto_lower for kw in KEYWORDS_OPOSICIONES)
    
    return tiene_admin and tiene_opo

def buscar_en_bop_dival():
    """
    Busca en el BOP de la Diputació¹¿½ de Valè¿½ncia
    URL: https://bop.dival.es/
    """
    resultados = []
    
    if not HAS_REQUESTS:
        print("⚠️  Skipping BOP Dival - sin requests")
        return resultados
    
    try:
        # URL de bíƒsqueda del BOP
        # Usamos la pí ¿gina principal y filtramos por fecha
        url = "https://bop.dival.es/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Buscar anuncios relacionados con administrativo
        # El BOP muestra una tabla con los anuncios
        anuncios = soup.find_all('div', class_=re.compile(r'anuncio|item|row', re.I))
        
        # Si no encontramos con clases, buscar por estructura
        if not anuncios:
            # Buscar todos los elementos que parezcan anuncios
            posibles = soup.find_all(text=re.compile(r'(administrativo|auxiliar|oposició¹¿½|convocatí¿½ria)', re.I))
            
            for texto in posibles[:10]:  # Limitar a 10
                parent = texto.find_parent()
                if parent:
                    anuncios.append(parent)
        
        today = datetime.now().date()
        
        for anuncio in anuncios[:20]:  # Limitar procesamien to
            texto = anuncio.get_text(strip=True)
            
            if es_relevante(texto):
                # Extraer info básica
                titulo = texto[:200]  # Limitar longitud
                
                # Buscar enlace
                enlace_tag = anuncio.find('a')
                enlace = enlace_tag['href'] if enlace_tag and enlace_tag.has_attr('href') else url
                
                if not enlace.startswith('http'):
                    enlace = url + enlace
                
                # Buscar fecha
                fecha_tag = anuncio.find(text=re.compile(r'\d{2}/\d{2}/\d{4}'))
                fecha_str = fecha_tag.strip() if fecha_tag else today.strftime("%d/%m/%Y")
                
                resultados.append({
                    "title": titulo,
                    "date": fecha_str,
                    "url": enlace,
                    "description": texto[:300] if len(texto) > 300 else texto,
                    "category": "BOP Valencia"
                })
        
        print(f"✓ BOP Dival: {len(resultados)} resultados relevantes")
        
    except Exception as e:
        print(f"✗ Error en BOP Dival: {e}")
    
    return resultados

def buscar_en_dogv():
    """
    Busca en el DOGV (Diari Oficial de la Generalitat Valenciana)
    URL: https://dogv.gva.es/
    
    NOTA: El DOGV requiere autenticació¹¿½n para acceso completo.
    Usamos una aproximació¹¿½n con bíƒsqueda de Google site:dogv.gva.es
    """
    resultados = []
    
    if not HAS_REQUESTS:
        print("⚠️  Skipping DOGV - sin requests")
        return resultados
    
    try:
        # El DOGV no tiene API pí ƒblica fí¿¡cil.
        # Usamos Google Custom Search o scraping básico
        # Por ahora, dejamos esta funció¹¿½n lista para implementació¹¿½n futura
        
        print("ℹ DOGV: Requiere implementació¹¿½n con API o scraping avanzado")
        
    except Exception as e:
        print(f"✗ Error en DOGV: {e}")
    
    return resultados

def buscar_oposiciones():
    """
    Funció¹¿½n principal que busca en todas las fuentes.
    """
    todas_oposiciones = []
    
    print("\n🔍 Iniciando bíƒsqueda de oposiciones...\n")
    
    # Buscar en BOP de la Diputació¹¿½
    bop_results = buscar_en_bop_dival()
    for result in bop_results:
        result['source'] = 'Diputació¹¿½ de Valè¿½ncia'
        todas_oposiciones.append(result)
    
    # Buscar en DOGV
    dogv_results = buscar_en_dogv()
    for result in dogv_results:
        result['source'] = 'DOGV'
        todas_oposiciones.append(result)
    
    print(f"\n✅ Total: {len(todas_oposiciones)} oposiciones encontradas\n")
    
    return todas_oposiciones

def main():
    # Crear directorio data si no existe
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Buscar oposiciones
    oposiciones = buscar_oposiciones()
    
    # Preparar datos
    data = {
        'lastUpdated': datetime.now().isoformat(),
        'oposiciones': oposiciones
    }
    
    # Guardar JSON
    output_file = data_dir / 'oposiciones.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Datos guardados en {output_file}")

if __name__ == '__main__':
    main()
