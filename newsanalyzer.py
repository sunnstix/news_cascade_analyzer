import zipfile
from zipfile import ZipFile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
from progress import ProgressBar
import math
        

class NewsAnalyzer:
    # loading the face detection classifier
    face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
    
    def __init__(self,fileName):
        print('Initializing Classification of '+fileName)
        self.imageList = self.unzipImages(fileName)
        self.detect()
        print('Done Analyzing {}'.format(fileName))
        
    def unzipImages(self,zipFile):
        #Create list of dictionaries to fill with fileName, image objects, word information and
        #bounding boxes and initially populate with image and fileName data from ZipFile
        print('Extracting Images:')
        images = []
        with ZipFile('readonly/'+zipFile,'r') as zipF:
            bar = ProgressBar(len(zipF.infolist()))
            for item in zipF.infolist():
                bar.update()
                bar.iterate()
                with zipF.open(item) as imageFile:
                    image = Image.open(imageFile)
                    images.append({'fileName':item.filename,'img':image.convert('RGB')})
            bar.complete()
        return images
    
    def detect(self):
        #Detect words and faces in imageList using OpenCV and tesseract and populate with strings 
        #and bounding box data - also creates a progress bar
        print('Detecting Text and Faces:')
        bar = ProgressBar(len(self.imageList))
        for imageData in self.imageList:
            bar.update()
            bar.iterate()
            grayscaleImage = cv.cvtColor(np.array(imageData['img']),cv.COLOR_BGR2GRAY)
            faceBoxes = self.face_cascade.detectMultiScale(grayscaleImage,1.3, 5)
            imageData['faceBox'] = faceBoxes
            txt = pytesseract.image_to_string(imageData['img'])
            imageData['text'] = txt
        bar.complete()
    
    def getFace(self,img,faceBox,imageSize):
        x,y,width,height = faceBox
        faceImg = img.crop((x,y,x+width,y+height))
        faceImg.thumbnail(imageSize,Image.ANTIALIAS)
        return faceImg
    
    def search(self,keyword,imageSize = (100,100),numCol = 5):
        print('Results for Search Query "{}":'.format(keyword))
        found = False
        for imageData in self.imageList:
            if keyword not in imageData['text']: 
                continue
            found = True
            print('Result found in file '+imageData['fileName']+':')
            if len(imageData['faceBox'])==0: 
                print('No faces found')
                continue
            numRow = math.ceil(len(imageData['faceBox'])/numCol)
            canvas = Image.new(imageData['img'].mode,(numCol*imageSize[0],numRow * imageSize[1]))
            currRow,currCol = (0,0)
            for faceBox in imageData['faceBox']:
                canvas.paste(self.getFace(imageData['img'],faceBox,imageSize),(currCol*imageSize[0],currRow*imageSize[1]))
                currCol+=1
                if(currCol>=numCol):
                    currCol = 0
                    currRow+=1
            canvas.show()
        if not found: print('No results for this word\n')
