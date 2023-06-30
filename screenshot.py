import cv2
import os
import numpy as np

def remove_adjacent(nums):
    '''From an input list, removes an 
       entry if they are sequential'''
    i = 1
    while i < len(nums):    
        #print(nums[i], nums[i-1])
        if nums[i] == (nums[i-1] + 1):
            nums.pop(i)
            i -= 1  
        i += 1
    return nums

class Screenshot():
    def __init__(self, screenshot_path):
        self.screenshot_path = screenshot_path
        self.basename = os.path.splitext(os.path.basename(self.screenshot_path))[0]
        
        #Read image into CV2 Image Objects
        self.img = cv2.imread(screenshot_path)
        self.img_orig = self.img.copy()

        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.bw = cv2.threshold(self.gray, 250, 255, cv2.THRESH_BINARY)[1]
        self.bw_inv = cv2.threshold(self.gray, 250, 255, cv2.THRESH_BINARY_INV)[1]

    #STEP 1 - CROP
    def crop(self, upper_pixel:int=128, lower_pixel:int=168, left_pixel:int=130):
        '''Read in the screenshot and crop out the top, bottom, and album art from the left'''
        self.img = self.img[upper_pixel:-lower_pixel, left_pixel:]  #Crop image ([y1:y2, x1:x2])
        self.gray = self.gray[upper_pixel:-lower_pixel, left_pixel:]
        self.bw = self.bw[upper_pixel:-lower_pixel, left_pixel:]
        self.bw_inv = self.bw_inv[upper_pixel:-lower_pixel, left_pixel:]

    #STEP 2 - FIND HOIZONTAL SEPERATORS IN CROPPED IMAGES
    def find_seperators(self):
        '''Detects the pixel positions of the horizontal seperators present in the screenshots'''

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        detect_horizontal = cv2.morphologyEx(self.bw_inv, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        #Get vertical indicies that lines are at
        lines = detect_horizontal.sum(axis=1)  #Find horisontal line locations
        indicies = np.nonzero(lines)[0]
        indicies = np.array(remove_adjacent(list(indicies)))
        if indicies[0] > 50:
            indicies = np.concatenate([np.array([0]),indicies ]) #Add an initial row if it doesn't exist   
        self.seperators = indicies

    #STEP 3 - PARTITION INTO SMALLER IMAGES BASED ON HORIZONTAL SEPERATORS
    def partition(self):
        partitioned_imgs = []
        previous_index = self.seperators[0]
        for index in self.seperators[1:]:
            result_cropped = self.bw[previous_index:index,:]
            partitioned_imgs.append(result_cropped)
            previous_index = index
        self.partitioned_imgs = partitioned_imgs

    #STEP 4 - WRITE PARTITIONED IMAGES TO A DIRECTORY
    def write_partitions(self, out_dir):
        '''Writes partitioned Images to a directory'''
        for num, img in enumerate(self.partitioned_imgs):
            cv2.imwrite(os.path.join(out_dir, f"{self.basename}_{num}.jpg"), img)
       