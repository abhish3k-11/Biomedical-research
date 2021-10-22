# imports
from tkinter import *
#from Tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import threading
from imutils.video import WebcamVideoStream
import cv2
import time
import numpy as np
import math
import socket
from os import listdir
from os.path import isfile, join
from functools import reduce
#from googleapiclient.http import MediaFileUpload
import time
import os
#from barcode import EAN13


# creating class Window inheriting Frame from tkinter
class Window(Frame):
    # creating constructor function
    def __init__(self, master=None):
        self.frame = None
        self.panel = None
        self.vs = None
        Frame.__init__(self, master)
        self.master = master

        # Loading required logos
        load = Image.open("power.png")
        load = load.resize((45, 45), Image.ANTIALIAS)
        self.power_img = ImageTk.PhotoImage(load)
        load = Image.open("cor.png")
        load = load.resize((45, 45), Image.ANTIALIAS)
        self.cor_img = ImageTk.PhotoImage(load)
        load = Image.open("wrong.png")
        load = load.resize((45, 45), Image.ANTIALIAS)
        self.wrong_img = ImageTk.PhotoImage(load)
        load = Image.open("add_p1.png")
        load = load.resize((50, 50), Image.ANTIALIAS)
        self.add_p_img = ImageTk.PhotoImage(load)
        load = Image.open("manual.png")
        load = load.resize((32, 32), Image.ANTIALIAS)
        self.manual_img = ImageTk.PhotoImage(load)
        load = Image.open("warning.png")
        load = load.resize((30, 30), Image.ANTIALIAS)
        self.warning_img = ImageTk.PhotoImage(load)
        load = Image.open("home.png")
        load = load.resize((55, 60), Image.ANTIALIAS)
        self.home_img = ImageTk.PhotoImage(load)
        load = Image.open("spacing.png")
        load = load.resize((474, 146), Image.ANTIALIAS)
        self.spacing_img = ImageTk.PhotoImage(load)

        # initializing vars
        self.unactive_color = 'LightBlue3'
        self.active_color = 'LightGray'
        self.PatientID_StrVar = StringVar(value='Patient ID: ')
        self.left_eye = 0
        self.right_eye = 0
        self.left_nails = 0
        self.right_nails = 0
        self.mucous = 0
        self.palm = 0
        self.video_thread = False
        self.date_time_thread = False
        self.rgb_frame = 0
        self.init_window(-1)

    def init_window(self, page_no):
        self.remove_widgets(page_no)
        print("O page_no init_window")
        # removing previous page widgets
        # self.remove_widgets(page_no)
        time.sleep(0.5)
        self.master.title("GUI")

        # packing the frame
        self.pack(fill=BOTH, expand=1)

        # if page_no == -1:
        #    self.uploading_message = Label(self, text="Processing. Please wait....", font=('Times New Roman', 22, "bold"),bg="white")
        #    self.uploading_message.place(x=10, y=10, width=460, height=300)
        # connection to drive and folder here

        page_no = 0
        # left_eye = 0
        # right_eye = 0
        # left_nails = 0
        # right_nails = 0
        # mucous = 0
        # palm = 0
        # date Label
        self.date_l = Label(self, text=datetime.datetime.now().strftime(
            '%d/%m/%Y'), font=("Times New Roman", 17, "bold"), bg="white", anchor='w')
        self.date_l.place(x=10, y=5, width=150)

        # time label
        self.time_l = Label(self, text=datetime.datetime.now().strftime(
            '%H:%M:%S'), font=("Times New Roman", 17, "bold"), bg="white", anchor='e')
        self.time_l.place(x=320, y=5, width=150)

        # creating date time thread
        self.dt_thread = threading.Thread(target=self.date_time)

        # patient id label
        self.PID = Label(self, textvariable=self.PatientID_StrVar, font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.PID.place(x=10, y=50, width=460)

        # patient name Label
        self.P_name = Label(self, text='Name:', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.P_name.place(x=10, y=90, width=100)

        # patient age Label
        self.P_age = Label(self, text='Age:', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.P_age.place(x=10, y=145, width=100)

        # patient gender Label
        self.P_gender = Label(self, text='Gender:', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.P_gender.place(x=250, y=145, width=100)

        # patient height Label
        self.P_height = Label(self, text='Height:', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.P_height.place(x=10, y=200, width=100)

        # patient weight Label
        self.P_weight = Label(self, text='Weight:', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.P_weight.place(x=250, y=200, width=100)

        # Fetch patient data button
        self.fetch_btn = Button(self, text='Fetch', bg='LightGray', activebackground='LightGray', font=(
            "Times New Roman", 17, 'bold'), border='1', state=DISABLED)
        self.fetch_btn.place(x=11, y=260, width=146, height=55)

        # New patient button
        self.add_p_btn = Button(self, text='Add \nPatient', compound=LEFT, bg='LightBlue3',
                                activebackground='LightBlue3', border='1', font=("Times New Roman", 17, 'bold'), state=DISABLED)
        self.add_p_btn.place(x=167, y=260, width=146, height=55)

        # Next page button
        self.next_page1_btn = Button(self, text='Next', bg='LightBlue3', activebackground='LightBlue3',
                                     border='1', font=("Times New Roman", 17, 'bold'), command=lambda: self.all_images(page_no))
        self.next_page1_btn.place(x=323, y=260, width=146, height=55)

        # making date time thrad active
        self.date_time_thread = True
        self.dt_thread.start()
    
    def date_time(self):
        while self.date_time_thread:
            self.date_l.configure(text=datetime.datetime.now().strftime('%d/%m/%Y'))
            self.time_l.configure(text=datetime.datetime.now().strftime('%H:%M:%S'))
    
    def stop_date_time(self):
        self.date_time_thread = False

    def all_images(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no
        page_no = 1
        print("In all images, page_no 1")
        # packing the frame
        self.pack(fill=BOTH, expand=1)

        # left eye
        self.left_eye_img = Button(self, border='1', bg="grey")
        self.left_eye_img.place(x=10, y=10, width=146, height=100)
        if self.left_eye:
            self.left_eye_img['image'] = self.left_eye
        else:
            self.left_eye_img['text'] = 'Empty'
        self.left_eye_btn = Button(self, text='Left Eye', font=(
            'Times New Roman', 22, "bold"), bg="white", command=lambda: self.camera_fun(page_no, 'le'))
        self.left_eye_btn.place(x=10, y=100, width=146, height=30)

        # right eye, NOTEEEEEEEEE - change every element to left_eye syntax
        if self.right_eye:
            self.right_eye_img = Label(
                self, image=self.right_eye, border='1', bg="grey")
            self.right_eye_img.place(x=166, y=10, width=146, height=100)
        else:
            self.right_eye_img = Label(self, text='Empty', font=(
                'Times New Roman', 22, "bold"), bg="grey")
            self.right_eye_img.place(x=166, y=10, width=146, height=100)
        self.right_eye_btn = Button(self, text='Right Eye', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.right_eye_btn.place(x=166, y=100, width=146, height=30)

        # mucous
        if self.mucous:
            self.mucous_img = Label(
                self, image=self.mucous, border='1', bg="grey")
            self.mucous_img.place(x=322, y=10, width=146, height=100)
        else:
            self.mucous_img = Label(self, text='Empty', font=(
                'Times New Roman', 22, "bold"), bg="grey")
            self.mucous_img.place(x=322, y=10, width=146, height=100)
        self.mucous_btn = Button(self, text='Mucous', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.mucous_btn.place(x=322, y=100, width=146, height=30)

        # left nails
        if self.left_nails:
            self.left_nails_img = Label(
                self, image=self.left_nails, border='1', bg="grey")
            self.left_nails_img.place(x=10, y=140, width=146, height=100)
        else:
            self.left_nails_img = Label(self, text='Empty', font=(
                'Times New Roman', 22, "bold"), bg="grey")
            self.left_nails_img.place(x=10, y=140, width=146, height=100)
        self.left_nails_btn = Button(self, text='Left Nails', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.left_nails_btn.place(x=10, y=240, width=146, height=30)

        # right nails
        if self.right_nails:
            self.right_nails_img = Label(
                self, image=self.right_nails, border='1', bg="grey")
            self.right_nails_img.place(x=166, y=140, width=146, height=100)
        else:
            self.right_nails_img = Label(self, text='Empty', font=(
                'Times New Roman', 22, "bold"), bg="grey")
            self.right_nails_img.place(x=166, y=140, width=146, height=100)
        self.right_nails_btn = Button(self, text='Right Nails', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.right_nails_btn.place(x=166, y=240, width=146, height=30)

        # palm
        if self.palm:
            self.palm_img = Label(
                self, image=self.palm, border='1', bg="grey")
            self.palm_img.place(x=322, y=140, width=146, height=100)
        else:
            self.palm_img = Label(self, text='Empty', font=(
                'Times New Roman', 22, "bold"), bg="grey")
            self.palm_img.place(x=322, y=140, width=146, height=100)
        self.palm_btn = Button(self, text='Palm', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.palm_btn.place(x=322, y=240, width=146, height=30)

        # back button
        self.back = Button(self, text='Back', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.init_window(page_no))
        self.back.place(x=10, y=280, width=146, height=38)

        # next button
        self.next_page2_btn = Button(self, text='Next', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3")
        self.next_page2_btn.place(x=322, y=280, width=146, height=38)

    # def barcode_page(self, page_no):
    #     self.remove_widgets(page_no)
    #     # current page no;
    #     page_no = 4

    #     # packing the frame
    #     self.barcode_label = Label(self, font=(
    #         'Times New Roman', 22, "bold"), bg="grey")
    #     self.next_page2_btn.place(x=100, y=50, width=280, height=100)
    #     Label(self, text="Barcode is being printed", font=('Times New Roman', 22)).place(x=100, y=160, width=280, height=50)
    #     return

    def camera_fun(self, page_no, image_type):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no
        page_no = 2
        print("In camera function, page_no 2")
        # packing the frame
        # self.pack(fill=BOTH, expand=1) y=320 X x=480

        # adding label to show video frame
        self.frame = None
        self.vid_frame = Frame(self, bg='grey')
        self.vid_frame.place(x=10, y=10, width=460, height=245)
        self.video_label = Label(self.vid_frame)
        self.video_label.place(x=10, y=10, width=460, height=245)

        self.video_thread = True
        self.vs = WebcamVideoStream(src=0).start()
            # time.sleep(0.5)
        self.thread_lock = threading.Lock()
        # back button
        self.back_to_1 = Button(self, text='Back', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.all_images(page_no))
        self.back_to_1.place(x=10, y=265, width=146, height=50)

        # next button
        self.snapshot_btn = Button(self, text='Capture', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3")
        self.snapshot_btn.place(x=322, y=265, width=146, height=50)
        # command action for snapshot_btn
        # le = left eye, re = right eye, rn = right nails, ln = left nails, mc = mucous, pl = palm
        if image_type == 'le':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 'le')

        if image_type == 're':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 're')

        if image_type == 'ln':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 'ln')

        if image_type == 'rn':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 'rn')

        if image_type == 'mc':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 'mc')

        if image_type == 'pl':
            self.snapshot_btn['command'] = lambda: self.snapshot(page_no, 'pl')

        # getting video
        # self.capture = cv2.VideoCapture(0)
        # while True:
        #     # add a green rectangle
        #     self.frame = self.capture.read()[1]
        #     self.frame = cv2.flip(self.frame, 1)
        #     if self.frame is not None:
        #         self.rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        #     self.frame = ImageTk.PhotoImage(Image.fromarray(self.rgb_frame))
        #     self.video_label['image'] = self.frame
        #     self.update()

        # self.capture.release()
        # testing
        self.v_thread = threading.Thread(target=self.videoLoop)
        self.v_thread.start()

    def videoLoop(self):
        while self.video_thread:
            self.frame = self.vs.read()
            self.frame = cv2.flip(self.frame, 1)
            if self.frame is not None:
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.rgb_frame = self.image
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            self.thread_lock.acquire()
            self.video_label.configure(image=self.image)
            self.video_label.image = self.image
            self.thread_lock.release()
        self.vs.stop()

    def video_close(self):
        #print("\nvideo close");
        self.eye_video_thread = False

    def snapshot(self, page_no, image_type):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no is 3
        page_no = 3

        # snapshot Label
        self.snapshot_taken = ImageTk.PhotoImage(
            Image.fromarray(self.rgb_frame))
        self.snapshot_label = Label(self, image=self.snapshot_taken, bg='grey')
        self.snapshot_label.place(x=10, y=10, width=460, height=245)

        # back button
        self.back_to_1 = Button(self, text='Back', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.all_images(page_no))
        self.back_to_1.place(x=10, y=265, width=146, height=50)

        # next button
        self.next_page1_btn = Button(self, text='Next', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.all_images(page_no))
        self.next_page1_btn.place(x=322, y=265, width=146, height=50)

        # passing image to all images
        # le = left eye, re = right eye, rn = right nails, ln = left nails, mc = mucous, pl = palm
        if image_type == 'le':
            self.left_eye = self.snapshot_taken

        if image_type == 're':
            self.left_eye = self.snapshot_taken

        if image_type == 'ln':
            self.left_eye = self.snapshot_taken

        if image_type == 'rn':
            self.left_eye = self.snapshot_taken

        if image_type == 'mc':
            self.left_eye = self.snapshot_taken

        if image_type == 'pl':
            self.left_eye = self.snapshot_taken

        # retake button
        self.retake = Button(self, text='Retake', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.camera_fun(page_no, image_type))
        self.retake.place(x=166, y=265, width=146, height=50)

        return

    def remove_widgets(self, page_no):
        if page_no == 0:
            self.next_page1_btn.place_forget()
            self.add_p_btn.place_forget()
            self.fetch_btn.place_forget()
            self.PID.place_forget()
            self.time_l.place_forget()
            self.date_l.place_forget()
            self.P_age.place_forget()
            self.P_gender.place_forget()
            self.P_height.place_forget()
            self.P_weight.place_forget()
            self.P_name.place_forget()
            print("Widgets on initialization removed")

        if page_no == 1:
            self.left_eye_img.place_forget()
            self.left_eye_btn.place_forget()
            self.right_eye_img.place_forget()
            self.right_eye_btn.place_forget()
            self.left_nails_img.place_forget()
            self.left_nails_btn.place_forget()
            self.right_nails_img.place_forget()
            self.right_nails_btn.place_forget()
            self.mucous_img.place_forget()
            self.mucous_btn.place_forget()
            self.palm_img.place_forget()
            self.palm_btn.place_forget()
            self.back.place_forget()
            self.next_page2_btn.place_forget()
            print("Widgets on all images (page_no 1) removed")

        if page_no == 2:
            self.video_label.place_forget()
            self.vid_frame.place_forget()
            self.back_to_1.place_forget()
            self.snapshot_btn.place_forget()
            # self.capture.release()
            self.vs.stop()
            self.video_close()
            self.vs = WebcamVideoStream(src=0).stop()
            cv2.destroyAllWindows()
            print("capture released")
            print("Wdigets on camera func, page 2, removed")

        if page_no == 3:
            self.snapshot_label.place_forget()
            self.back_to_1.place_forget()
            self.retake.place_forget()
            self.next_page1_btn.place_forget()
            print("Wdigets on snapshot, page 3, removed")


def main():
    root = Tk()
    root.geometry('%dx%d+%d+%d' % (480, 320, 0, -30))
    root.resizable(False, False)

    # creation of an instance
    app = Window(root)
    app.configure(background="white")
    # mainloop
    root.mainloop()

# in all images next button --> will take to application final page 4 where info will be saved, throw barcode and print using thermal printer and err if err is caught
# add patient button
# fetch patient information button


if __name__ == '__main__':
    main()
