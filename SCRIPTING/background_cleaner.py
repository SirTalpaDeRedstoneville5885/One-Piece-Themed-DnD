import json
import os
import re

# === CONFIGURAZIONE ===
INPUT_FILE = "background.json"
OUTPUT_FILE = "background_linked.json"

# Oggetti e strumenti presenti nel PHB (nomi chiave → source)
PHB_ITEMS = {
   "ink pen" : { "item": "ink pen", "source" : "phb"},
   "bottle of ink" : { "item": "bottle of ink", "source" : "phb"},
   "traveler's clothes" : { "item": "traveler's clothes", "source" : "phb"},
   "cook's utensils" : { "item": "cook's utensils", "source" : "phb"},
  "cartographer's tools"  : { "item": "cartographer's tools", "source" : "phb"},
   "navigator's tools" : { "item": "navigator's tools", "source" : "phb"},
   "herbalism kit" : { "item": "herbalism kit", "source" : "phb"},
   "brewer's supplies" : { "item": "brewer's supplies", "source" : "phb"},
   "alchemist's supplies" : { "item": "alchemist's supplies", "source" : "phb"},
   "carpenter's tools" : { "item": "carpenter's tools", "source" : "phb"},
   "woodcarver's tools" : { "item": "woodcarver's tools", "source" : "phb"},
  "healer's kit"  : { "item": "healer's kit", "source" : "phb"},
   "crowbar" : { "item": "crowbar", "source" : "phb"},
   "shovel" : { "item": "shovel", "source" : "phb"},
   "tent" : { "item": "tent", "source" : "phb"},
   "backpack" : { "item": "backpack", "source" : "phb"},
   "bedroll" : { "item": "bedroll", "source" : "phb"},
   "rope" : { "item": "rope", "source" : "phb"}
}

# 🧾 converte tabelle markdown in formato 5etools
def parse_markdown_table(lines):
    rows = []
    headers = []
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*[-]+", line):
            continue
        parts = [c.strip() for c in line.strip("|").split("|")]
        if not headers:
            headers = parts
        else:
            rows.append(parts)
    return {"type": "table", "colLabels": headers, "rows": rows}


def convert_tables(entries):
    new_entries = []
    buffer = []
    in_table = False
    for entry in entries:
        if isinstance(entry, str) and "|" in entry:
            in_table = True
            buffer.append(entry)
        else:
            if in_table:
                new_entries.append(parse_markdown_table(buffer))
                buffer = []
                in_table = False
            new_entries.append(entry)
    if buffer:
        new_entries.append(parse_markdown_table(buffer))
    return new_entries


# 🪄 collega oggetti conosciuti del PHB
def link_phb_items(starting_equipment):
    for group in starting_equipment:
        if "_" in group:
            for i, item in enumerate(group["_"]):
                if "special" in item:
                    key = item["special"].lower()
                    for known_item, ref in PHB_ITEMS.items():
                        if known_item in key:
                            group["_"][i] = ref
    return starting_equipment


# 🔧 sistema un file singolo
def process_backgrounds_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    backgrounds = data.get("background", [])
    if not backgrounds:
        print(f"ℹ️  Nessun background trovato in {os.path.basename(filepath)}")
        return

    for bg in backgrounds:
        if "entries" in bg:
            bg["entries"] = convert_tables(bg["entries"])
        if "startingEquipment" in bg:
            bg["startingEquipment"] = link_phb_items(bg["startingEquipment"])
        if "toolProficiencies" not in bg:
            bg["toolProficiencies"] = []
        if "skillProficiencies" not in bg:
            bg["skillProficiencies"] = []
        if "startingEquipmentAlt" not in bg:
            bg["startingEquipmentAlt"] = []

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Sistemato: {os.path.basename(filepath)}")


# 🚀 esegui su tutti i file JSON nella cartella
def main():
    folder = os.getcwd()
    print(f"📂 Scansione cartella: {folder}")

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            try:
                process_backgrounds_file(os.path.join(folder, filename))
            except Exception as e:
                print(f"⚠️ Errore con {filename}: {e}")

    print("\n🏁 Tutti i file JSON sono stati sistemati!")


if __name__ == "__main__":
    main()
