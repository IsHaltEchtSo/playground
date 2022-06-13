from controller.MainController import controller

# exit gaming controller if state == 2
while controller.is_running:

    # select a game to play
    controller.set_state_by_user()

    # play the game
    if controller.selected_game:
        controller.selected_game.run()
        controller.clear_selected_game()