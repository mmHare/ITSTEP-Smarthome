from tinydb import TinyDB, Query
from pathlib import Path
from datetime import datetime
import threading


class StatsDBManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path=None):
        with cls._lock:  # lock in case multiple threads try to access singleton
            if cls._instance is None:  # Ensure only one instance exists
                cls._instance = super().__new__(cls)
                cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path=None):
        if hasattr(self, "db"):  # if already has self.db assigned
            return
        if db_path is None:
            BASE_DIR = Path(__file__).resolve(
            ).parent.parent  # main folder path
            db_path = BASE_DIR / "data" / "stats_db.json"
        self.db = TinyDB(db_path)

    def add_stat(self, device_id, metric, value):
        self.db.insert({
            "device_id": device_id,
            "metric": metric,
            "value": value,
            "timestamp": datetime.now().isoformat(),
        })

    def get_stats_for_device(self, device_id):
        return self.db.search(Query().device_id == device_id)

    def clear_stats(self):
        self.db.truncate()


# from stats.db_manager import StatsDBManager

# stats_db = StatsDBManager()
