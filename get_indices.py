import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_XCRs9-Weqq7leUj1mqmvuXTghMlVB6D1AOs6RJ17MNI")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def get_indices():
    print("🚀 Rilevazione indici su Railway...")
    
    # 1. Pulisci sessioni precedenti
    run("browser-use close --all")
    time.sleep(2)
    
    # 2. Connetti al cloud
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    time.sleep(2)
    
    # 3. Apri la pagina
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # 4. ATTESA CHE REACT RENDERIZZI (CRITICO!)
    print("⏳ Attesa che React renderizzi il form...")
    time.sleep(10)  # Attesa maggiore per React
    
    # 5. Prima di tutto, ottieni lo stato COMPLETO
    print("📋 Stato COMPLETO della pagina:")
    result = run("browser-use state", capture=True)
    print(result.stdout[:2000])  # Prime 2000 righe
    
    # 6. Cerca il form direttamente (forse non serve cliccare Sign In)
    # Il form potrebbe essere già visibile
    lines = result.stdout.split('\n')
    
    username_idx = None
    password_idx = None
    enter_idx = None
    
    print("\n🔍 Cerca campi specifici...")
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Cerca campo username
        if ('username' in line_lower or 'email' in line_lower) and 'input' in line_lower:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                username_idx = int(match.group(1))
                print(f"✅ Username index: {username_idx} - {line.strip()[:100]}")
        
        # Cerca campo password
        if 'password' in line_lower and 'input' in line_lower:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                password_idx = int(match.group(1))
                print(f"✅ Password index: {password_idx} - {line.strip()[:100]}")
        
        # Cerca bottone login (btn_green)
        if ('btn_green' in line_lower or 'enter' in line_lower) and 'button' in line_lower:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                enter_idx = int(match.group(1))
                print(f"✅ Enter button index: {enter_idx} - {line.strip()[:100]}")
    
    # 7. SE NON TROVATI, prova a catturare TUTTI gli elementi interattivi
    if username_idx is None or password_idx is None:
        print("\n⚠️ Campi non trovati. Cerco in tutti gli elementi...")
        
        # Usa browser-use eval per esplorare il DOM direttamente
        print("🔍 Esplorazione DOM con eval...")
        
        # Trova tutti gli input
        eval_inputs = run("browser-use eval 'document.querySelectorAll(\"input\").length'", capture=True)
        print(f"📊 Numero di input trovati: {eval_inputs.stdout}")
        
        # Trova il bottone
        eval_buttons = run("browser-use eval 'document.querySelectorAll(\"button\").length'", capture=True)
        print(f"📊 Numero di button trovati: {eval_buttons.stdout}")
        
        # Prova a ottenere gli attributi dei primi input
        eval_details = run("browser-use eval 'Array.from(document.querySelectorAll(\"input\")).map(i => i.name || i.id || i.placeholder || i.type).join(\", \")'", capture=True)
        print(f"📋 Input details: {eval_details.stdout[:500]}")
    
    return username_idx, password_idx, enter_idx

if __name__ == "__main__":
    username_idx, password_idx, enter_idx = get_indices()
    print(f"\n📊 INDICI TROVATI: username={username_idx}, password={password_idx}, enter={enter_idx}")
    
    # Salva gli indici su file per debug
    with open("indices.txt", "w") as f:
        f.write(f"username={username_idx}\npassword={password_idx}\nenter={enter_idx}")
