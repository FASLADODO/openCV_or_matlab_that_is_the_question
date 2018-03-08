import numpy as np
import cv2
import time

class subtractor:
    """description of class"""
    def __init__(self, filepath, type='knn', showfps=False, masksource=False, saveVid=False, framerate=25, outname="video.avi", **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        self.type = type
        self.showfps = showfps
        self.saveVid = saveVid
        self.outname = outname
        self.framerate = framerate
        self.masksource = masksource
        
    def createDetector(self):
        self.capture = cv2.VideoCapture(self.filepath)
        if (self.type == 'knn'):
            self.fgbg = cv2.createBackgroundSubtractorKNN()
        elif (self.type == 'mog2'):
            self.fgbg = cv2.createBackgroundSubtractorMOG2()
    
    def writeVid(self, dim):
        self.out = cv2.VideoWriter(self.outname, cv2.VideoWriter_fourcc(*'XVID'), self.framerate, dim)

    def pad_channels(self, img):
        w_, h_ = img.shape
        i_ = np.empty((w_, h_, 3), dtype=np.uint8)
        i_[:,:,0] = img
        i_[:,:,1] = img
        i_[:,:,2] = img
        return i_

    def end(self):
        if(self.saveVid):
            self.out.release()
        self.capture.release()
        cv2.destroyAllWindows()

    def showMask(self, saveVideo='false'):
        self.createDetector()
        if(self.saveVid):
            _, f_ = self.capture.read()
            x, y, _ = f_.shape
            self.writeVid((x,y))
            
            '''
            fo_ = self.fgbg.apply(f_)
            fo_ = self.pad_channels(fo_)
            print(fo_[:,:,1])
            fo_[fo_ > 1] = 1
            arr_ = np.unique(fo_)
            for i in arr_:
                print(i, )
            '''
        
        while(self.capture.isOpened()):
            startTime = time.time()
            ret, frame = self.capture.read()
            foremask = self.fgbg.apply(frame)
            if(self.masksource):
                foremask = self.pad_channels(foremask)
                foremask[foremask <120] = 0
                foremask = np.bitwise_and(frame, foremask)
                
            if(ret):
                h_, w_, c_ = frame.shape
                foremask = cv2.putText(foremask, 'Using {}'.format(self.type),
                                      (10, 50), cv2.FONT_HERSHEY_COMPLEX,
                                      1, [200, 20, 254], 2)
                
                if(self.showfps):
                    fps = 1.0/(time.time()-startTime)
                    foremask = cv2.putText(foremask, ("Framerate: {:.2f}".format(fps)),
                                       (int(w_/2) + int(w_/4), h_ - int(h_/10)), cv2.FONT_HERSHEY_COMPLEX,
                                       1, [200, 20, 254], 2)

                cv2.imshow('frame', foremask)
                if(self.saveVid):
                    self.out.write(foremask)
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    break
            else:
                self.end()
                break
        