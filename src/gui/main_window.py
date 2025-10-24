import requests
import tkinter as tk

from importlib import resources as importlib_resources
from tkinter import ttk, PhotoImage, Toplevel
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from core.comic_service import ComicService
from io import BytesIO
from utils.circular_list import CircularList
from utils.preferences import Preferences
from utils.cache import Cache
from gui.scrollImage import ScrollableImage
from core.db import DB

class MainWindow:
    __db = DB().init_db()
    __comic_service = ComicService("https://xkcd.com/")
    __preferences = Preferences()
    __cache = Cache()
    __current_comic = None

    def __init__(self, master):
        self.master = master

        # Set the window title and icon
        master.title("XKCD Viewer")
        with importlib_resources.path("src.assets", "xkcd.png") as icon_path:
            master.iconphoto(False, PhotoImage(file=icon_path))

        # Set the window size
        self.screen_width, self.screen_height = map(
            int, self.__preferences.get_preferences()["resolution"].split("x")
        )
        master.geometry(f"{self.screen_width}x{self.screen_height}")

        # Create a master frame
        master_frame = ttk.Frame(master)
        master_frame.pack(fill=tk.BOTH, expand=True)

        # Grid the master frame
        master_frame.columnconfigure(0, weight=1)
        master_frame.rowconfigure(0, weight=1)

        # Create a frame for the image
        self.image_frame = ttk.Frame(master_frame, padding=10)
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        # Create a frame for the control buttons
        control_frame = ttk.Frame(master_frame)
        control_frame.grid(row=1, column=0, sticky="nsew")

        # Load a random comic
        self.__current_comic = self.__comic_service.get_random_comic()

        # Download the image
        image = self.download_image(self.__current_comic)
        self.image = ImageTk.PhotoImage(image)

        # Create the title top
        self.title_top = f"{self.__current_comic.get_title()}"
        self.title_label = ttk.Label(self.image_frame, text=self.title_top, font=("Arial", 15, "bold"), foreground="black", padding=10)
        self.title_label.pack()

        # Create the scrollable image
        image_width = self.image.width()
        image_height = self.image.height()
        screen_width_limit = self.screen_width
        screen_height_limit = self.screen_height - 150

        self.image_window = ScrollableImage(self.image_frame, image=self.image, scrollbarwidth=6, width=image_width, height=image_height)
        if image_height > screen_height_limit and image_width < screen_width_limit:
            self.image_window.h_scroll.config(width=0)
        elif image_width > screen_width_limit and image_height < screen_height_limit:
            self.image_window.v_scroll.config(width=0)
        elif image_height < screen_height_limit and image_width < screen_width_limit:
            self.image_window.h_scroll.config(width=0)
            self.image_window.v_scroll.config(width=0)
        self.image_window.pack(fill=None, expand=True)

        # Create control buttons
        with importlib_resources.path("src.assets.buttons", "first.png") as icon_path:
            self.first_image = PhotoImage(file=icon_path)
        with importlib_resources.path("src.assets.buttons", "previous.png") as icon_path:
            self.previous_image = PhotoImage(file=icon_path)
        with importlib_resources.path("src.assets.buttons", "random.png") as icon_path:
            self.random_image = PhotoImage(file=icon_path)
        with importlib_resources.path("src.assets.buttons", "next.png") as icon_path:
            self.next_image = PhotoImage(file=icon_path)
        with importlib_resources.path("src.assets.buttons", "last.png") as icon_path:
            self.last_image = PhotoImage(file=icon_path)

        self.btn_first = ttk.Button(control_frame, image=self.first_image, text="First", width=10, command=self.first_comic)
        self.btn_previous = ttk.Button(control_frame, image=self.previous_image, text="Previous", width=10, command=self.previous_comic)
        self.btn_random = ttk.Button(control_frame, image=self.random_image, text="Random", width=10, command=self.random_comic)
        self.btn_next = ttk.Button(control_frame, image=self.next_image, text="Next", width=10, command=self.next_comic)
        self.btn_last = ttk.Button(control_frame, image=self.last_image, text="Last", width=10, command=self.last_comic)

        # Arrange the control buttons in a grid
        self.btn_first.pack(side=tk.LEFT, expand=True, padx=10, pady=15)
        self.btn_previous.pack(side=tk.LEFT, expand=True, padx=10, pady=15)
        self.btn_random.pack(side=tk.LEFT, expand=True, padx=10, pady=15)
        self.btn_next.pack(side=tk.LEFT, expand=True, padx=10, pady=15)
        self.btn_last.pack(side=tk.LEFT, expand=True, padx=10, pady=15)

    def set_comic(self, comic):
        self.__current_comic = comic
        self.set_image(self.download_image(comic))
        self.set_title(comic.get_title())

    def first_comic(self):
        comic = self.__comic_service.get_first_comic()
        self.set_comic(comic)

    def previous_comic(self):
        comic = self.__comic_service.get_previous_comic()
        self.set_comic(comic)

    def random_comic(self):
        comic = self.__comic_service.get_random_comic()
        self.set_comic(comic)

    def next_comic(self):
        comic = self.__comic_service.get_next_comic()
        self.set_comic(comic)

    def last_comic(self):
        comic = self.__comic_service.get_last_comic()
        self.set_comic(comic)

    def download_image(self, comic):
        img_url = comic.get_image_url()
        if "/home/" in img_url:
            return Image.open(img_url)
        else:
            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))
            self.__cache.save_to_cache(comic_num=comic.get_num(), image=image)
        return image
    
    def get_image_from_cache(self, comic_num):
        cache = self.__cache.get_from_cache(comic_num=comic_num)
        if cache is None:
            return None
        return cache.image_url

    def set_image(self, image):
        self.image = ImageTk.PhotoImage(image)
        image_width = self.image.width()
        image_height = self.image.height()
        screen_width_limit = self.screen_width
        screen_height_limit = self.screen_height - 150

        if hasattr(self, "image_window"):
            self.image_window.pack_forget()

        self.image_window = ScrollableImage(self.image_frame, image=self.image, scrollbarwidth=6, width=image_width, height=image_height)
        if image_height > screen_height_limit and image_width < screen_width_limit:
            self.image_window.h_scroll.config(width=0)
        elif image_width > screen_width_limit and image_height < screen_height_limit:
            self.image_window.v_scroll.config(width=0)
        elif image_height < screen_height_limit and image_width < screen_width_limit:
            self.image_window.h_scroll.config(width=0)
            self.image_window.v_scroll.config(width=0)
        self.image_window.pack(fill=None, expand=True)

    def set_title(self, title):
        self.title_label.config(text=title)
 
    def change_theme(self, root):
        all_themes = ThemedTk.get_themes(root)

        themes_blacklist = ["black", "equilux"]
        for theme in themes_blacklist:
            all_themes.remove(theme)

        cl = CircularList(all_themes)
        theme = cl.next_item()
        self.__preferences.save_preferences("theme", theme)
        root.set_theme(theme)
    
    def open_help(self):
        help_window = Toplevel(self.master)
        help_window.geometry("240x320")
        help_window.title("Shortcuts")
        help_window.resizable(False, False)

        help_text = """
        Ctrl + F: First comic
        Ctrl + N: Next comic
        Ctrl + R: Random comic
        Ctrl + P: Previous comic
        Ctrl + L: Last comic

        Ctrl + S: Save image
        Ctrl + I: Info comic
        Ctrl + T: Change theme
        Ctrl + G: Search comic

        F1: Open help
        F11: Fullscreen

        Ctrl + Q: Quit
        """
        help_label = ttk.Label(help_window, text=help_text, foreground="black", font=("Arial", 12, "normal"), justify="left")
        help_label.pack(padx=0, pady=0, fill="both", expand=True)
        help_window.bind("<Escape>", lambda event: help_window.destroy())
        help_window.grab_set()
    
    def get_current_comic(self):
        return self.__current_comic

    def info_comic(self, comic):
        import webbrowser 

        info_window = Toplevel(self.master)
        window_width = max(((len(comic.get_title()) + 7) * 10), 200)
        info_window.geometry(f"{window_width}x150")
        info_window.title("Comic info")
        info_window.resizable(False, False)

        info_text = f"""
        ID: {comic.get_num()}
        Title: {comic.get_title()}
        Date: {comic.get_date()}
        """
        info_label = ttk.Label(info_window, text=info_text, foreground="black", font=("Arial", 12, "normal"), justify="left")
        info_label.pack(padx=0, pady=0, fill="both", expand=True)

        explain_url = f"https://www.explainxkcd.com/wiki/index.php/{comic.get_num()}:_{comic.get_title().replace(' ', '_')}"
        button_explain = ttk.Button(info_window, text="Explain comic", command=lambda: webbrowser.open(explain_url))
        button_explain.pack(padx=0, pady=0, fill="both")

        info_window.bind("<Escape>", lambda event: info_window.destroy())
        info_window.grab_set()
    
    def save_image(self, comic):
        import tkinter.filedialog as filedialog
        import os

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            initialdir=os.path.expanduser("~"),
            initialfile=f"{comic.get_title().replace(' ', '_')}.png"
        )

        if save_path:
            image_path = self.get_image_from_cache(comic_num=self.__current_comic.get_num())
            Image.open(image_path).save(save_path)

    def open_search(self):
        popup = Toplevel(self.master)
        popup.geometry("130x50")
        popup.title("Search")
        popup.resizable(False, False)

        search_frame = ttk.Frame(popup)
        search_frame.pack(fill="both", expand=True)

        search_entry = ttk.Entry(search_frame, width=30, justify="center", font=("Arial", 12, "normal"), validate="key", validatecommand=(popup.register(self.validate_search), "%P"))
        search_entry.pack(padx=20, pady=10, fill="both", expand=True)
        search_entry.focus()

        popup.bind('<Return>', lambda event: self.search_comic(search_entry.get(), popup))
        popup.bind('<KP_Enter>', lambda event: self.search_comic(search_entry.get(), popup))
        popup.bind("<Escape>", lambda event: popup.destroy())
        popup.grab_set()

    def validate_search(self, P):
        return str.isdigit(P) or P == ""

    def search_comic(self, comic_num, popup):
        comic = self.__comic_service.get_comic_with_num(comic_num)
        self.__current_comic = comic
        self.set_image(self.download_image(comic))
        self.set_title(comic.get_title())

        popup.destroy()
