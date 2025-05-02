# tracking/entry_exit_tracker.py

import datetime

class EntryExitTracker:
    def __init__(self):
        self.entry_times = {}
        self.exit_times = {}

    def register_entry(self, plate_number):
        if plate_number not in self.entry_times:
            self.entry_times[plate_number] = datetime.datetime.now()
            print(f"[ENTRY] {plate_number} at {self.entry_times[plate_number].strftime('%H:%M:%S')}")

    def register_exit(self, plate_number):
        if plate_number in self.entry_times and plate_number not in self.exit_times:
            self.exit_times[plate_number] = datetime.datetime.now()
            print(f"[EXIT] {plate_number} at {self.exit_times[plate_number].strftime('%H:%M:%S')}")
            return True
        return False

    def get_entry_exit_times(self, plate_number):
        return self.entry_times.get(plate_number), self.exit_times.get(plate_number)
