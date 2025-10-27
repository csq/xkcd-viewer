from ttkthemes import ThemedTk
from .gui.main_window import MainWindow
from .utils.preferences import Preferences

def main():
    root = ThemedTk(theme="yaru") if Preferences()._exists_preferences_file() == False else ThemedTk(theme=Preferences().get_preferences()["theme"])
    app = MainWindow(root)

    root.bind("<Control-q>", lambda event: root.destroy())
    root.bind("<Control-f>", lambda event: app.first_comic())
    root.bind("<Control-n>", lambda event: app.next_comic())
    root.bind("<Control-r>", lambda event: app.random_comic())
    root.bind("<Control-p>", lambda event: app.previous_comic())
    root.bind("<Control-l>", lambda event: app.last_comic())
    root.bind("<Control-t>", lambda event: app.change_theme(root))
    root.bind("<Control-i>", lambda event: app.info_comic(comic=app.get_current_comic()))
    root.bind("<Control-s>", lambda event: app.save_image(comic=app.get_current_comic()))
    root.bind("<Control-g>", lambda event: app.open_search())
    root.bind("<F1>", lambda event: app.open_help())
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

    root.mainloop()

if __name__ == "__main__":
    main()
