import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import PIL
from PIL import Image, ImageTk


class ColorPalette:
    def __init__(self):
        # Constants For Program
        self.font = "Futura"
        self.palette_length = 6
        self.image_size = 350
        self.window_color = "#e6be94"
        # Widgets Needed for Program
        self.window = None
        self.current_image_pil = None
        self.current_image_rgba = None
        self.current_image = None
        self.image_path_entry = None
        self.canvas = None 
        self.canvas_image = None 
        self.hex_label_list = []
        self.color_frame_list = []
        # Setup for all widgets in the window
        self.setup_all_widgets()
        self.center_window()

    def center_window(self) -> None:
        """
        Centers the root window using the screen size and window size
        """
        # Screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # Window dimensions
        window_width = 786
        window_height = 631
        # (x,y) starts at top left of window (0, 0)
        # x increases moving right, decreases moving left
        # y increases moving down, decreases moving up
        x = screen_width / 2 - window_width / 2 # position top left corner's x at this x
        y = screen_height / 2 - window_height # position top left corner's y at a smaller y (otherwise window too low)
        self.window.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y)) # Adds x and y offsets to window dims
        self.window.resizable(width=False, height=False) # Prevent window from being resizable

    def setup_all_widgets(self) -> None:
        """
        Sets up all widgets on the window
        """
        self.setup_window()
        self.setup_title()
        self.setup_canvas()
        self.setup_image_browser()
        self.setup_palette()

    def setup_window(self) -> None:
        """
        Sets up the main window
        """
        self.window = tk.Tk()
        self.window.title("Color Palette")
        self.window.config(bg=self.window_color)

    def setup_title(self) -> None:
        """
        Sets up the title for the window
        """
        title_label = tk.Label(text="Color Palette", font=(self.font, 30, "bold"), justify="center",
                                    bg=self.window_color, fg="#654321")
        title_label.grid(row=0, column=0, columnspan=self.palette_length)

    def setup_canvas(self) -> None:
        """
        Sets up the canvas with an initial placeholder image (a blank canvas)
        """
        self.current_image_pil = Image.open("canvas.png").resize((self.image_size, self.image_size))
        self.current_image_rgba = self.current_image_pil.convert("RGBA")
        self.current_image = ImageTk.PhotoImage(self.current_image_pil)
        self.canvas = tk.Canvas(self.window, height=self.image_size, width=self.image_size, borderwidth=0,
                                highlightbackground=self.window_color, bg=self.window_color)
        self.canvas.grid(row=3, column=0, columnspan=self.palette_length)
        self.canvas_image = self.canvas.create_image(self.image_size / 2, self.image_size / 2,
                                                     image=self.current_image)

    def setup_image_browser(self) -> None:
        """
        Sets up the image file browser (consists of a file path display and a button to prompt the browse)
        """
        self.image_path_entry = tk.Entry(self.window, width=50, state="readonly", highlightbackground=self.window_color)
        self.image_path_entry.grid(row=1, column=0, columnspan=self.palette_length)
        image_display_button = tk.Button(text="Browse Image Files", command=self.find_image,
                                              highlightbackground=self.window_color)
        image_display_button.grid(row=2, column=0, columnspan=self.palette_length)

    def setup_palette(self) -> None:
        """
        Sets up the color palette (hex code labels and color palette frames)
        """
        for i in range(self.palette_length):
            hex_label = tk.Entry(self.window, font=(self.font, 10), width=13, bd=3, relief="sunken",
                                 highlightbackground=self.window_color, justify="center")
            hex_label.grid(row=4, column=i)
            hex_label.config(state="readonly", readonlybackground=self.window_color)
            self.hex_label_list.append(hex_label)
            color_frame = tk.Frame(self.window, bg=self.window_color, width=128, height=128, bd=3,
                                   relief="sunken", highlightbackground=self.window_color)
            color_frame.grid(row=5, column=i)
            self.color_frame_list.append(color_frame)

    def get_pixel_color(self, event, rgba) -> None:
        """
        Function to get color of a pixel on the current displayed image
        :param event: the event of clicking on a canvas pixel
        :param rgba: the rgba image displayed on the canvas
        """
        try: # Sometimes the canvas has an issue where clicking the edge of the canvas results in an IndexError
            pixel_pos = (event.x, event.y) # Get the pixel's position and the hex code at the position
            pixel_code = self.rgba_to_hex(rgba.getpixel(pixel_pos)) # Converts the pixel's rgb value to hex code
            for i in range(self.palette_length - 1, 0, -1): # To push the least recent color over to the right
                current_label = self.hex_label_list[i]
                next_label = self.hex_label_list[i - 1]
                # Change the current label to the one on the left
                current_label.config(state="normal")
                current_label.delete(0, tk.END)
                current_label.insert(0, next_label.get())
                current_label.config(state="readonly")
                current_frame = self.color_frame_list[i]
                next_frame = self.color_frame_list[i - 1]
                # Change the current color to the one on the left
                current_frame.config(bg=next_frame.cget("bg"))
            # Put most recent pixel color onto the leftmost square
            self.hex_label_list[0].config(state="normal")
            self.hex_label_list[0].delete(0, tk.END)
            self.hex_label_list[0].insert(0, pixel_code)
            self.hex_label_list[0].config(state="readonly")
            self.color_frame_list[0].config(bg=pixel_code)
        except IndexError:
            pass

    def rgba_to_hex(self, rgba) -> str:
        """
        Converts a rgba tuple full of integer values into a hexadecimal code string
        :param rgba: the rgba tuple to be converted (rgba accounts for images with transparency)
        :return: the hexadecimal string
        """
        # r = red, b = blue, g = green, a = alpha
        r, g, b, a = rgba
        # :02x = 2-digit hex, zero-padding if needed
        return f'#{r:02x}{g:02x}{b:02x}'

    def find_image(self) -> None:
        """
        Finds the image based on the image file path from the text entry and displays it on the canvas
        """
        try:
            image_file_path = askopenfilename() # Bring up user file system to allow them to open a file
            if image_file_path: # If the image file path exists
                # Try to open the new image file and display it
                self.current_image_pil = Image.open(image_file_path).resize((self.image_size, self.image_size))
                self.current_image_rgba = self.current_image_pil.convert("RGBA")
                self.current_image = ImageTk.PhotoImage(self.current_image_pil)
                self.canvas.itemconfig(self.canvas_image, image=self.current_image)
                # The canvas will run the function get_pixel_color() any time the left mouse button clicks on it
                self.canvas.bind("<Button-1>", func=lambda event: self.get_pixel_color(event, self.current_image_rgba))
                # Reset the palette when a new image is displayed
                for i in range(self.palette_length):
                    self.color_frame_list[i].config(bg=self.window_color) # Reset current color frame
                    # Reset the current hex label
                    self.hex_label_list[i].config(state="normal")
                    self.hex_label_list[i].delete(0, tk.END)
                    self.hex_label_list[i].config(state="readonly")
        except (IsADirectoryError, PIL.UnidentifiedImageError, TimeoutError): # In the case a directory/non-image file is selected
            messagebox.showerror("ERROR!", "Invalid image file.\nPlease try again.")
        else:
            if image_file_path: # If the image file path exists
                self.image_path_entry.config(state="normal")  # Allow text entry to be edited
                self.image_path_entry.delete(0, tk.END) # Delete all text inside entry
                self.image_path_entry.insert(0, image_file_path) # Write image file path to entry
                self.image_path_entry.config(state="readonly")  # Set it back to read only
