class VersionTracker:
    def __init__(self):
        self._version = None

    def set_version(self, version: str):
        self._version = version

    def get_version(self) -> str:
        return self._version

    def has_changed(self, new_version: str) -> bool:
        return self._version != new_version