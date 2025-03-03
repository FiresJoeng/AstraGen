import tkinter as tk


class UI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title('AstraGen 星核')
        self.main_window.resizable(width=False, height=False)
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 400
        window_height = 210
        size = f'{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}'
        self.main_window.geometry(size)

        # 控制变量
        self.search_entry_var = tk.StringVar()

        # 欢迎文本
        self.welcome_label = tk.Label(
            self.main_window,
            text='欢迎使用AstraGen 星核',
            font=('Arial', 14)
        )
        self.welcome_label.place(x=100, y=20)

        # 退出按钮
        self.exit_button = tk.Button(
            self.main_window,
            text='退出',
            command=self.main_window.quit,
            bg='#f0f0f0',
            relief='flat'
        )
        self.exit_button.place(x=340, y=10, width=50, height=25)

        # 文本输入
        self.search_entry = tk.Entry(
            self.main_window,
            textvariable=self.search_entry_var,
            fg='grey',
            highlightthickness=2,
            relief='groove'
        )
        self.search_entry.place(x=50, y=70, width=200, height=30)
        self.search_entry.insert(0, '请输入Deepseek的API Key')
        self.search_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_entry_focus_out)
        self.search_entry.bind('<Enter>', self._on_entry_hover)
        self.search_entry.bind('<Leave>', self._on_entry_leave)

        # 搜索按钮
        self.search_button = tk.Button(
            self.main_window,
            text='确认',
            command=self._on_search,
            bg='#006400',
            fg='white',
            relief='flat'
        )
        self.search_button.place(x=270, y=70, width=80, height=30)

    def _on_entry_focus_in(self, event):
        if self.search_entry_var.get() == '请输入Deepseek的API Key':
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='black')
        self.search_entry.config(highlightbackground='#006400', highlightcolor='#006400')

    def _on_entry_focus_out(self, event):
        if not self.search_entry_var.get():
            self.search_entry.insert(0, '请输入Deepseek的API Key')
            self.search_entry.config(fg='grey')
        self.search_entry.config(highlightbackground='#d9d9d9', highlightcolor='#d9d9d9')

    def _on_entry_hover(self, event):
        if not self.search_entry.focus_get():
            self.search_entry.config(highlightbackground='black', highlightcolor='black', bg='#f9f9f9')

    def _on_entry_leave(self, event):
        if not self.search_entry.focus_get():
            self.search_entry.config(highlightbackground='#d9d9d9', highlightcolor='#d9d9d9', bg='white')

    def _on_search(self):
        api_key = self.search_entry_var.get()
        if api_key == '请输入Deepseek的API Key' or not api_key.strip():
            tk.messagebox.showwarning("输入错误", "请输入有效的API Key")
        else:
            # 执行搜索操作
            print(f"API Key: {api_key}")


if __name__ == '__main__':
    root = tk.Tk()
    app = UI(root)
    root.mainloop()