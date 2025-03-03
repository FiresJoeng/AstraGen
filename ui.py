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
        size = '%dx%d+%d+%d' % (window_width, window_height,
                                (screen_width - window_width) / 2,
                                (screen_height - window_height) / 2)
        self.main_window.geometry(size)

        # 控制变量
        self.search_entry_var = tk.StringVar()

        # 退出按钮
        self.exit_button_title = tk.StringVar(value='退出')
        self.exit_button = tk.Button(self.main_window, textvariable=self.exit_button_title)
        self.exit_button.place(x=260, y=10, width=50, height=25)

        # 配置按钮
        self.config_button_title = tk.StringVar(value='配置')
        self.config_button = tk.Button(self.main_window, textvariable=self.config_button_title)
        self.config_button.place(x=205, y=10, width=50, height=25)

        # 文本输入
        self.search_entry = tk.Entry(
            self.main_window,
            textvariable=self.search_entry_var,
            fg='grey'
        )
        self.search_entry.place(x=30, y=70, width=200, height=25)
        self.search_entry.insert(0, '请输入企业名称关键词')
        self.search_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_entry_focus_out)

        # 搜索按钮
        self.search_button_title = tk.StringVar(value='搜索')
        self.search_button = tk.Button(
            self.main_window,
            textvariable=self.search_button_title,
            command=self._on_search
        )
        self.search_button.place(x=240, y=70, width=60, height=25)

    def _on_entry_focus_in(self, event):
        if self.search_entry_var.get() == '请输入企业名称关键词':
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='black')

    def _on_entry_focus_out(self, event):
        if not self.search_entry_var.get():
            self.search_entry.insert(0, '请输入企业名称关键词')
            self.search_entry.config(fg='grey')

    def _on_search(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = UI(root)
    root.mainloop()