import pathlib

import yaml


class Storage:
    def __init__(self, storage_path: pathlib.Path):
        self.data = {
            "passwords": [
                {
                    "username": "president_skroob",
                    "purpose": "luggage",
                    "password": "12345",
                },
                {"username": "admin", "purpose": "admin", "password": "admin"},
                {"username": "AzureDiamond", "purpose": "IRC", "password": "hunter2"},
            ]
        }

        self.storage_path = storage_path

        if self.storage_path.exists():
            with open(storage_path) as storage_file:
                self.data = yaml.load(storage_file, Loader=yaml.Loader)
        else:
            self.save()

    def save(self):
        with open(self.storage_path, "w") as storage_file:
            yaml.dump(self.data, storage_file)
