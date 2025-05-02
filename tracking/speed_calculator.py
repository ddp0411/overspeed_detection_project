# tracking/speed_calculator.py

from config.settings import DISTANCE_METERS, SPEED_LIMIT

class SpeedCalculator:
    def __init__(self):
        pass

    def calculate_speed(self, entry_time, exit_time):
        time_taken_sec = (exit_time - entry_time).total_seconds()
        if time_taken_sec <= 0:
            return 0, "Invalid"

        speed_kmph = (DISTANCE_METERS / time_taken_sec) * 3.6
        status = "Overspeeding" if speed_kmph > SPEED_LIMIT else "Normal"
        return round(speed_kmph, 2), status
