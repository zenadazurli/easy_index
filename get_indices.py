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
    
    run("browser-use close --all")
    time.sleep(2)
    
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    
    # Clicca su "Sign In" per aprire il modale (usa il testo)
    print("🔓 Apro il modale Sign In...")
    run('browser-use click "Sign In"')
    time.sleep(2)
    
    # Ottieni lo stato
    print("📋 Stato della pagina:")
    result = run("browser-use state", capture=True)
    print(result.stdout)
    
    # Cerca gli indici
    username_idx = None
    password_idx = None
    enter_idx = None
    
    lines = result.stdout.split('\n')
    for i, line in enumerate(lines):
        if 'username' in line and 'input' in line:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                username_idx = int(match.group(1))
                print(f"✅ Username index: {username_idx}")
        if 'password' in line and 'input' in line:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                password_idx = int(match.group(1))
                print(f"✅ Password index: {password_idx}")
        if 'button' in line and ('Enter' in line or 'btn_green' in line):
            match = re.search(r'\[(\d+)\]', line)
            if match:
                enter_idx = int(match.group(1))
                print(f"✅ Enter button index: {enter_idx}")
    
    return username_idx, password_idx, enter_idx

if __name__ == "__main__":
    username_idx, password_idx, enter_idx = get_indices()
    print(f"\n📊 INDICI TROVATI: username={username_idx}, password={password_idx}, enter={enter_idx}")
