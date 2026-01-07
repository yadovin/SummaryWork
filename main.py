import tkinter as tk

from gui import FinanceApp
from startScreen import SplashScreen


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    splash = SplashScreen(root)
    root.wait_window(splash)
    root.deiconify()
    app = FinanceApp(root)
    root.mainloop()
