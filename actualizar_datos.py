import pandas as pd
import requests
import os

def actualizar_y_retrain():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Cargar el dataset existente (13,853 partidos)
    csv_path = os.path.join(base_dir, 'datos_futbol.csv')
    if not os.path.exists(csv_path):
        print("❌ Error: No se encontró datos_futbol.csv")
        return
        
    df_existente = pd.read_csv(csv_path)
    print(f"📖 Dataset existente cargado: {len(df_existente)} partidos.")
    
    # Eliminar cualquier registro previo de mundial_26 por si acaso
    df_existente = df_existente[df_existente['Liga'] != 'mundial_26']
    
    # 2. Descargar resultados del Mundial 2026 en curso
    url_mundial = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'
    print(f"📥 Descargando resultados del Mundial 2026 desde GitHub...")
    
    try:
        r = requests.get(url_mundial, timeout=15)
        r.raise_for_status()
        data = r.json()
        matches = data.get('matches', [])
        
        partidos_m26 = []
        for match in matches:
            score = match.get('score', {})
            if not score:
                continue
            
            # Formato: score = {"ft": [2, 1]}
            if isinstance(score, dict):
                ft = score.get('ft', [])
                if not ft or len(ft) < 2:
                    continue
                hg, ag = int(ft[0]), int(ft[1])
            elif isinstance(score, str) and '-' in score:
                partes = score.replace(' ', '').split('-')
                hg, ag = int(partes[0]), int(partes[1])
            else:
                continue
                
            res = 'H' if hg > ag else ('A' if hg < ag else 'D')
            
            partidos_m26.append({
                'Date': match.get('date', ''),
                'HomeTeam': match.get('team1', ''),
                'AwayTeam': match.get('team2', ''),
                'FTHG': hg, 'FTAG': ag, 'FTR': res,
                'HTHG': 0, 'HTAG': 0, 'HTR': res,
                'HS': 0, 'AS': 0, 'HST': 0, 'AST': 0,
                'HC': 0, 'AC': 0, 'HY': 0, 'AY': 0,
                'HR': 0, 'AR': 0, 'Liga': 'mundial_26'
            })
            
        print(f"✅ Descargados {len(partidos_m26)} partidos jugados del Mundial 2026.")
        
        if partidos_m26:
            df_m26 = pd.DataFrame(partidos_m26)
            
            # Formatear fecha
            df_m26['Date'] = pd.to_datetime(df_m26['Date'], errors='coerce')
            df_existente['Date'] = pd.to_datetime(df_existente['Date'], errors='coerce')
            
            # Unir datasets
            df_final = pd.concat([df_existente, df_m26], ignore_index=True)
            df_final.dropna(subset=['Date', 'FTHG', 'FTAG', 'FTR'], inplace=True)
            df_final = df_final.sort_values('Date').reset_index(drop=True)
            
            # Guardar
            df_final.to_csv(os.path.join(base_dir, 'datos_futbol.csv'), index=False)
            df_final.to_csv(os.path.join(base_dir, 'datos', 'partidos.csv'), index=False)
            
            print(f"🎉 Dataset actualizado: {len(df_final)} partidos totales guardados.")
            
            # 3. Reentrenar el modelo
            print("🏋️ Reentrenando el clasificador modelo_futbol.pkl...")
            import entrenar_pkl
            entrenar_pkl.entrenar_y_guardar_modelo()
            
        else:
            print("⚠ No se encontraron partidos jugados para agregar.")
            
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")

if __name__ == '__main__':
    actualizar_y_retrain()
