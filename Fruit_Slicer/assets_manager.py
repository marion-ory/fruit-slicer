import _json


def load_language(selected_language):
    way_files = f"data/locales/{selected_language}.json"
    with open(way_files, "r", encoding=utf - 8) as files:
        traduction = json.load(files)
    return traduction


traduction = load_language("fr")
print(traduction)
