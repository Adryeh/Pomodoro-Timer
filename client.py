from config import *
from tkinter import *
from tkinter.colorchooser import askcolor
from utils import humanize_time, send_announcement


class PomodoroApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Pomodoro")
        self.geometry("300x500")
        self.resizable(False, False)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (WorkingPage, RelaxPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(WorkingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_bg_color(self, cont_list):
        rgb, color_str = askcolor()
        for f in cont_list:
            frame = self.frames[f]
            frame.configure(bg=color_str)
            frame.configure(background=color_str)


class Timer(Frame):
    def __init__(self, parent, timer_type: str, sec: int):
        Frame.__init__(self, parent, bg=BG)
        self.btn_start = Button(parent, text='Start', width=10, borderwidth=0, command=self.refresh_label, bg=BTN_BG,
                                fg='white')
        self.btn_start.pack(pady=5, side=TOP)
        self.btn_stop = Button(parent, text='Stop', width=10,  borderwidth=0, command=self.stop, bg=BTN_BG, fg='white')
        self.btn_stop.pack(pady=5, side=TOP)
        self.work_times = 0
        self.timer_type = timer_type
        self.seconds = sec
        self.counter = IntVar()
        self.counter.set(0)
        self.label = Label(parent, text=f"{self.timer_type} time:\n {self.customize_time(self.seconds)}", bg=BG,
                           font=LARGE_FONT)
        self.label.pack(pady=15)
        self.rounds = Label(parent, text=f"{self.timer_type} rounds: ", bg=BG)
        self.rounds.pack()
        self.count = Label(parent, textvariable=self.counter, bg=BG)
        self.count.pack()

    @staticmethod
    def customize_time(s):
        return humanize_time(s)

    def refresh_label(self):
        if self.seconds > 0:
            self.btn_start['state'] = 'disabled'
            self.seconds -= 1
            self.label.configure(text=f"{self.timer_type} time:\n {self.customize_time(self.seconds)}")
            self.label.after(1000, self.refresh_label)
        else:
            self.work_times += 1
            self.counter.set(self.work_times)
            self.btn_start['state'] = 'normal'
            if self.timer_type == 'Working':
                self.seconds = WORKING_TIME
                send_announcement('Relax!', 'Nice job!')
            else:
                self.seconds = RELAX_TIME
                send_announcement('Work', 'Time to work')
            self.label.configure(text=f"{self.timer_type} time:\n {self.customize_time(self.seconds)}")

    def stop(self):
        self.seconds = 0


class WorkingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BG)

        settings_btn = Button(self, text="Settings", borderwidth=0, command=lambda: controller.show_frame(SettingsPage),
                              bg=BTN_BG, fg='white')
        settings_btn.pack(side=BOTTOM, pady=5)
        relax_btn = Button(self, text="Relax Time", borderwidth=0, command=lambda: controller.show_frame(RelaxPage),
                           bg=BTN_BG, fg='white')
        relax_btn.pack(side=BOTTOM, pady=10)
        work_timer = Timer(self, 'Working', WORKING_TIME)
        work_timer.pack(side=BOTTOM)


class RelaxPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BG)
        settings_btn = Button(self, text="Settings", borderwidth=0, command=lambda: controller.show_frame(SettingsPage),
                              bg=BTN_BG, fg='white')
        settings_btn.pack(side=BOTTOM, pady=5)
        work_btn = Button(self, text="Back to work", borderwidth=0, command=lambda: controller.show_frame(WorkingPage),
                          bg=BTN_BG, fg='white')
        work_btn.pack(side=BOTTOM, pady=10)
        relax_timer = Timer(self, 'Relax', RELAX_TIME)
        relax_timer.pack(side=BOTTOM)


class SettingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BG)
        label = Label(self, text="Settings", font=LARGE_FONT, bg=BG)
        label.pack(pady=10, padx=10, side=TOP)
        # Settings buttons
        bg_color_btn = Button(self, text='Change bg color',
                              command=lambda: controller.change_bg_color([SettingsPage, WorkingPage, RelaxPage]))
        bg_color_btn.pack()
        # Navigation buttons
        work_btn = Button(self, text="Work Page", borderwidth=0, command=lambda: controller.show_frame(WorkingPage),
                          bg=BTN_BG, fg='white')
        work_btn.pack(side=BOTTOM, pady=5)
        relax_btn = Button(self, text="Relax Page", borderwidth=0, command=lambda: controller.show_frame(RelaxPage),
                           bg=BTN_BG, fg='white')
        relax_btn.pack(side=BOTTOM, pady=10)


if __name__ == '__main__':
    app = PomodoroApp()
    app.mainloop()
