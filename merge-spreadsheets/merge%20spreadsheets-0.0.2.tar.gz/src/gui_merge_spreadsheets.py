import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from .spreadsheets import merge_directory

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master

        self.directory_var = tk.StringVar()

        tk.Label(self, text="Source:").pack(side=tk.LEFT)

        tk.Entry(
            self,
            textvariable=self.directory_var,
        ).pack(side=tk.LEFT, expand=True)

        tk.Button(
            self,
            text='...',
            command=self.directory_choose_button,
        ).pack()

        tk.Button(
            self,
            text='close',
            command=self.close_button
        ).pack(side=tk.LEFT, expand=True)

        tk.Button(
            self,
            text='merge',
            command=self.merge_button
        ).pack(side=tk.LEFT, expand=True)

        self.pack()

    def directory_choose_button(self):
        directory = filedialog.askdirectory()
        print(directory)
        self.directory_var.set(directory)

    def close_button(self):
        self.root.destroy()

    def merge_button(self):
        merge_directory(
            self.directory_var.get(),
            'Сводная таблица.xlsx'
        )

        messagebox.showinfo(title='Merge', message='done')



def main():
    root = tk.Tk()
    frame = MainFrame(root)
    frame.mainloop()

if __name__ == '__main__':
    main()
