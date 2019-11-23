#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Roberto C."
__copyright__ = "Copyright (C) 2019. RC"
__license__ = "Private Domain"
__version__ = "1.0"
import picamera,io,time
import Tkinter as tk
import ttk as ttk
import sys as sys
#from PIL import *
class splashScreen(tk.Frame):
	def __init__(self,master): 
		tk.Frame.__init__(self,master)
		self.master = master
		self.master.overrideredirect(True)
		self.width = self.master.winfo_screenwidth()
		self.height = self.master.winfo_screenheight()
		self.master.geometry("{0}x{1}+{2}+{3}".format(self.width/4,self.height/4,self.width/3,self.height/3))	 
		self.logo_image = tk.PhotoImage(file="icons/logo.png").subsample(20)
		self.logo_canvas= tk.Canvas(self.master,height=self.height/4-20,width=self.width/4,bg="white")
		self.logo_canvas.create_image(175,120,image=self.logo_image)
		self.logo_canvas.pack()
		self.versionerBottom_frame = tk.Frame(self.master)
		self.versionerBottom_frame.pack()
		self.versioner_label = tk.Label(self.versionerBottom_frame,text="v1.0")
		self.versioner_label.pack(side=tk.RIGHT)
		
class educascopeApp(tk.Frame): 
	global photoFlag
	global videoFlag
	global configFlag
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		self.master = master
		self.w = self.master.winfo_screenwidth()
		self.h = self.master.winfo_screenheight() 
		self.camera = picamera.PiCamera() 
		self.photoFlag = False
		self.videoFlag = False	
		self.configFlag = False
		self.initGUI()
		self.initGUIComponents()
		self.initCamera()
	def quit(self):
		self.master.destroy()
	def initGUI(self):
		#self.master.overrideredirect(True)
		self.master.title("Educascope Menu")
		self.master.geometry("{0}x{1}+0+0".format(self.w/4,self.h))	
	def initGUIComponents(self): 
		self.mainFrame = tk.Frame(self.master,bg="white")
		self.mainFrame.pack(fill=tk.BOTH,expand=True)
		self.logoFrame = tk.Frame(self.mainFrame,bg="white")
		self.logoFrame.pack(pady=5)
		self.logoImage = tk.PhotoImage(file="icons/logo.png").subsample(20)
		self.logoLabel = tk.Label(self.logoFrame,image=self.logoImage,bg="white").pack()
		self.multimediaFrame = tk.Frame(self.mainFrame,bg="White")
		self.multimediaFrame.pack()
		self.photoButtonImage = tk.PhotoImage(file="icons/pictureIcon.png").subsample(2)
		self.photoButton = tk.Button(self.multimediaFrame,image=self.photoButtonImage,command=self.photoMenu,bg="white",activebackground="white",relief=tk.GROOVE)
		self.photoButton.pack(pady=5)
		self.videoButtonImage = tk.PhotoImage(file="icons/videoIcon.png").subsample(2)
		self.videoButton = tk.Button(self.multimediaFrame,image=self.videoButtonImage,command=self.videoMenu,bg="white",activebackground="white",relief=tk.GROOVE)
		self.videoButton.pack(pady=5)
		self.configButtonImage = tk.PhotoImage(file="icons/configIcon.png").subsample(8)
		self.configButton = tk.Button(self.multimediaFrame,image=self.configButtonImage,command=self.configMenu,bg="white",activebackground="white",relief=tk.GROOVE)
		self.configButton.pack(pady=10)
		self.photoFrame = tk.Frame(self.mainFrame,bg="white")
		self.filenameFrame = tk.Frame(self.photoFrame,bg="white")
		self.filenameFrame.pack(pady=5)
		self.labelFN = tk.StringVar()
		self.filenameLabel = tk.Label(self.filenameFrame,bg="white",textvariable=self.labelFN).pack()
		self.filenameEBFrame = tk.Frame(self.filenameFrame,bg="white")
		self.filenameEBFrame.pack()
		self.filenameEntry = tk.Entry(self.filenameEBFrame)
		self.filenameEntry.pack(side=tk.LEFT,padx=10)
		self.filenameSaveButton = tk.Button (self.filenameEBFrame,text="Guardar",command=self.saveFile,width=5)
		self.filenameSaveButton.pack(side=tk.RIGHT)
		self.videoOptionFrame = tk.Frame(self.mainFrame,bg="white")
		self.timeVideoLabel = tk.Label(self.videoOptionFrame,text="Tiempo (s)",bg="white")
		self.timeVideoLabel.pack(side=tk.LEFT)
		self.timeVideoBox = ttk.Combobox(self.videoOptionFrame,values=[5,15,30,45,60])
		self.timeVideoBox.current(0)
		self.timeVideoBox.pack(padx=5,side=tk.RIGHT,pady=5)
		self.configFrame = tk.Frame(self.mainFrame,bg="white")
		self.configImageMenuLabel = tk.Label(self.configFrame,text="Ajustes de imágen",bg="white")
		self.configImageMenuLabel.pack(side=tk.LEFT,pady=10,padx=5)
		self.defaultAdjustButton = tk.Button(self.configFrame,text="Predeterminados",command=self.setDefaultAdjust)
		self.defaultAdjustButton.pack(side=tk.RIGHT)
		self.configImageFrame = tk.Frame(self.mainFrame,bg="white")
		self.brightnessFrame = tk.Frame(self.configImageFrame,bg="white")
		self.brightnessFrame.pack() 
		self.brightnessLabel = tk.Label(self.brightnessFrame,text="Brillo",bg="white")
		self.brightnessLabel.pack(side=tk.TOP)
		self.brightnessScale = tk.Scale(self.brightnessFrame,orient=tk.HORIZONTAL,from_=0,to=100,command=self.setBrightness,showvalue=False,resolution=1.0)
		self.brightnessScale.set(50)
		self.brightnessScale.pack(side=tk.LEFT)
		self.brightnessPercent = tk.Label(self.brightnessFrame,text="50",bg="white")
		self.brightnessPercent.pack(side=tk.RIGHT)
		self.contrastFrame = tk.Frame(self.configImageFrame,bg="white")
		self.contrastFrame.pack() 
		self.contrastLabel = tk.Label(self.contrastFrame,text="Contraste",bg="white")
		self.contrastLabel.pack(side=tk.TOP)
		self.contrastScale = tk.Scale(self.contrastFrame,orient=tk.HORIZONTAL,from_=-100,to=100,command=self.setContrast,showvalue=False,resolution=1.0)
		self.contrastScale.set(0)
		self.contrastScale.pack(side=tk.LEFT)
		self.contrastPercent = tk.Label(self.contrastFrame,text="0",bg="white")
		self.contrastPercent.pack(side=tk.RIGHT) 
		self.saturationFrame = tk.Frame(self.configImageFrame,bg="white")
		self.saturationFrame.pack() 
		self.saturationLabel = tk.Label(self.saturationFrame,text="Saturación",bg="white")
		self.saturationLabel.pack(side=tk.TOP)
		self.saturationScale = tk.Scale(self.saturationFrame,orient=tk.HORIZONTAL,from_=-100,to=100,command=self.setSaturation,showvalue=False,resolution=1.0)
		self.saturationScale.set(0)
		self.saturationScale.pack(side=tk.LEFT)
		self.saturationPercent = tk.Label(self.saturationFrame,text="0",bg="white")
		self.saturationPercent.pack(side=tk.RIGHT) 
		self.sharpnessFrame = tk.Frame(self.configImageFrame,bg="white")
		self.sharpnessFrame.pack() 
		self.sharpnessLabel = tk.Label(self.sharpnessFrame,text="Nitidez",bg="white")
		self.sharpnessLabel.pack(side=tk.TOP)
		self.sharpnessScale = tk.Scale(self.sharpnessFrame,orient=tk.HORIZONTAL,from_=-100,to=100,command=self.setSharpness,showvalue=False,resolution=1.0)
		self.sharpnessScale.set(0)
		self.sharpnessScale.pack(side=tk.LEFT)
		self.sharpnessPercent = tk.Label(self.sharpnessFrame,text="0",bg="white")
		self.sharpnessPercent.pack(side=tk.RIGHT)
		self.zoomFrame = tk.Frame(self.configImageFrame,bg="white")
		self.zoomFrame.pack()
		self.zoomLabel = tk.Label(self.zoomFrame,text="Zoom",bg="white")
		self.zoomLabel.pack(side=tk.TOP)
		self.zoom1Frame = tk.Frame(self.zoomFrame,bg="white")
		self.zoom1Frame.pack()
		self.zoom1Scale = tk.Scale(self.zoom1Frame,orient=tk.HORIZONTAL,from_=0,to=0.9,command=self.setZoomXY,showvalue=False,resolution=0.1)
		self.zoom1Scale.set(0)
		self.zoom1Scale.pack(side=tk.LEFT)
		self.zoom1Percent = tk.Label(self.zoom1Frame,text="0.0",bg="white")
		self.zoom1Percent.pack(side=tk.RIGHT,pady=10)
		self.zoom2Frame = tk.Frame(self.zoomFrame,bg="white")
		self.zoom2Frame.pack()
		self.zoom2Scale = tk.Scale(self.zoom2Frame,orient=tk.HORIZONTAL,from_=0.2,to=1,command=self.setZoomWH,showvalue=False,resolution=0.1)
		self.zoom2Scale.set(1)
		self.zoom2Scale.pack(side=tk.LEFT)
		self.zoom2Percent = tk.Label(self.zoom2Frame,text="1.0",bg="white")
		self.zoom2Percent.pack(side=tk.RIGHT,pady=10)
		self.closeFrame = tk.Frame(self.mainFrame,bg="white")
		self.closeFrame.pack()
		self.closeButton = tk.Button(self.closeFrame,text="CERRAR",command=self.quit,bg="red",fg="white",activeforeground="white",activebackground="red")
		self.closeButton.pack(side=tk.TOP,pady=5)

	def photoMenu(self):
		if (self.photoFlag is False):
			self.configFrame.pack_forget()
			self.configImageFrame.pack_forget()
			self.configFlag = False
			self.labelFN.set("Nombre de la imágen")
			self.videoOptionFrame.pack_forget()
			self.closeFrame.pack_forget()
			self.photoFrame.pack()
			self.closeFrame.pack()
			self.photoFlag = True
			self.videoFlag = False
		elif (self.photoFlag is True):
			self.photoFrame.pack_forget()
			self.photoFlag = False
			self.videoFlag = False
	
	def videoMenu(self):
		if (self.videoFlag is False):
			self.configFrame.pack_forget()
			self.configImageFrame.pack_forget()
			self.configFlag = False 
			self.labelFN.set("Nombre del video")
			self.closeFrame.pack_forget()
			self.photoFrame.pack()
			self.videoOptionFrame.pack()
			self.closeFrame.pack()
			self.videoFlag = True
			self.photoFlag = False
		elif (self.videoFlag is True):
			self.photoFrame.pack_forget()
			self.videoOptionFrame.pack_forget()
			self.videoFlag = False
			self.photoFlag = False
	
	def configMenu(self):
		if (self.configFlag is False):
			self.photoFrame.pack_forget()
			self.videoOptionFrame.pack_forget()
			self.closeFrame.pack_forget()
			self.configFrame.pack()
			self.configImageFrame.pack()
			self.closeFrame.pack()
			self.configFlag = True
			self.videoFlag = False
			self.photoFlag = False
		elif (self.configFlag is True):
			self.configFrame.pack_forget()
			self.configImageFrame.pack_forget()
			self.configFlag = False
			self.videoFlag = False
			self.photoFlag = False
	
	def saveFile(self):
		dateText = str(time.strftime("%d%m%y"))
		timeText = str(time.strftime("%H%M%S"))
		self.strName = self.filenameEntry.get()
		if self.photoFlag is True:
			filename = "img/" + self.strName + "_" + dateText + "_" +  timeText + ".jpg"
			self.camera.capture(filename)
			self.filenameEntry.delete(0,tk.END)
			self.photoFlag = False
		elif self.videoFlag is True:
			filename = "video/" + self.strName + "_" + dateText + "_" + timeText + ".h264"
			self.camera.start_recording(filename)
			stay = float(self.timeVideoBox.get())
			self.camera.wait_recording(stay)
			self.camera.stop_recording()
			self.filenameEntry.delete(0,tk.END)
			self.videoFlag = False 
	def addLabelImg(self):
		text = self.textAddEntry.get()
		self.camera.annotate_text = text 
		self.textAddEntry.delete(0,END)
			
	def setBrightness(self,brightness):
		self.brightness = int(float(brightness))
		self.brightnessPercent.config(text=self.brightness)
		self.camera.brightness = self.brightness
	
	def setContrast(self,contrast):
		self.contrast = int(float(contrast))
		self.contrastPercent.config(text=self.contrast)
		self.camera.contrast = self.contrast
		
	def setSaturation(self,saturation):
		self.saturation = int(float(saturation))
		self.saturationPercent.config(text=self.saturation)
		self.camera.saturation = self.saturation
		
	def setSharpness(self,sharpness):
		self.sharpness = int(float(sharpness))
		self.sharpnessPercent.config(text=self.sharpness)
		self.camera.sharpness = self.sharpness
		
	def setZoomXY(self,value):
		self.value1 = self.zoom1Scale.get()
		self.value2 = self.zoom2Scale.get()
		self.zoom1Percent.config(text=self.value1) 
		self.zoom2Percent.config(text=self.value2)
		self.camera.crop = (float(self.value1),float(self.value1),float(self.value2),float(self.value2))
	
	def setZoomWH(self,value):
		self.value1 = self.zoom1Scale.get()
		self.value2 = self.zoom2Scale.get()
		self.zoom1Percent.config(text=self.value1) 
		self.zoom2Percent.config(text=self.value2)
		self.camera.crop = (float(self.value1),float(self.value1),float(self.value2),float(self.value2)) 
		
	def initCamera(self):
		self.camera.preview_fullscreen=False
		self.camera.preview_window=(self.w/4,0,self.w, self.h)
		self.camera.resolution=(self.w,self.h)
		self.camera.start_preview()  
	
	def setDefaultAdjust(self):
		self.camera.brightness = 50
		self.brightnessScale.set(50)
		self.brightnessPercent.config(text="50")
		self.camera.contrast = 0
		self.contrastScale.set(0)
		self.contrastPercent.config(text="0")
		self.camera.saturation = 0
		self.saturationScale.set(0)
		self.saturationPercent.config(text="0")
		self.camera.sharpness = 0
		self.sharpnessScale.set(0)
		self.sharpnessPercent.config(text="0")
		self.zoom1Scale.set(0)
		self.zoom1Percent.config(text="0.0")
		self.zoom2Scale.set(1)
		self.zoom2Percent.config(text="1.0")
		self.camera.crop = (0.0,0.0,1.0,1.0)
	
if __name__ == "__main__":
	root = tk.Tk()
	previous = splashScreen(root)
	previous.after(3500,root.destroy)
	previous.mainloop()
	main = tk.Tk()
	app = educascopeApp(main)
	app.mainloop()
