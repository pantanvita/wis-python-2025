import requests
from pathlib import Path

class ReactomeService:
    # Updated base URL
    BASE_URL = "https://reactome.org/ContentService"

    def __init__(self, config):
        self.email = config.get("contact_email", "")
        self.desktop = Path.home() / "Desktop"
        self.download_folder = self.desktop / "Reactome_Downloads"
        self.download_folder.mkdir(parents=True, exist_ok=True)

    def get_pathway_folder(self, st_id):
        """Create folder for a given pathway (stable ID)."""
        folder = self.download_folder / st_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def download_pathway_json(self, st_id, progress_callback=None):
        """
        Download Reactome pathway or event as JSON from the ContentService API.
        `st_id` is stable identifier, like "R‑HSA‑199420" or any event ID.
        """
        url = f"{self.BASE_URL}/data/query/{st_id}"
        headers = {"User-Agent": f"ReactomeDownloader/1.0 ({self.email})"}
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            if progress_callback:
                progress_callback(f"Error: {resp.status_code} when downloading {st_id}")
            return None

        data = resp.json()
        folder = self.get_pathway_folder(st_id)
        filepath = folder / f"{st_id}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resp.text)

        if progress_callback:
            progress_callback(f"Saved JSON for {st_id} to {filepath}")
        return filepath

    def download_database_version(self, progress_callback=None):
        """
        Download the current Reactome database version.
        """
        url = f"{self.BASE_URL}/data/database/version"
        headers = {"User-Agent": f"ReactomeDownloader/1.0 ({self.email})"}
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            if progress_callback:
                progress_callback(f"Error retrieving version: {resp.status_code}")
            return None

        version = resp.text.strip()
        if progress_callback:
            progress_callback(f"Reactome version: {version}")
        return version
