import json
import os
import time

def update_dates(obj, now):
    """Aggiorna i campi dateAdded e dateLastModified in modo ricorsivo."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "dateAdded":
                obj[k] = now
            elif k == "dateLastModified":
                obj[k] = now
            else:
                update_dates(v, now)
    elif isinstance(obj, list):
        for item in obj:
            update_dates(item, now)

def main():
    folder = os.getcwd()
    print(f"📂 Cartella corrente: {folder}\n")

    # Trova tutti i file .json nella cartella
    json_files = [f for f in os.listdir(folder) if f.endswith(".json")]
    if not json_files:
        print("❌ Nessun file JSON trovato nella cartella.")
        return

    # Mostra elenco file
    print("📄 File trovati:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")

    # Selezione manuale
    selected_indices = input("\n👉 Inserisci i numeri dei file da unire (es: 1,3,4): ")
    try:
        selected_files = [json_files[int(i.strip()) - 1] for i in selected_indices.split(",")]
    except (ValueError, IndexError):
        print("❌ Selezione non valida.")
        return

    print("\n📑 Ordine di unione:")
    for i, f in enumerate(selected_files, 1):
        print(f"{i}. {f}")

    merged_data = {"_meta": None}
    merged_keys = set()
    now = int(time.time())

    for idx, filename in enumerate(selected_files):
        filepath = os.path.join(folder, filename)
        print(f"\n🔄 Leggendo: {filename}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Usa solo il primo _meta
            if "_meta" in data:
                if merged_data["_meta"] is None:
                    merged_data["_meta"] = data["_meta"]
                    print("✅ _meta mantenuto da questo file.")
                else:
                    print("⚙️  _meta ignorato (già impostato dal primo file).")

            # Aggiorna date
            update_dates(data, now)

            # Unisci i campi principali (feat, background, ecc.)
            for key, value in data.items():
                if key == "_meta":
                    continue
                if isinstance(value, list):
                    if key not in merged_data:
                        merged_data[key] = []
                    merged_data[key].extend(value)
                    merged_keys.add(key)

        except Exception as e:
            print(f"❌ Errore con {filename}: {e}")

    # Chiedi il nome del file di output
    output_name = input("\n💾 Nome file di output (predefinito: merged.json): ").strip()
    if not output_name:
        output_name = "merged.json"

    output_path = os.path.join(folder, output_name)

    # Salvataggio
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print("\n🏁 Unione completata con successo!")
    print(f"📘 File salvato come: {output_path}")
    print(f"🔑 Chiavi unite: {', '.join(merged_keys)}")
    print(f"🕒 Timestamp aggiornato a: {now}")

if __name__ == "__main__":
    main()
