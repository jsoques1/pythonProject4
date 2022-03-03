#
from ChessViews import ChessMainViews
from ChessControllers import ChessMainControllers





# from ChessViews import ChessPlayersView

def main():
    chess_main_view = ChessMainViews.ChessMainView()
    chess_main_controller = ChessControllers.ChessMainController(chess_main_view)

    chess_main_controller.run()
    #chess_main_view.display_interface()


if __name__ == "__main__":
    main()
