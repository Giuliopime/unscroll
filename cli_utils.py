def prompt_for_goal():
    use_goal = input("Would you like to specify a goal? (y/n): ").strip().lower()
    goal = None

    if use_goal == 'y':
        goal = input("Enter your goal (e.g., events near Verona): ").strip()
        print(f"Goal set to: {goal}")
    else:
        print("No goal specified.")

    return goal