from math import floor

class Goal():
    def __init__(self, subject, exercises) -> None:
        self.subject = subject
        self.exercises = exercises
        self.exercises_per_day = 0


class GoalTracker():
    def __init__(self, deadline_in_days: int) -> None:
        self.goal: Goal = None
        self.current_day: int = None
        self.terminal_day: int = None
        self.deadline: int = deadline_in_days

    def register_goal(self, goal: Goal) -> None:
        self.goal = goal

    def set_progress_time(self, puffer_value: float) -> None:
        self.terminal_day = floor( puffer_value * self.deadline )
        self.goal.exercises_per_day = self.goal.exercises / self.terminal_day

    def set_current_day(self, day: int) -> None:
        self.current_day = day

    def show_scheduled_progress(self) -> None:
        print(f"You are trying to learn {self.goal.subject}.\n")
        print(f"You are at day {self.current_day} / {self.deadline}.\n")
        print(f"{self.goal.exercises_per_day * self.current_day} / {self.goal.exercises} exercises should have been done by now!")


def get_goal() -> Goal:
    # ask user for a new goal
    subject = input("What subject are you learning for?")
    exercises = int(input("How many exercises to do?"))

    return Goal(subject, exercises)

