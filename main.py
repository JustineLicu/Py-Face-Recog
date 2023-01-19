import cv2
import numpy as np
import face_recognition as fr
import tkinter as tk
import customtkinter as ct
from PIL import Image, ImageTk
from start_id import sid
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ct.set_appearance_mode("Light")


class App(ct.CTk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Face Recognition using OpenCV")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(width=False, height=False)
        self.iconbitmap(BASE_DIR + "\\poweredby24.ico")

        self.img_holder = ct.CTkLabel(master=self, text="")
        self.img_holder.place(x=0, y=0, relwidth=1, relheight=1)

        self.cmd_sid = ct.CTkButton(master=self, text="Start ID", command=self.start_id)
        self.cmd_sid.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="w")

        self.cmd_camera = ct.CTkButton(
            master=self, text="Open Camera", command=self.open_camera
        )
        self.cmd_camera.grid(row=1, column=0, pady=5, padx=20, sticky="w")

        self.cmd_save = ct.CTkButton(master=self, text="Save", command=self.save_img)
        self.cmd_save.grid(row=2, column=0, pady=5, padx=20, sticky="w")

        self.cmd_retake = ct.CTkButton(master=self, text="Retake", command=self.retake)
        self.cmd_retake.grid(row=3, column=0, pady=5, padx=20, sticky="w")

        self.cmd_exit = ct.CTkButton(master=self, text="Exit", command=self.exit_app)
        self.cmd_exit.grid(row=4, column=0, pady=5, padx=20, sticky="w")

        self.cancel = False
        self.camerabtn_switch(False)
        self.btn_switch(self.cmd_save, stat=False)
        self.btn_switch(self.cmd_retake, stat=False)

    def start_id(self):
        sid(self)

    def open_camera(self):
        self.cancel = False
        self.camerabtn_switch(True)

        self.cap = cv2.VideoCapture(0)

        success, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        self.prevImg = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.prevImg)
        self.img_holder.imgtk = imgtk
        self.img_holder.configure(image=imgtk)

        if not self.cancel:
            self.img_holder.after(10, self.show_frame)

    def capture(self):
        self.cancel = True
        self.btn_switch(self.cmd_camera, stat=False)
        self.btn_switch(self.cmd_save, stat=True)
        self.btn_switch(self.cmd_retake, stat=True)

        self.txt_imgfname = ct.CTkEntry(
            master=self, width=240, placeholder_text="e.g.: Steve Rogers"
        )
        self.txt_imgfname.grid(row=5, column=0, pady=5, padx=20, sticky="w")

    def save_img(self):
        success, frame = self.cap.read()
        cv2.imwrite(
            BASE_DIR + "\\ImageList\\" + self.txt_imgfname.get() + ".png", frame
        )

        self.img_holder.imgtk = None
        self.img_holder.configure(image=None)
        self.txt_imgfname.destroy()
        self.camerabtn_switch(False)
        self.btn_switch(self.cmd_save, stat=False)
        self.btn_switch(self.cmd_retake, stat=False)

    def retake(self):
        self.cancel = False

        self.txt_imgfname.destroy()
        self.btn_switch(self.cmd_camera, stat=True)
        self.btn_switch(self.cmd_save, stat=False)
        self.btn_switch(self.cmd_retake, stat=False)

        self.img_holder.after(10, self.show_frame)

    def exit_app(self):
        self.quit()

    def camerabtn_switch(self, stat: bool):
        if not stat:
            self.cmd_camera = ct.CTkButton(
                master=self, text="Open Camera", command=self.open_camera
            )
            self.cmd_camera.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        else:
            self.cmd_camera = ct.CTkButton(
                master=self, text="Capture", command=self.capture
            )
            self.cmd_camera.grid(row=1, column=0, pady=5, padx=20, sticky="w")

    def btn_switch(self, btn: ct.CTkButton, stat: bool):
        if not stat:
            btn.configure(state="disabled")
        else:
            btn.configure(state="normal")

    def show_frame(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        self.prevImg = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.prevImg)
        self.img_holder.imgtk = imgtk
        self.img_holder.configure(image=imgtk)

        if not self.cancel:
            self.img_holder.after(10, self.show_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
