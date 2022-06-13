from goal_tracker_classes import Goal, GoalTracker, get_goal


def main():
    goal: Goal = get_goal()
    
    # init goal tracker with deadline
    goal_tracker = GoalTracker(deadline_in_days=10)

    # configure goal tracker
    goal_tracker.register_goal(goal)
    goal_tracker.set_progress_time(puffer_value=0.8)
    goal_tracker.set_current_day(1)

    # print scheduled values
    goal_tracker.show_scheduled_progress()


main()



















