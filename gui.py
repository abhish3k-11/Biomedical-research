# imports
from tkinter import *
# from Tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import threading
from imutils.video import WebcamVideoStream
import cv2
import time
import numpy as np
import math
import socket
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from os import listdir
from os.path import isfile, join
from functools import reduce
# from googleapiclient.http import MediaFileUpload
import time
import os
import csv
from Gooogle import Create_Service
from googleapiclient.http import MediaFileUpload
import barcode
from barcode.writer import ImageWriter


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
        self.PatientID_StrVar = StringVar(value='PID: ')
        self.left_eye = 0
        self.right_eye = 0
        self.left_nails = 0
        self.right_nails = 0
        self.mucous = 0
        self.palm = 0
        self.video_thread = False
        self.date_time_thread = False
        self.rgb_frame = 0
        self.patient_name = StringVar(value="Name: ")
        self.patient_age = StringVar(value="Age: ")
        self.patient_gender = StringVar(value="Gender: ")
        self.patient_height = StringVar(value="Height: ")
        self.patient_weight = StringVar(value="Weight: ")
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.API_NAME = 'drive'
        self.API_VERSION = 'v3'
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.service = None
        self.connect_to_drive()
        self.folder_id = '1C1eAzE_VkUu09hAn67BcHPmm90JhtLX0'
        self.init_window(-1)

    def connect_to_drive(self):
        try:
            self.service = Create_Service(
                self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        except:
            print("cannot connect to drive")

    def is_connected(self, host="8.8.8.8", port=53, timeout=0.8):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port))
            return True
        except socket.error as ex:
            return False

    def init_window(self, page_no):
        self.remove_widgets(page_no)
        print("O page_no init_window")
        # removing previous page widgets
        # self.remove_widgets(page_no)
        time.sleep(0.5)
        self.master.title("GUI")
        # packing the frame
        self.pack(fill=BOTH, expand=1)

        if page_no == -1:
            time.sleep(0.5)

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

        # New patient button
        self.add_p_btn = Button(self, text='Add \nPatient', compound=LEFT, bg='LightBlue3',
                                activebackground='LightBlue3', border='1', font=("Times New Roman", 17, 'bold'), command=lambda: self.new_patients(page_no))
        self.add_p_btn.place(x=300, y=150, width=126, height=60)

        # upload btn
        self.upload_btn = Button(self, text='Upload \nData', compound=LEFT, bg='LightBlue3',
                                 activebackground='LightBlue3', border='1', font=("Times New Roman", 17, 'bold'), command=lambda: self.uploadFun(page_no))
        self.upload_btn.place(x=170, y=150, width=126, height=60)

        # power button
        self.power_btn = Button(self, text='Power \nOff', compound=LEFT, bg='LightBlue3',
                                activebackground='LightBlue3', border='1', font=("Times New Roman", 17, 'bold'), command=self.powerFun)
        self.power_btn.place(x=40, y=150, width=126, height=60)

        # making date time thrad active
        self.date_time_thread = True
        self.dt_thread.start()

    def uploadFun(self, page_no):
        self.uploading_message = Label(self, text="Processing. Please wait....", font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.uploading_message.place(x=10, y=10, width=460, height=300)
        print("Entered")
        # if self.is_connected():
        #     if self.service == None:
        #         self.connect_to_drive()

        #     folder_names = [f for f in listdir("patients_data/")]
        #     #try:
        #     for folder_name in folder_names:
        #         print(folder_name)
        #         file_names = [f for f in os.listdir("patients_data/{}/".format(folder_name))]
        #         mime_types = ['image/jpeg' for names in file_names]
        #         for file_name, mime_type in zip(file_names, mime_types):
        #             print(file_names)
        #             file_metadata = {
        #                 'name' : file_name,
        #                 'parents': [self.folder_id]
        #             }
        #             print(file_name)
        #             media = MediaFileUpload("patients_data/{}/{}".format(folder_name, file_name), mimetype=mime_type)
        #             #print()
        #             self.service.files().create(
        #                 body = file_metadata,
        #                 media_body=media,
        #                 fields='id'
        #                 ).execute()
        #os.remove("patients_data/{}/{}".format(folder_name, file_name))
        # except :
        #     print("error while uploading")

        time.sleep(0.5)
        self.uploading_message.place_forget()
        print("Exiting")
        time.sleep(0.5)
        self.init_window(page_no)

    def powerFun(self):
        os.system("sudo shutdown -h now")

    def shiftFun(self, page_no):
        self.remove_widgets(page_no)
        # current page no
        page_no = 12

        # packing Frame
        self.entryText.place(x=8, y=8, height=56, width=307)

        self.shift_btn = Button(self, text='123', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.fetch_patient_data(page_no))
        self.shift_btn.place(x=323, y=10, height=52, width=147)

        # alphabets button
        self.a_btn = Button(self, text='A', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('A'))
        self.a_btn.place(x=10, y=67, height=43, width=71)

        self.b_btn = Button(self, text='B', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('B'))
        self.b_btn.place(x=88, y=67, height=43, width=71)

        self.c_btn = Button(self, text='C', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('C'))
        self.c_btn.place(x=166, y=67, height=43, width=71)

        self.d_btn = Button(self, text='D', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('D'))
        self.d_btn.place(x=244, y=67, height=43, width=71)

        self.e_btn = Button(self, text='E', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('E'))
        self.e_btn.place(x=322, y=67, height=43, width=71)

        self.f_btn = Button(self, text='F', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('F'))
        self.f_btn.place(x=400, y=67, height=43, width=70)

        self.g_btn = Button(self, text='G', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('G'))
        self.g_btn.place(x=10, y=117, height=43, width=71)

        self.h_btn = Button(self, text='H', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('H'))
        self.h_btn.place(x=88, y=117, height=43, width=71)

        self.i_btn = Button(self, text='I', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('I'))
        self.i_btn.place(x=166, y=117, height=43, width=71)

        self.j_btn = Button(self, text='J', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('J'))
        self.j_btn.place(x=244, y=117, height=43, width=71)

        self.k_btn = Button(self, text='K', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('K'))
        self.k_btn.place(x=322, y=117, height=43, width=71)

        self.l_btn = Button(self, text='L', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('L'))
        self.l_btn.place(x=400, y=117, height=43, width=70)

        self.m_btn = Button(self, text='M', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('M'))
        self.m_btn.place(x=10, y=167, height=43, width=71)

        self.n_btn = Button(self, text='N', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('N'))
        self.n_btn.place(x=88, y=167, height=43, width=71)

        self.o_btn = Button(self, text='O', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('O'))
        self.o_btn.place(x=166, y=167, height=43, width=71)

        self.p_btn = Button(self, text='P', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('P'))
        self.p_btn.place(x=244, y=167, height=43, width=71)

        self.q_btn = Button(self, text='Q', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Q'))
        self.q_btn.place(x=322, y=167, height=43, width=71)

        self.r_btn = Button(self, text='R', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('R'))
        self.r_btn.place(x=400, y=167, height=43, width=70)

        self.s_btn = Button(self, text='S', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('S'))
        self.s_btn.place(x=10, y=217, height=43, width=71)

        self.t_btn = Button(self, text='T', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('T'))
        self.t_btn.place(x=88, y=217, height=43, width=71)

        self.u_btn = Button(self, text='U', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('U'))
        self.u_btn.place(x=166, y=217, height=43, width=71)

        self.v_btn = Button(self, text='V', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('V'))
        self.v_btn.place(x=244, y=217, height=43, width=71)

        self.w_btn = Button(self, text='W', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('W'))
        self.w_btn.place(x=322, y=217, height=43, width=71)

        self.x_btn = Button(self, text='X', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('X'))
        self.x_btn.place(x=400, y=217, height=43, width=70)

        self.y_btn = Button(self, text='Y', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Y'))
        self.y_btn.place(x=10, y=267, height=43, width=71)

        self.z_btn = Button(self, text='Z', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Z'))
        self.z_btn.place(x=88, y=267, height=43, width=71)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFun())
        self.clear_btn.place(x=166, y=267, height=43, width=149)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.fetching(page_no))
        self.enter_btn.place(x=322, y=267, height=43, width=148)

    def date_time(self):
        while self.date_time_thread:
            self.date_l.configure(
                text=datetime.datetime.now().strftime('%d/%m/%Y'))
            self.time_l.configure(
                text=datetime.datetime.now().strftime('%H:%M:%S'))

    def stop_date_time(self):
        self.date_time_thread = False

    # function to add new patients
    def new_patients(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # 11 for fetch and 12 for new patients
        # current page no
        page_no = 120
        # 120 is for 12's first page i.e for names
        print("In new patients page add name")
        self.txtVar = StringVar(value="Name :")

        # packing the frame
        # entry text
        self.entryText = Entry(self, textvariable=self.txtVar, font=(
            'Times New Roman', 20), border='3', width=27)
        self.entryText.place(x=8, y=8, height=56, width=464)

        # alphabets button
        self.a_btn = Button(self, text='A', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('A'))
        self.a_btn.place(x=10, y=67, height=43, width=71)

        self.b_btn = Button(self, text='B', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('B'))
        self.b_btn.place(x=88, y=67, height=43, width=71)

        self.c_btn = Button(self, text='C', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('C'))
        self.c_btn.place(x=166, y=67, height=43, width=71)

        self.d_btn = Button(self, text='D', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('D'))
        self.d_btn.place(x=244, y=67, height=43, width=71)

        self.e_btn = Button(self, text='E', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), width=4, command=lambda: self.numFun('E'))
        self.e_btn.place(x=322, y=67, height=43, width=71)

        self.f_btn = Button(self, text='F', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('F'))
        self.f_btn.place(x=400, y=67, height=43, width=70)

        self.g_btn = Button(self, text='G', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('G'))
        self.g_btn.place(x=10, y=117, height=43, width=71)

        self.h_btn = Button(self, text='H', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('H'))
        self.h_btn.place(x=88, y=117, height=43, width=71)

        self.i_btn = Button(self, text='I', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('I'))
        self.i_btn.place(x=166, y=117, height=43, width=71)

        self.j_btn = Button(self, text='J', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('J'))
        self.j_btn.place(x=244, y=117, height=43, width=71)

        self.k_btn = Button(self, text='K', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('K'))
        self.k_btn.place(x=322, y=117, height=43, width=71)

        self.l_btn = Button(self, text='L', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('L'))
        self.l_btn.place(x=400, y=117, height=43, width=70)

        self.m_btn = Button(self, text='M', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('M'))
        self.m_btn.place(x=10, y=167, height=43, width=71)

        self.n_btn = Button(self, text='N', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('N'))
        self.n_btn.place(x=88, y=167, height=43, width=71)

        self.o_btn = Button(self, text='O', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('O'))
        self.o_btn.place(x=166, y=167, height=43, width=71)

        self.p_btn = Button(self, text='P', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('P'))
        self.p_btn.place(x=244, y=167, height=43, width=71)

        self.q_btn = Button(self, text='Q', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Q'))
        self.q_btn.place(x=322, y=167, height=43, width=71)

        self.r_btn = Button(self, text='R', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('R'))
        self.r_btn.place(x=400, y=167, height=43, width=70)

        self.s_btn = Button(self, text='S', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('S'))
        self.s_btn.place(x=10, y=217, height=43, width=71)

        self.t_btn = Button(self, text='T', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('T'))
        self.t_btn.place(x=88, y=217, height=43, width=71)

        self.u_btn = Button(self, text='U', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('U'))
        self.u_btn.place(x=166, y=217, height=43, width=71)

        self.v_btn = Button(self, text='V', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('V'))
        self.v_btn.place(x=244, y=217, height=43, width=71)

        self.w_btn = Button(self, text='W', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('W'))
        self.w_btn.place(x=322, y=217, height=43, width=71)

        self.x_btn = Button(self, text='X', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('X'))
        self.x_btn.place(x=400, y=217, height=43, width=70)

        self.y_btn = Button(self, text='Y', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Y'))
        self.y_btn.place(x=10, y=267, height=43, width=71)

        self.z_btn = Button(self, text='Z', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun('Z'))
        self.z_btn.place(x=88, y=267, height=43, width=71)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFun())
        self.clear_btn.place(x=166, y=267, height=43, width=149)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.enterFun(page_no))
        self.enter_btn.place(x=322, y=267, height=43, width=148)

    def numFun(self, val):
        self.txtVar.set(self.txtVar.get()+str(val))

    def clearFun(self):
        textLen = len(self.txtVar.get())
        if textLen > 6:
            self.txtVar.set(self.txtVar.get()[:textLen-1])

    def enterFun(self, page_no):
        self.patient_name.set(self.patient_name.get()+self.txtVar.get()[6:])
        print(self.patient_name.get())
        self.add_age(page_no)

    def add_age(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # 11 for fetch and 12 for new patients
        # current page no
        page_no = 121
        # 121 is for 12's second page i.e for age
        print("In new patients page add age")
        self.txtVar = StringVar(value="Age : ")

        # packing the frame
        # entry text
        self.entryText = Entry(self, textvariable=self.txtVar, font=(
            'Times New Roman', 20), border='3', width=27)
        self.entryText.place(x=8, y=8, height=56, width=464)

        self.one_btn = Button(self, text='1', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(1))
        self.one_btn.place(x=10, y=72, height=52, width=147)

        self.two_btn = Button(self, text='2', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(2))
        self.two_btn.place(x=167, y=72, height=52, width=146)

        self.three_btn = Button(self, text='3', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(3))
        self.three_btn.place(x=323, y=72, height=52, width=147)

        self.four_btn = Button(self, text='4', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(4))
        self.four_btn.place(x=10, y=134, height=52, width=147)

        self.five_btn = Button(self, text='5', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(5))
        self.five_btn.place(x=167, y=134, height=52, width=146)

        self.six_btn = Button(self, text='6', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(6))
        self.six_btn.place(x=323, y=134, height=52, width=147)

        self.seven_btn = Button(self, text='7', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(7))
        self.seven_btn.place(x=10, y=196, height=52, width=147)

        self.eight_btn = Button(self, text='8', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(8))
        self.eight_btn.place(x=167, y=196, height=52, width=146)

        self.nine_btn = Button(self, text='9', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(9))
        self.nine_btn.place(x=323, y=196, height=52, width=147)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFun())
        self.clear_btn.place(x=10, y=258, height=52, width=147)

        self.zero_btn = Button(self, text='0', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(0))
        self.zero_btn.place(x=167, y=258, height=52, width=146)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.enterFunAge(page_no))
        self.enter_btn.place(x=323, y=258, height=52, width=147)

    def enterFunAge(self, page_no):
        self.patient_age.set(self.patient_age.get()+self.txtVar.get()[6:])
        print(self.patient_age.get())
        self.add_gender(page_no)

    def add_gender(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # 11 for fetch and 12 for new patients
        # current page no
        page_no = 122
        # 121 is for 12's second page i.e for age
        print("In new patients page add age")
        self.txtVar = StringVar(value="Gender : ")

        # packing the frame
        # entry text
        self.entryText = Entry(self, textvariable=self.txtVar, font=(
            'Times New Roman', 20), border='3', width=27)
        self.entryText.place(x=8, y=8, height=56, width=464)

        self.male_btn = Button(self, text='Male', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun("M"))
        self.male_btn.place(x=10, y=134, height=52, width=147)

        self.female_btn = Button(self, text='Female', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun("F"))
        self.female_btn.place(x=167, y=134, height=52, width=146)

        self.others_btn = Button(self, text='Other', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun("O"))
        self.others_btn.place(x=323, y=134, height=52, width=147)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFun())
        self.clear_btn.place(x=10, y=258, height=52, width=147)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.enterFunGender(page_no))
        self.enter_btn.place(x=323, y=258, height=52, width=147)

    def enterFunGender(self, page_no):
        self.patient_gender.set(
            self.patient_gender.get()+self.txtVar.get()[8:])
        print(self.patient_age.get())
        self.add_height(page_no)

    def add_height(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # 11 for fetch and 12 for new patients
        # current page no
        page_no = 123
        # 123 is for 12's fourth page i.e for height
        print("In new patients page add height")
        self.txtVar = StringVar(value="Height: ")

        # packing the frame
        # entry text
        self.entryText = Entry(self, textvariable=self.txtVar, font=(
            'Times New Roman', 20), border='3', width=27)
        self.entryText.place(x=8, y=8, height=56, width=464)

        self.one_btn = Button(self, text='1', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(1))
        self.one_btn.place(x=10, y=72, height=52, width=147)

        self.two_btn = Button(self, text='2', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(2))
        self.two_btn.place(x=167, y=72, height=52, width=146)

        self.three_btn = Button(self, text='3', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(3))
        self.three_btn.place(x=323, y=72, height=52, width=147)

        self.four_btn = Button(self, text='4', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(4))
        self.four_btn.place(x=10, y=134, height=52, width=147)

        self.five_btn = Button(self, text='5', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(5))
        self.five_btn.place(x=167, y=134, height=52, width=146)

        self.six_btn = Button(self, text='6', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(6))
        self.six_btn.place(x=323, y=134, height=52, width=147)

        self.seven_btn = Button(self, text='7', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(7))
        self.seven_btn.place(x=10, y=196, height=52, width=147)

        self.eight_btn = Button(self, text='8', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(8))
        self.eight_btn.place(x=167, y=196, height=52, width=146)

        self.nine_btn = Button(self, text='9', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(9))
        self.nine_btn.place(x=323, y=196, height=52, width=147)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFunHeight())
        self.clear_btn.place(x=10, y=258, height=52, width=147)

        self.zero_btn = Button(self, text='0', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(0))
        self.zero_btn.place(x=167, y=258, height=52, width=146)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.enterFunHeight(page_no))
        self.enter_btn.place(x=323, y=258, height=52, width=147)

    def clearFunHeight(self):
        textLen = len(self.txtVar.get())
        if textLen > 8:
            self.txtVar.set(self.txtVar.get()[:textLen-1])

    def enterFunHeight(self, page_no):
        self.patient_height.set(
            self.patient_height.get()+self.txtVar.get()[8:])
        print(self.patient_height.get())
        self.add_weight(page_no)

    def add_weight(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # 11 for fetch and 12 for new patients
        # current page no
        page_no = 124
        # 124 is for 12's fifth page i.e for weight
        print("In new patients page add height")
        self.txtVar = StringVar(value="Weight: ")

        # packing the frame
        # entry text
        self.entryText = Entry(self, textvariable=self.txtVar, font=(
            'Times New Roman', 20), border='3', width=27)
        self.entryText.place(x=8, y=8, height=56, width=464)

        self.one_btn = Button(self, text='1', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(1))
        self.one_btn.place(x=10, y=72, height=52, width=147)

        self.two_btn = Button(self, text='2', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(2))
        self.two_btn.place(x=167, y=72, height=52, width=146)

        self.three_btn = Button(self, text='3', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(3))
        self.three_btn.place(x=323, y=72, height=52, width=147)

        self.four_btn = Button(self, text='4', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(4))
        self.four_btn.place(x=10, y=134, height=52, width=147)

        self.five_btn = Button(self, text='5', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(5))
        self.five_btn.place(x=167, y=134, height=52, width=146)

        self.six_btn = Button(self, text='6', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(6))
        self.six_btn.place(x=323, y=134, height=52, width=147)

        self.seven_btn = Button(self, text='7', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(7))
        self.seven_btn.place(x=10, y=196, height=52, width=147)

        self.eight_btn = Button(self, text='8', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(8))
        self.eight_btn.place(x=167, y=196, height=52, width=146)

        self.nine_btn = Button(self, text='9', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(9))
        self.nine_btn.place(x=323, y=196, height=52, width=147)

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.clearFunHeight())
        self.clear_btn.place(x=10, y=258, height=52, width=147)

        self.zero_btn = Button(self, text='0', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.numFun(0))
        self.zero_btn.place(x=167, y=258, height=52, width=146)

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=(
            "Times New Roman", 25), command=lambda: self.enterFunWeight(page_no))
        self.enter_btn.place(x=323, y=258, height=52, width=147)

    # def clearFunWeight(self):
    #     textLen = len(self.txtVar.get())
    #     if textLen > 8:
    #         self.txtVar.set(self.txtVar.get()[:textLen-1])

    def enterFunWeight(self, page_no):
        self.patient_weight.set(
            self.patient_weight.get()+self.txtVar.get()[8:])
        print(self.patient_weight.get())
        # setting patient id
        date = datetime.datetime.now().strftime('%d-%m-%Y')
        curr_time = datetime.datetime.now().strftime('%H.%M.%S')
        self.PatientID_StrVar.set(self.PatientID_StrVar.get(
        )+self.patient_name.get()[6:]+"-"+date+"-"+curr_time)
        print(self.PatientID_StrVar.get())
        # making directory and saing data in folder with name  = self.PatientID_StrVar
        parent_dir = "patients_data/patients_details"
        personal_data = [self.PatientID_StrVar.get()[5:], self.patient_name.get()[6:], self.patient_age.get(
        )[5:], self.patient_gender.get()[8:], self.patient_height.get()[8:], self.patient_weight.get()[8:]]
        infoFileName = "{}.csv".format(self.PatientID_StrVar.get()[5:])
        completeName = os.path.join(parent_dir, infoFileName)
        file = open(completeName, 'w')
        for data in personal_data:
            file.write("{},".format(data))
        file.close()
        self.patient_details(page_no)

    def patient_details(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no
        page_no = 21
        print("In patient details page, page_no 21")
        # packing the frame
        self.pack(fill=BOTH, expand=1)

        # patient id label
        self.PID = Label(self, textvariable=self.PatientID_StrVar, font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.PID.place(x=10, y=50, width=460)

        # # patient name Label
        self.P_name = Label(self, textvariable=self.patient_name, font=(
            'Times New Roman', 22, "bold"), bg="white", anchor="w")
        self.P_name.place(x=10, y=90, width=470)

        # # patient age Label
        self.P_age = Label(self, textvariable=self.patient_age, font=(
            'Times New Roman', 22, "bold"), bg="white", anchor="w")
        self.P_age.place(x=10, y=145, width=220)

        # # patient gender Label
        self.P_gender = Label(self, textvariable=self.patient_gender, font=(
            'Times New Roman', 22, "bold"), bg="white", anchor="w")
        self.P_gender.place(x=250, y=145, width=210)

        # # patient height Label
        self.P_height = Label(self, textvariable=self.patient_height, font=(
            'Times New Roman', 22, "bold"), bg="white", anchor="w")
        self.P_height.place(x=10, y=200, width=220)

        # # patient weight Label
        self.P_weight = Label(self, textvariable=self.patient_weight, font=(
            'Times New Roman', 22, "bold"), bg="white", anchor="w")
        self.P_weight.place(x=250, y=200, width=210)

        # Next page button
        self.next_page1_btn = Button(self, text='Next', bg='LightBlue3', activebackground='LightBlue3',
                                     border='1', font=("Times New Roman", 17, 'bold'), command=lambda: self.all_images(page_no))
        self.next_page1_btn.place(x=323, y=260, width=146, height=55)

    def all_images(self, page_no):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no
        page_no = 1
        print("In all images, page_no 1")
        # packing the frame
        self.pack(fill=BOTH, expand=1)

        # left eye
        # le = left eye, re = right eye, rn = right nails, ln = left nails, mc = mucous, pl = palm
        self.left_eye_img = Button(
            self, border='1', bg="grey", command=lambda: self.camera_fun(page_no, 'le'))
        self.left_eye_img.place(x=10, y=10, width=146, height=100)
        if self.left_eye:
            self.left_eye_img['image'] = self.left_eye
        else:
            self.left_eye_img['text'] = 'Empty'
        self.left_eye_btn = Label(self, text='Left Eye', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.left_eye_btn.place(x=10, y=100, width=146, height=30)

        # right eye
        self.right_eye_img = Button(
            self, border='1', bg="grey", command=lambda: self.camera_fun(page_no, 're'))
        self.right_eye_img.place(x=166, y=10, width=146, height=100)
        if self.right_eye:
            self.right_eye_img['image'] = self.right_eye
        else:
            self.right_eye_img['text'] = 'Empty'
        self.right_eye_btn = Label(self, text='Right Eye', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.right_eye_btn.place(x=166, y=100, width=146, height=30)

        # mucous
        self.mucous_img = Button(
            self, border='1', bg="grey", command=lambda: self.camera_fun(page_no, 'mc'))
        self.mucous_img.place(x=322, y=10, width=146, height=100)
        if self.mucous:
            self.mucous_img['image'] = self.mucous
        else:
            self.mucous_img['text'] = 'Empty'
        self.mucous_btn = Label(self, text='Mucous', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.mucous_btn.place(x=322, y=100, width=146, height=30)

        # left nails
        self.left_nails_img = Button(
            self, border='1', bg="grey", command=lambda: self.camera_fun(page_no, 'ln'))
        self.left_nails_img.place(x=10, y=140, width=146, height=100)
        if self.left_nails:
            self.left_nails_img['image'] = self.left_nails
        else:
            self.left_nails_img['text'] = 'Empty'
        self.left_nails_btn = Label(self, text='Left Nails', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.left_nails_btn.place(x=10, y=240, width=146, height=30)

        # right nails
        self.right_nails_img = Button(
            self, border='1', bg="grey", command=lambda: self.camera_fun(page_no, 'rn'))
        self.right_nails_img.place(x=166, y=140, width=146, height=100)
        if self.right_nails:
            self.right_nails_img['image'] = self.right_nails
        else:
            self.right_nails_img['text'] = 'Empty'
        self.right_nails_btn = Label(self, text='Right Nails', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.right_nails_btn.place(x=166, y=240, width=146, height=30)

        # palm
        self.palm_img = Button(self, border='1', bg="grey",
                               command=lambda: self.camera_fun(page_no, 'pl'))
        self.palm_img.place(x=322, y=140, width=146, height=100)
        if self.palm:
            self.palm_img['image'] = self.palm
        else:
            self.palm_img['text'] = 'Empty'
        self.palm_btn = Label(self, text='Palm', font=(
            'Times New Roman', 22, "bold"), bg="white")
        self.palm_btn.place(x=322, y=240, width=146, height=30)

        # back button
        self.back = Button(self, text='Back', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.init_window(page_no))
        self.back.place(x=10, y=280, width=146, height=38)

        # save button
        self.save_btn = Button(self, text='Save', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.save_data(page_no))
        self.save_btn.place(x=322, y=280, width=146, height=38)

    def save_data(self, page_no):
        self.remove_widgets(page_no)
        # current page no
        # page_no = 4

        # setting up data
        parent_dir = "patients_data"
        if self.left_eye:
            path = os.path.join(parent_dir, "left_eye_images")
            imgName = "left_eye_{}".format(self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)

        if self.right_eye:
            path = os.path.join(parent_dir, "right_eye_images")
            imgName = "right_eye_{}".format(
                self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)

        if self.mucous:
            path = os.path.join(parent_dir, "mucous_images")
            imgName = "mucous_{}".format(
                self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)

        if self.right_nails:
            path = os.path.join(parent_dir, "right_nails_images")
            imgName = "right_nails_{}".format(
                self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)

        if self.left_nails:
            path = os.path.join(parent_dir, "left_nails_images")
            imgName = "left_nails_{}".format(
                self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)

        if self.palm:
            path = os.path.join(parent_dir, "palm_images")
            imgName = "palm_{}".format(
                self.PatientID_StrVar.get()[5:])
            filename = '{}.jpg'.format(imgName)
            # image = np.ndarray(self.left_eye)
            # self.rgb_frame = cv2.cvtColor(self.rgb_frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(path, filename), self.rgb_frame)
        # self.barcode_page(page_no)
        self.init_window(page_no)

    def barcode_page(self, page_no):
        self.remove_widgets(page_no)
        # current page no;
        page_no = 4

        # packing the frame
        data = str(self.PatientID_StrVar.get()[5:])
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(data, writer=ImageWriter())
        self.barcode_label = Label(self, image=ean, font=(
            'Times New Roman', 22, "bold"), bg="grey")
        self.next_page2_btn.place(x=100, y=50, width=280, height=100)
        Label(self, text="Barcode for patient", font=('Times New Roman', 22)).place(
            x=100, y=160, width=280, height=50)
        self.init_window(page_no)

    def camera_fun(self, page_no, image_type):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no
        page_no = 2
        print("In camera function, page_no 2")
        # packing the frame
        # self.pack(fill=BOTH, expand=1) y=320 X x=480

        # adding label to show video frame
        # self.frame = None

        # harr cascading
        # self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.vid_frame = Frame(self, bg='grey')
        self.vid_frame.place(x=10, y=10, width=460, height=245)
        self.video_label = Label(self.vid_frame)
        self.video_label.place(x=10, y=10, width=460, height=245)

        self.video_thread = True
        self.vs = WebcamVideoStream(src=0).start()
        print(type(self.vs))
        time.sleep(0.5)
        self.thread_lock = threading.Lock()

        # image label
        # self.img_label = Label(self)

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
            # self.img_label['text'] = "Left Eye"
            # self.img_label.place(x=0, y=0, width=310, height=40)

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
        time.sleep(0.5)
        self.v_thread.start()

    def videoLoop(self):
        self.top_left = (200, 200)
        self.bottom_right = (400, 300)
        self.color = (0, 255, 0)
        self.thickness = 2
        while self.video_thread:
            self.frame = self.vs.read()
            self.frame = cv2.flip(self.frame, 1)
            self.frame = cv2.rectangle(
                self.frame, self.top_left, self.bottom_right, self.color, self.thickness)
            if self.frame is not None:
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.rgb_frame = self.image
            # cv2.imwrite( 'pic.jpg', self.rgb_frame)
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            self.thread_lock.acquire()
            self.video_label.configure(image=self.image)
            self.video_label.image = self.image
            self.thread_lock.release()
        self.vs.stop()

    def video_close(self):
        # print("\nvideo close");
        self.eye_video_thread = False

    def snapshot(self, page_no, image_type):
        self.remove_widgets(page_no)
        self.stop_date_time()
        # current page no is 3
        page_no = 3
        print(self.vs)
        # self.vs.stream.release()

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
            self.right_eye = self.snapshot_taken

        if image_type == 'ln':
            self.left_nails = self.snapshot_taken

        if image_type == 'rn':
            self.right_nails = self.snapshot_taken

        if image_type == 'mc':
            self.mucous = self.snapshot_taken

        if image_type == 'pl':
            self.palm = self.snapshot_taken

        # retake button
        self.retake = Button(self, text='Retake', font=(
            'Times New Roman', 22, "bold"), bg="LightBlue3", command=lambda: self.camera_fun(page_no, image_type))
        self.retake.place(x=166, y=265, width=146, height=50)

        return

    def remove_widgets(self, page_no):
        if page_no == 0:
            # self.next_page1_btn.place_forget()
            self.add_p_btn.place_forget()
            # self.fetch_btn.place_forget()
            # self.PID.place_forget()
            self.time_l.place_forget()
            self.date_l.place_forget()
            # self.P_age.place_forget()
            # self.P_gender.place_forget()
            # self.P_height.place_forget()
            # self.P_weight.place_forget()
            # self.P_name.place_forget()
            self.upload_btn.place_forget()
            self.power_btn.place_forget()
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
            self.save_btn.place_forget()
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

        if page_no == 21:
            self.next_page1_btn.place_forget()
            self.next_page1_btn.place_forget()
            self.PID.place_forget()
            self.P_age.place_forget()
            self.P_gender.place_forget()
            self.P_height.place_forget()
            self.P_weight.place_forget()
            self.P_name.place_forget()
            print("Detail's page widgets removed")

        if page_no == 3:
            self.snapshot_label.place_forget()
            self.back_to_1.place_forget()
            self.retake.place_forget()
            self.next_page1_btn.place_forget()
            print("Wdigets on snapshot, page 3, removed")

        if page_no == 11:
            self.enter_btn.place_forget()
            self.clear_btn.place_forget()
            self.entryText.place_forget()
            self.shift_btn.place_forget()
            self.one_btn.place_forget()
            self.two_btn.place_forget()
            self.three_btn.place_forget()
            self.four_btn.place_forget()
            self.five_btn.place_forget()
            self.six_btn.place_forget()
            self.seven_btn.place_forget()
            self.eight_btn.place_forget()
            self.nine_btn.place_forget()
            self.zero_btn.place_forget()
            self.underscore_btn.place_forget()
            self.dot_btn.place_forget()
            print("widgets removed from fetching page")

        if page_no == 12:
            self.entryText.place_forget()
            self.clear_btn.place_forget()
            self.shift_btn.place_forget()
            self.enter_btn.place_forget()
            self.z_btn.place_forget()
            self.y_btn.place_forget()
            self.x_btn.place_forget()
            self.w_btn.place_forget()
            self.v_btn.place_forget()
            self.u_btn.place_forget()
            self.t_btn.place_forget()
            self.s_btn.place_forget()
            self.r_btn.place_forget()
            self.q_btn.place_forget()
            self.p_btn.place_forget()
            self.o_btn.place_forget()
            self.n_btn.place_forget()
            self.m_btn.place_forget()
            self.l_btn.place_forget()
            self.k_btn.place_forget()
            self.j_btn.place_forget()
            self.i_btn.place_forget()
            self.h_btn.place_forget()
            self.g_btn.place_forget()
            self.f_btn.place_forget()
            self.e_btn.place_forget()
            self.d_btn.place_forget()
            self.c_btn.place_forget()
            self.b_btn.place_forget()
            self.a_btn.place_forget()
            print("widgets on fetching removed")

        if page_no == 120:
            self.enter_btn.place_forget()
            self.clear_btn.place_forget()
            self.z_btn.place_forget()
            self.y_btn.place_forget()
            self.x_btn.place_forget()
            self.w_btn.place_forget()
            self.v_btn.place_forget()
            self.u_btn.place_forget()
            self.t_btn.place_forget()
            self.s_btn.place_forget()
            self.r_btn.place_forget()
            self.q_btn.place_forget()
            self.p_btn.place_forget()
            self.o_btn.place_forget()
            self.n_btn.place_forget()
            self.m_btn.place_forget()
            self.l_btn.place_forget()
            self.k_btn.place_forget()
            self.j_btn.place_forget()
            self.i_btn.place_forget()
            self.h_btn.place_forget()
            self.g_btn.place_forget()
            self.f_btn.place_forget()
            self.e_btn.place_forget()
            self.d_btn.place_forget()
            self.c_btn.place_forget()
            self.b_btn.place_forget()
            self.a_btn.place_forget()
            self.entryText.place_forget()
            print("widgets on add new patients name removed")

        if page_no == 121:
            self.entryText.place_forget()
            self.clear_btn.place_forget()
            self.enter_btn.place_forget()
            self.one_btn.place_forget()
            self.two_btn.place_forget()
            self.three_btn.place_forget()
            self.four_btn.place_forget()
            self.five_btn.place_forget()
            self.six_btn.place_forget()
            self.seven_btn.place_forget()
            self.eight_btn.place_forget()
            self.nine_btn.place_forget()
            self.zero_btn.place_forget()
            print("widgets removed from add age page")

        if page_no == 122:
            self.entryText.place_forget()
            self.male_btn.place_forget()
            self.female_btn.place_forget()
            self.others_btn.place_forget()
            self.clear_btn.place_forget()
            self.enter_btn.place_forget()

        if page_no == 123:
            self.entryText.place_forget()
            self.clear_btn.place_forget()
            self.enter_btn.place_forget()
            self.one_btn.place_forget()
            self.two_btn.place_forget()
            self.three_btn.place_forget()
            self.four_btn.place_forget()
            self.five_btn.place_forget()
            self.six_btn.place_forget()
            self.seven_btn.place_forget()
            self.eight_btn.place_forget()
            self.nine_btn.place_forget()
            self.zero_btn.place_forget()
            print("widgets removed from add height page")

        if page_no == 124:
            self.entryText.place_forget()
            self.clear_btn.place_forget()
            self.enter_btn.place_forget()
            self.one_btn.place_forget()
            self.two_btn.place_forget()
            self.three_btn.place_forget()
            self.four_btn.place_forget()
            self.five_btn.place_forget()
            self.six_btn.place_forget()
            self.seven_btn.place_forget()
            self.eight_btn.place_forget()
            self.nine_btn.place_forget()
            self.zero_btn.place_forget()
            print("widgets removed from add weight page")


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
