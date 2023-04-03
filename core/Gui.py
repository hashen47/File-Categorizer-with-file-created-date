import tkinter, os
from .Logic_Thread import Logic_Thread
from tkinter import Frame, ttk, W, S, E, messagebox, filedialog



class Gui(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("File Categorizer")
        self.master.configure(padx=10, pady=10)
        self.master.resizable(False, False)

        self.src = ""
        self.dst = ""
        self.compleated = False # indicate that copy/move process is compleated

        self.set_styles()
        self.create_widgets()
        

    def set_styles(self):
        """
        change some builtin styles of some widgets
        :return None
        """
        self.style = ttk.Style() 
        self.style.configure("TButton", font=('Helvetica', 11))


    def create_widgets(self):
        """
        create all the widgets and add them to grid system
        :return None
        """

        # text variables
        self.src_entry_var = tkinter.StringVar()
        self.dst_entry_var = tkinter.StringVar()
        self.compleated_files_count = tkinter.StringVar()
        self.prog = tkinter.StringVar()
        self.compleated_files_count.set("compleated : 0/0")
        self.prog.set("0%")

        # widgets
        self.src_label = ttk.Label(master=self.master, text="src", font=("Helvetica", 13))
        self.src_label.grid(column=0, row=0, sticky=W)

        self.src_entry = ttk.Entry(master=self.master, state=tkinter.DISABLED, width=50, font=("Helvetica", 12), textvariable=self.src_entry_var)
        self.src_entry.grid(column=0, row=1)

        self.src_btn = ttk.Button(master=self.master, text="SET", command=self.set_src)
        self.src_btn.grid(column=1, row=1, padx=(10, 0))

        self.dst_label = ttk.Label(master=self.master, text="dst", font=("Helvetica", 13))
        self.dst_label.grid(column=0, row=2, columnspan=3, sticky=W, pady=(15, 0))

        self.dst_entry = ttk.Entry(master=self.master, state=tkinter.DISABLED, width=50, font=("Helvetica", 12), textvariable=self.dst_entry_var)
        self.dst_entry.grid(column=0, row=3)

        self.dst_btn = ttk.Button(master=self.master, text="SET", command=self.set_dst)
        self.dst_btn.grid(column=1, row=3, padx=(10, 0))

        self.progress_label = ttk.Label(master=self.master, text="progress", font=("Helvetica", 13))
        self.progress_label.grid(column=0, row=4, columnspan=3, sticky=W, pady=(15,0))

        self.progress_bar = ttk.Progressbar(master=self.master, value=0, length=560)
        self.progress_bar.grid(column=0, row=5, columnspan=3, sticky=W, pady=(5, 6))

        self.compleated = ttk.Label(master=self.master, textvariable=self.compleated_files_count)
        self.compleated.grid(column=0, row=6, sticky=W)

        self.current_progress = ttk.Label(master=self.master, textvariable=self.prog)
        self.current_progress.grid(column=1, row=6, sticky=E)

        self.cancel_btn = ttk.Button(master=self.master, text="cancel", command=self.cancel_btn_func)
        self.cancel_btn.grid(column=1, row=7, sticky=E, pady=(20, 0))

        self.start_btn = ttk.Button(master=self.master, text="start", command=self.start_btn_func)
        self.start_btn.grid(column=0, row=7, sticky=E, pady=(20, 0))


    def update(self, progress, tot, done_tot, compleated=False):
        self.compleated = compleated
        self.prog.set(f"{progress}%")
        self.progress_bar["value"] = int(progress)
        self.compleated_files_count.set(f"compleated : {done_tot}/{tot}")

        if self.compleated:
            if progress == 100:
                messagebox.showinfo(title="Success", message="Successfully copy/move the files")
            elif tot == 0:
                messagebox.showwarning(title="Warning", message="Source is empty or all files are already exist in the destination")
            self.compleated = False 
            self.enable_or_disable_buttons(disable=False)

    
    def set_src(self):
        """
        set the source folder and
        update the src_entry_var value with it
        :return None
        """
        self.src = filedialog.askdirectory()
        if self.src:
            self.src_entry_var.set(self.src)
            messagebox.showinfo("Success", f"You chose {self.src} as the source directory")


    def set_dst(self):
        """
        set the distination folder and
        update the dst_entry_var value with it
        :return None
        """
        self.dst = filedialog.askdirectory() 
        if self.src:
            self.dst_entry_var.set(self.dst)
            messagebox.showinfo("Success", f"You chose {self.dst} as the destination directory")
        else:
            messagebox.showwarning("warning", "set the source folder before set the destination folder")


    def start_btn_func(self):
        """
        create the Categorizer instance and call its methods
        :return None
        """
        if self.src and self.dst:
            self.process = Logic_Thread(self.src, self.dst, self.update)
            self.process.start()
            self.enable_or_disable_buttons()
        else:
            messagebox.showerror(title="Error", message="You should set both src and dst folders before continue")

    
    def enable_or_disable_buttons(self, disable=True):
        """
        enable or disable button (except the cancel button)
        :param disable : bool
        :return None
        """
        if disable:
            state = tkinter.DISABLED
        else:
            state = tkinter.NORMAL

        self.start_btn.configure(state=state)
        self.src_btn.configure(state=state)
        self.dst_btn.configure(state=state)


    def cancel_btn_func(self):
        """
        call the destroy method
        :return None
        """
        self.master.destroy()


    def run(self):
        """
        execute the mainloop
        :return None
        """
        self.master.mainloop()