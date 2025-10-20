import os
import json
import re

def convert_tables(entries):
    """
    Cerca tabelle in formato Markdown all’interno di entries
    e le converte in formato strutturato 5eTools.
    """
    new_entries = []
    i = 0
    while i < len(entries):
        line = entries[i]
        # Riconosce una riga di intestazione di tabella come: | d6 | Trait |
        if isinstance(line, str) and re.match(r'^\|\s*d?\d*\s*\|', line.strip()):
            # raccoglie le righe della tabella
            table_lines = []
            while i < len(entries) and isinstance(entries[i], str) and entries[i].strip().startswith("|"):
                table_lines.append(entries[i])
                i += 1

            # converte la tabella markdown in struttura JSON 5eTools
            headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
            rows = []
            for row_line in table_lines[2:]:
                cols = [c.strip() for c in row_line.split("|")[1:-1]]
                if len(cols) == len(headers):
                    rows.append(cols)

            new_entries.append({
                "type": "table",
                "colLabels": headers,
                "rows": rows
            })
        else:
            new_entries.append(line)
            i += 1
    return new_entries


def process_object(obj):
    """
    Scansiona ricorsivamente ogni dizionario o lista JSON,
    e converte i campi "entries" ovunque si trovino.
    """
    if isinstance(obj, dict):
        if "entries" in obj and isinstance(obj["entries"], list):
            obj["entries"] = convert_tables(obj["entries"])
        for v in obj.values():
            process_object(v)
    elif isinstance(obj, list):
        for v in obj:
            process_object(v)


# === MAIN ===
folder = os.path.dirname(os.path.abspath(__file__))
print(f"📂 Scansione cartella: {folder}\n")

for fname in os.listdir(folder):
    if fname.endswith(".json"):
        path = os.path.join(folder, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"🔍 Analizzo {fname}...")

            process_object(data)

            out_path = path.replace(".json", "_converted.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅  Creato {os.path.basename(out_path)}\n")

        except Exception as e:
            print(f"⚠️  Errore nel leggere {fname}: {e}\n")

print("🏁 Conversione completata per tutti i file JSON nella cartella!")
