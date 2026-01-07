import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Новый более мягкий цвет фона
COLORBG = '#A8D5BA'  # светлый зеленовато-голубой

def center_window(win, width=800, height=600):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добро пожаловать!")
        self.configure(background=COLORBG)
        self.overrideredirect(True)
        self.resizable(False, False)

        window_width, window_height = 800, 600
        center_window(self, window_width, window_height)

        self.main_text = tk.Label(
            self,
            text="✨ Загружаю ваш фин. планер... ✨",
            font=("Arial Rounded MT Bold", 22),
            bg=COLORBG,
            fg='#333333'  # тёмно-серый
        )
        self.main_text.pack(pady=20)

        self.canvas = tk.Canvas(self, width=700, height=400, bg=COLORBG, highlightthickness=0)
        self.canvas.pack()

        self.money_gif = Image.open("data/mr-krabs-money.gif")

        self.frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(self.money_gif)]
        self.frame_index = 0
        self.money_image = self.canvas.create_image(350, 200, image=self.frames[0])  # Центр

        self.animate_gif()

        self.signature = tk.Label(
            self,
            text="@Y4DOV1N",
            font=("Arial", 10),
            bg=COLORBG,
            fg='gray30'
        )
        self.signature.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')

        self.blink_state = True
        self.animate_text()

        self.after(4000, self.close_window)

    def animate_text(self):
        if self.blink_state:
            self.main_text.config(fg='#555555')  # тёмно-серый
        else:
            self.main_text.config(fg='#999999')  # светло-серый
        self.blink_state = not self.blink_state
        self.after(500, self.animate_text)

    def close_window(self):
        self.destroy()

    def animate_gif(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.canvas.itemconfig(self.money_image, image=self.frames[self.frame_index])
        self.after(100, self.animate_gif)