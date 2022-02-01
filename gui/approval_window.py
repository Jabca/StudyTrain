from random import choice
from time import sleep
from tkinter import *

from PIL import ImageGrab
from docx_interaction import save_dir_to_docx


class ApproveWindow:
    def __init__(self, root, figures: dict, to_save_dir: str, amount_to_generate,
                 window_width=440,
                 window_height=600,
                 canvas_width=400,
                 canvas_height=350,
                 offset_width=75):

        self.cur_image_num = 0
        self.amount_to_generate = amount_to_generate
        self.width = window_width
        self.height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.figure = None
        self.figures = figures
        self.offset_width = offset_width
        self.to_save_dir = to_save_dir

        self.root_window = root
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.configure(bg="white")

        self.root_canvas = Canvas(self.root_window, width=self.canvas_width, height=self.canvas_height, bg='white',
                                  bd=3)

        self.root_window.winfo_toplevel().title("Approve window")
        self.render_window()
        self.update_window()

        self.root_window.bind("<Key>", lambda e: self.arrow_handler(e.keysym))
        self.root_window.bind("<Return>", lambda e: self.approve())
        self.root_window.bind("<Escape>", lambda e: self.cancel())

    def update_window(self):
        self.update_canvas()
        if self.figure is not None:
            try:
                self.angle_scale.set(self.figure.projecting_angle)
            except ValueError:
                self.angle_scale.set(45)
            self.y_scale.config(from_=self.figure.y_offset - self.offset_width,
                                to=self.figure.y_offset + self.offset_width)
            self.y_scale.set(self.figure.y_offset)

            self.x_scale.config(from_=self.figure.x_offset - self.offset_width,
                                to=self.figure.x_offset + self.offset_width)
            self.x_scale.set(self.figure.x_offset)
        self.root_window.update()

    def update_canvas(self):
        self.root_canvas.delete("all")
        if self.figure is not None:
            self.figure.render()
        self.root_canvas.update()

    def render_window(self):
        self.root_canvas.place(relx=0.14, rely=0.09, relheight=0.7, relwidth=0.84)

        self.angle_scale = Scale(self.root_window, from_=0, to=90, orient=HORIZONTAL, bg="white", bd=0,
                                 highlightbackground="white")
        self.angle_scale.place(relx=0.12, rely=0, relheight=0.08, relwidth=0.84)
        self.angle_scale.bind("<Motion>", lambda x: self.change_angle(self.angle_scale.get()))

        self.y_scale = Scale(self.root_window, from_=0, to=100, orient=VERTICAL, bg="white", bd=0,
                             highlightbackground="white")
        self.y_scale.place(relx=0.01, rely=0.1, relheight=0.7, relwidth=0.12)
        self.y_scale.bind("<Motion>", lambda x: self.change_y_offset(self.y_scale.get()))

        self.x_scale = Scale(self.root_window, from_=0, to=100, orient=HORIZONTAL, bg="white", bd=0,
                             highlightbackground="white")
        self.x_scale.place(relx=0.12, rely=0.8, relheight=0.08, relwidth=0.84)
        self.x_scale.bind("<Motion>", lambda x: self.change_x_offset(self.x_scale.get()))

        self.approve_image = PhotoImage(file="gui/source/green_check.png")
        self.approve_image = self.approve_image.subsample(8, 8)
        self.approve_b = Button(self.root_window, image=self.approve_image, bd=0, bg="white",
                                highlightbackground="white")
        self.approve_b["command"] = lambda: self.approve()
        self.approve_b.place(relx=0.15, rely=0.87, relheight=0.12, relwidth=0.3)

        self.cancel_image = PhotoImage(file="gui/source/red_cross.png")
        self.cancel_image = self.cancel_image.subsample(8, 8)
        self.cancel_b = Button(self.root_window, image=self.cancel_image, bd=0, bg="white", highlightbackground="white")
        self.cancel_b.place(relx=0.55, rely=0.87, relheight=0.12, relwidth=0.3)
        self.cancel_b["command"] = lambda: self.cancel()

        self.update_window()

    def change_angle(self, angle: int) -> None:
        if self.figure is not None:
            if self.figure.projecting_angle != angle:
                self.figure.set_angle(angle)
                self.update_canvas()

    def change_y_offset(self, offset: int):
        if self.figure is not None:
            if self.figure.y_offset != offset:
                self.figure.set_y_offset(offset)
                self.update_canvas()

    def change_x_offset(self, offset: int):
        if self.figure is not None:
            if self.figure.x_offset != offset:
                self.figure.set_x_offset(offset)
                self.update_canvas()

    def generate_next_figure(self):
        figure = choice(list(self.figures.values()))
        figure.clear()
        figure.set_angle(45)
        figure.create_3_dots()
        figure.cross_figure_with_plain()
        while figure.shoelace_formula() < 10000 and len(figure.plain_crossing_points) <= 4:
            figure.clear()
            figure.create_3_dots()
            figure.cross_figure_with_plain()
        self.figure = figure
        self.figure.parent = self
        self.figure.number_of_figure = self.cur_image_num

    def get_canvas(self):
        x = self.root_window.winfo_rootx() + self.root_canvas.winfo_x()
        y = self.root_window.winfo_rooty() + self.root_canvas.winfo_y()
        x1 = x + self.root_canvas.winfo_width()
        y1 = y + self.root_canvas.winfo_height()
        return ImageGrab.grab().crop((x, y, x1, y1))

    def approve(self):
        image = self.get_canvas()
        image.save(f"{self.to_save_dir}/teacher/{self.cur_image_num}.png")

        self.figure.clear_for_task()
        self.update_window()

        sleep(0.1)
        image = self.get_canvas()
        image.save(f"{self.to_save_dir}/students/{self.cur_image_num}.png")

        self.figure.clear()
        self.cur_image_num += 1
        self.amount_to_generate -= 1
        if self.amount_to_generate <= 0:
            self.root_window.destroy()
            save_dir_to_docx(f"{self.to_save_dir}/students", f"{self.to_save_dir}/students.docx")
            save_dir_to_docx(f"{self.to_save_dir}/teacher", f"{self.to_save_dir}/teacher.docx")
            return

        self.generate_next_figure()
        self.update_window()

    def cancel(self):
        self.generate_next_figure()
        self.update_window()

    def arrow_handler(self, key_type):
        if key_type == "Up":
            self.change_y_offset(self.y_scale.get() - 1)
            self.y_scale.set(self.figure.y_offset)
        elif key_type == 'Down':
            self.change_y_offset(self.y_scale.get() + 1)
            self.y_scale.set(self.figure.y_offset)
        elif key_type == "Left":
            self.change_x_offset(self.x_scale.get() - 1)
            self.x_scale.set(self.figure.x_offset)
        elif key_type == "Right":
            self.change_x_offset(self.x_scale.get() + 1)
            self.x_scale.set(self.figure.x_offset)
        elif key_type == "KP_Add":
            self.change_angle(self.angle_scale.get() + 1)
            self.angle_scale.set(self.figure.projecting_angle)
        elif key_type == "KP_Subtract":
            self.change_angle(self.angle_scale.get() - 1)
            self.angle_scale.set(self.figure.projecting_angle)
