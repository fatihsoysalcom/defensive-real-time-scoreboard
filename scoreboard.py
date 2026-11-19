import time
import threading

class RealTimeScoreboard:
    def __init__(self):
        # Initialize scores defensively: use a dictionary and ensure keys exist
        self._scores = {"TeamA": 0, "TeamB": 0}
        self._lock = threading.Lock() # Protect shared data from race conditions
        self._last_update_time = time.time()
        self._update_interval = 5 # Seconds between automatic checks

    def update_score(self, team_name, points):
        # Defensive input validation: ensure points is a non-negative integer
        if not isinstance(points, int) or points < 0:
            print(f"[DEFENSIVE] Invalid points value for {team_name}: {points}. Ignoring.")
            return

        with self._lock:
            # Defensive check: ensure team_name exists before updating
            if team_name not in self._scores:
                print(f"[DEFENSIVE] Unknown team '{team_name}'. Cannot update score.")
                return
            self._scores[team_name] += points
            print(f"Score updated: {team_name} +{points}. Current: {self._scores}")
            self._last_update_time = time.time() # Reset last update time on valid change

    def get_scores(self):
        with self._lock:
            # Return a copy to prevent external modification of internal state
            return self._scores.copy()

    def display_scores(self):
        current_scores = self.get_scores()
        print(f"\n--- Real-Time Scoreboard ---")
        for team, score in current_scores.items():
            print(f"{team}: {score}")
        print(f"---------------------------")

    def _monitor_activity(self):
        # Defensive check for inactivity: if no updates for a while, log it
        while True:
            time.sleep(self._update_interval)
            with self._lock:
                if time.time() - self._last_update_time > self._update_interval * 2: # Arbitrary inactivity threshold
                    print("[DEFENSIVE] Scoreboard has been inactive for a significant period.")
                    # In a real system, you might trigger alerts or logging here

    def start_monitoring(self):
        # Start a background thread for inactivity monitoring
        monitor_thread = threading.Thread(target=self._monitor_activity, daemon=True)
        monitor_thread.start()

# --- Example Usage ---
if __name__ == "__main__":
    scoreboard = RealTimeScoreboard()
    scoreboard.start_monitoring()

    print("Simulating score updates...")

    # Valid updates
    scoreboard.update_score("TeamA", 10)
    time.sleep(1)
    scoreboard.update_score("TeamB", 5)
    time.sleep(1)
    scoreboard.update_score("TeamA", 7)

    # Invalid inputs (demonstrating defensive checks)
    print("\nAttempting invalid updates:")
    scoreboard.update_score("TeamC", 10) # Unknown team
    scoreboard.update_score("TeamA", -5) # Negative points
    scoreboard.update_score("TeamB", "twenty") # Non-integer points

    time.sleep(2)
    scoreboard.display_scores()

    # Simulate a period of inactivity
    print("\nSimulating inactivity...")
    time.sleep(10) # Wait longer than the monitor interval

    scoreboard.display_scores() # Display again to show state after inactivity
