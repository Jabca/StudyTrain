from tkinter import *
from random import choice


class ApproveWindow:
    def __init__(self, root, figures, window_width=440, window_height=600, canvas_width=400, canvas_height=350, offset_width=75):
        self.width = window_width
        self.height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.figure = None
        self.figures = figures
        self.offset_width = offset_width

        self.root_window = root
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.configure(bg="white")

        self.root_canvas = Canvas(self.root_window, width=self.canvas_width, height=self.canvas_height, bg='white',
                                  bd=3)

        self.render_window()
        self.update_window()

    def update_window(self):
        self.update_canvas()
        if self.figure is not None:
            try:
                self.angle_scale.set(self.figure.projecting_angle)
            except ValueError:
                self.angle_scale.set(45)
            self.y_scale.config(from_=self.figure.y_offset - self.offset_width, to=self.figure.y_offset + self.offset_width)
            self.y_scale.set(self.figure.y_offset)

            self.x_scale.config(from_=self.figure.x_offset - self.offset_width, to=self.figure.x_offset + self.offset_width)
            self.x_scale.set(self.figure.x_offset)

    def update_canvas(self):
        self.root_canvas.delete("all")
        if self.figure is not None:
            self.figure.render()
        self.root_canvas.update()

    def render_window(self):
        self.root_canvas.place(relx=0.14, rely=0.09, relheight=0.7, relwidth=0.84)

        self.angle_scale = Scale(from_=0, to=90, orient=HORIZONTAL, bg="white", bd=0, highlightbackground="white")
        self.angle_scale.place(relx=0.12, rely=0, relheight=0.08, relwidth=0.84)
        self.angle_scale.bind("<Motion>", lambda x: self.change_angle(self.angle_scale.get()))

        self.y_scale = Scale(from_=0, to=100, orient=VERTICAL, bg="white", bd=0, highlightbackground="white")
        self.y_scale.place(relx=0.01, rely=0.1, relheight=0.7, relwidth=0.12)
        self.y_scale.bind("<Motion>", lambda x: self.change_y_offset(self.y_scale.get()))

        self.x_scale = Scale(from_=0, to=100, orient=HORIZONTAL, bg="white", bd=0, highlightbackground="white")
        self.x_scale.place(relx=0.12, rely=0.8, relheight=0.08, relwidth=0.84)
        self.x_scale.bind("<Motion>", lambda x: self.change_x_offset(self.x_scale.get()))

        self.approve_image = PhotoImage(file="gui/source/green_check.png")
        self.approve_image = self.approve_image.subsample(8, 8)
        self.approve_b = Button(image=self.approve_image, bd=0, bg="white", highlightbackground="white")
        self.approve_b.place(relx=0.15, rely=0.87, relheight=0.12, relwidth=0.3)

        self.cancel_image = PhotoImage(file="gui/source/red_cross.png")
        self.cancel_image = self.cancel_image.subsample(8, 8)
        self.cancel_b = Button(image=self.cancel_image, bd=0, bg="white", highlightbackground="white")
        self.cancel_b.place(relx=0.55, rely=0.87, relheight=0.12, relwidth=0.3)

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

    def generate_figure(self):
        figure = choice(list(self.figures.values()))
        figure.set_angle(45)
        figure.create_3_dots()
        figure.cross_figure_with_plain()
        while figure.shoelace_formula() < 10000:
            figure.clear()
            figure.create_3_dots()
            figure.cross_figure_with_plain()
        self.figure = figure
        self.figure.parent = self

    def approve(self):
        pass

    def cancel(self):
        pass
