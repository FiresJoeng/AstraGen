import tkinter as tk


class UI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title('AstraGen 星核')
        # 设置页面背景为全白色
        self.main_window.config(bg="white")
        self.main_window.resizable(width=False, height=False)
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 360
        window_height = 500
        size = '%dx%d+%d+%d' % (window_width, window_height,
                                (screen_width - window_width) / 2,
                                (screen_height - window_height) / 2)
        self.main_window.geometry(size)

        # 控制变量
        self.search_entry_var = tk.StringVar()
        self.entry_hovered = False

        # 退出按钮：紧贴右上角
        self.exit_button_title = tk.StringVar(value='退出')
        self.exit_button = tk.Button(self.main_window, textvariable=self.exit_button_title, bg="white")
        self.exit_button.place(x=window_width - 80, y=10, width=70, height=25)
        self.exit_button.bind('<Enter>', self._on_exit_button_hover)
        self.exit_button.bind('<Leave>', self._on_exit_button_hover_leave)

        # 新增：居中的文本标签，放置在搜索栏上方
        self.title_label = tk.Label(self.main_window, text="搜索企业信息",
                                    font=("Sarasa Gothic", 24, "bold"),
                                    fg="#333333", bg="white")
        # 使用相对定位，使标签水平居中，设置 y 坐标为150
        self.title_label.place(relx=0.5, y=130, anchor="center")

        # 文本输入框：加宽为320，高40，居中显示，并整体下移
        self.search_entry = tk.Entry(
            self.main_window,
            textvariable=self.search_entry_var,
            fg='black',
            highlightthickness=1,
            highlightbackground="gray",
            highlightcolor="gray"
        )
        # 设置搜索框居中，x = (360-320)/2 = 20，y 坐标设为220，与标签保持约70像素距离
        self.search_entry.place(x=20, y=220, width=320, height=40)
        self.search_entry.insert(15, '请输入企业名称关键词')
        self.search_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_entry_focus_out)
        self.search_entry.bind('<Enter>', self._on_entry_hover)
        self.search_entry.bind('<Leave>', self._on_entry_hover_leave)

        # 搜索按钮：尺寸宽150，高40，居中位于搜索框下方，并整体下移
        self.search_button_title = tk.StringVar(value='搜索')
        self.search_button = tk.Button(
            self.main_window,
            textvariable=self.search_button_title,
            command=self._on_search,
            bg="#FFCC00",
            fg="black"
        )
        # 计算居中：x = (360-150)/2 = 105，y 坐标设为330
        self.search_button.place(x=105, y=320, width=150, height=40)
        self.search_button.bind('<Enter>', self._on_search_button_hover)
        self.search_button.bind('<Leave>', self._on_search_button_hover_leave)

    def _on_entry_focus_in(self, event):
        if self.search_entry_var.get() == '请输入企业名称关键词':
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='black')
        # 获得焦点时边框设为绿色，边框稍粗
        self.search_entry.config(highlightthickness=1, highlightbackground="#006400", highlightcolor="#006400")

    def _on_entry_focus_out(self, event):
        if not self.search_entry_var.get():
            self.search_entry.insert(0, '请输入企业名称关键词')
            self.search_entry.config(fg='grey')
        # 失去焦点后，根据鼠标是否悬停来设置边框颜色
        if self.entry_hovered:
            self.search_entry.config(highlightthickness=1, highlightbackground="black", highlightcolor="black")
        else:
            self.search_entry.config(highlightthickness=1, highlightbackground="gray", highlightcolor="gray")

    def _on_entry_hover(self, event):
        self.entry_hovered = True
        # 如果当前未获得焦点，鼠标悬停时边框变灰
        if self.search_entry != self.main_window.focus_get():
            self.search_entry.config(highlightbackground="black", highlightcolor="black")

    def _on_entry_hover_leave(self, event):
        self.entry_hovered = False
        # 如果当前未获得焦点，鼠标离开后边框恢复黑色
        if self.search_entry != self.main_window.focus_get():
            self.search_entry.config(highlightbackground="gray", highlightcolor="gray")

    def _on_search_button_hover(self, event):
        # 鼠标悬停在搜索按钮上时，按钮填充颜色变为 #FF9B00
        self.search_button.config(bg="#FF9B00")

    def _on_search_button_hover_leave(self, event):
        # 鼠标离开后恢复搜索按钮填充颜色为 #FFCC00
        self.search_button.config(bg="#FFCC00")

    def _on_search(self):
        pass

    def _on_exit_button_hover(self, event):
        # 鼠标悬停在退出按钮上时，按钮填充颜色变为红色
        self.exit_button.config(bg="#E41B1B")

    def _on_exit_button_hover_leave(self, event):
        # 鼠标离开后恢复退出按钮填充颜色为白色
        self.exit_button.config(bg="white")


if __name__ == '__main__':
    root = tk.Tk()
    app = UI(root)
    root.mainloop()
