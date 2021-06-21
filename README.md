
# Welcome to my final project!

I tried to do a little more than neccessary to practice my python skills so you may notice that throughout this project I use classes. It was actually very convenient to represent the data on each set of zipped news files as objects because calculating the necessary data for each zipped file took a VERY long time. By making them objects I can now just modify my search queries without waiting long at all.

Also since many of the actions took extended periods of times I thought it would be really nice if I could be able to vizualize the progress of each step of the image analysis process so I created a small class called ProgressBar which I use throughout my main class to provide some debugging information. I made it a bit modular in case I decide to reuse the bit of code in a future endeavor.

## Progress Bar Class:


```python
import math
import sys

#Create a Progress Bar to Illustrate Progress of Different Things - Modular and Reusable
class ProgressBar:
    def __init__(self,totalActions,bar_char='▱',bar_len = 20):
        self.bar_char = bar_char
        self.bar_len = bar_len
        self.totalActions = totalActions
        self.doneActions = 0
    def update(self):
        displayLen = math.floor((self.doneActions/self.totalActions)*self.bar_len)
        displayedBar = self.bar_char * displayLen + ' ' * (self.bar_len - displayLen)
        percentage = str(math.floor(self.doneActions/self.totalActions*100))
        sys.stdout.write('\r\tProgress: {}% ({}/{}) Complete [{}]'.format(percentage,str(self.doneActions),str(self.totalActions),displayedBar))
        sys.stdout.flush()
    def iterate(self):
        if self.doneActions<self.totalActions:
            self.doneActions+=1
    def complete(self):
        displayedBar = self.bar_char * self.bar_len
        sys.stdout.write('\r\tProgress: {}% ({}/{}) Complete [{}]\n'.format('100',str(self.totalActions),str(self.totalActions),displayedBar))
        sys.stdout.flush()
```

## NewsAnalyzer Class:


```python
import zipfile
from zipfile import ZipFile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
        

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
            display(canvas)
        if not found: print('No results for this word')

```

## Small_img.zip Analysis:
Below I have an example of me running the code on the sample. However, this code could be run on any number of zipped files with images. Note how creating an object is quite convenient as I can now just call the search method on it multiple times with very fast results.

I'm also a big fan of the progress bars which move as you run the code (Feel free to run the code if you would like)


```python
small = NewsAnalyzer('small_img.zip')
```

    Initializing Classification of small_img.zip
    Extracting Images:
    	Progress: 100% (4/4) Complete [▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱]
    Detecting Text and Faces:
    	Progress: 100% (4/4) Complete [▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱]
    Done Analyzing small_img.zip



```python
small.search('Christopher')
print()
small.search('dog')
print()
small.search('Michigan')
```

    Results for Search Query "Christopher":
    Result found in file a-0.png:



![png](output_7_1.png)


    Result found in file a-3.png:



![png](output_7_3.png)


    
    Results for Search Query "dog":
    No results for this word
    
    Results for Search Query "Michigan":
    Result found in file a-0.png:



![png](output_7_5.png)


    Result found in file a-1.png:



![png](output_7_7.png)


    Result found in file a-2.png:



![png](output_7_9.png)


    Result found in file a-3.png:



![png](output_7_11.png)

