import json
from reactome_service import ReactomeService

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: config.json not found. Please create with your email.")
        exit(1)

def main():
    config = load_config()
    service = ReactomeService(config)

    print("=== Reactome Content Downloader ===")
    print("Options:\n1. Get Reactome version\n2. Download entity/pathway JSON by stable ID")
    choice = input("Enter choice (1 or 2): ").strip()

    def progress(msg):
        print(msg)

    if choice == "1":
        version = service.download_database_version(progress)
        print("Finished. Version:", version)
    elif choice == "2":
        st_id = input("Enter Reactome stable ID (e.g. R‑HSA‑199420): ").strip()
        service.download_pathway_json(st_id, progress)
        print("Finished. Check downloads on your Desktop.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
