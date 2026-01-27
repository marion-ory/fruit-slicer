import json


def load_language(selected_language):
    way_files = f"data/locales/{selected_language}.json"
    try:

        with open(way_files, "r", encoding="utf - 8") as files:
            traduction = json.load(files)
        return traduction
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Erreur avec le fichier{selected_language}.json")
        return {}


traduction = load_language("fr")
print(traduction)
