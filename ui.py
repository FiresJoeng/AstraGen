import tkinter as tk


class UI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title('AstraGen 星核')
        self.main_window.resizable(width=False, height=False)
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 320
        window_height = 180
        size = '%dx%d+%d+%d' % (window_width, window_height, (screen_width -
                                window_width) / 2, (screen_height - window_height) / 2)
        self.main_window.geometry(size)

        self.exit_button_title = tk.StringVar()
        self.exit_button_title.set('退出')
        self.exit_button = tk.Button(self.main_window, textvariable=self.exit_button_title)
        self.exit_button.place(x=260, y=10, width=50, height=25)

        self.config_button_title = tk.StringVar()
        self.config_button_title.set('配置')
        self.config_button = tk.Button(self.main_window, textvariable=self.config_button_title)
        self.config_button.place(x=205, y=10, width=50, height=25)


if __name__ == '__main__':
    root = tk.Tk()
    app = UI(root)
    root.mainloop()
