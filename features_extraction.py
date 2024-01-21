import os
import cv2
import numpy as np
import math

def bilateralFilter(image, d):
    image = cv2.bilateralFilter(image,d,50,50)
    return image

def medianFilter(image, d):
    image = cv2.medianBlur(image,d)
    return image

def threshold(image, t):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,image = cv2.threshold(image,t,255,cv2.THRESH_BINARY_INV)
    return image

def gaussianblur(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3,3), 0)
    return image

def dilate(image, kernalSize):
    kernel = np.ones(kernalSize, np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    return image

def cannyedge(image,x,y):
    image = cv2.Canny(image, x, y)    
    return image
    
def erode(image, kernalSize):
    kernel = np.ones(kernalSize, np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    return image

def resize(image, width, height):
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized

def horizontalProjection(img):
    (h, w) = img.shape[:2]
    sumRows = []
    for j in range(h):
        row = img[j:j+1, 0:w]
        sumRows.append(np.sum(row))
    return sumRows
    
def verticalProjection(img):
    (h, w) = img.shape[:2]
    sumCols = []
    for j in range(w):
        col = img[0:h, j:j+1] 
        sumCols.append(np.sum(col))
    return sumCols


def straighten(original, dilated, threshed):
    angle = 0.0
    angle_sum = 0.0
    countour_count = 0
    ctrs,hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rendered = original.copy()
    straitened = original.copy()
    threshed_c = threshed.copy()
    dilated_c = dilated.copy()
    for i, ctr in enumerate(ctrs):
        x, y, w, h = cv2.boundingRect(ctr)
        if h>w or h<20:
            continue
        minrect = cv2.minAreaRect(ctr)
        box = cv2.boxPoints(minrect)
        box = np.int0(box)
        angle = minrect[2]
        if angle > 70 : 
            angle -= 90
        rot = cv2.getRotationMatrix2D(((x+w)/2,(y+h)/2), angle, 1)
        roi = original[y:y+h, x:x+w]
        extract = cv2.warpAffine(roi, rot, (w,h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
        straitened[y:y+h, x:x+w] = extract
        if angle!=0 and i>0: 
            angle_sum += angle   
            countour_count += 1
    if countour_count!=0:
        mean_angle = angle_sum / countour_count
        baseline = round(mean_angle,2)
    else: 
        baseline=0 
    threshed_s = threshold(straitened, 160)
    return straitened, rendered, baseline, dilated_c, threshed_c, threshed_s

def extract_lines_indices(image, tolerance):
    hpList = horizontalProjection(image)
    tolerance = max(hpList)*tolerance/100
    start = 0    
    end = 0
    space_flag = False
    line_flag = False
    line_indices = []
    space_indices = []
    for i, sum in enumerate(hpList):
        if sum==0:
            if space_flag==False :
                start = i
                space_flag = True
        else :
            if space_flag==True :
                end = i
                space_indices.append([start,end])
                space_flag=False  
    for i, sum in enumerate(hpList):
        if sum!=0 :
            if line_flag==False :
                start = i
                line_flag = True
        else :
            if line_flag==True :
                end = i
                line_indices.append([start,end])
                line_flag=False   
    return hpList, line_indices, space_indices 

def extract_lines(image, lines_indices, spaces_indices):
    lines = []
    spaces = []
    top_margin = 0
    line_spacing = 0
    x = 0
    lined_image = image.copy()
    for indices in lines_indices :
        hplist = horizontalProjection(image[indices[0]:indices[1],:])
        spaces.append(indices[0]+hplist.index(min(hplist))-x)
        x = indices[0]+hplist.index(min(hplist))
        line = image[indices[0]:indices[1],:]
        lines.append(line)
        lined_image[x:x+1,:] = [255,0,0]
    if(len(spaces_indices)>0):
        top_margin = spaces_indices[0][1]
    else:
        top_margin = 0
    #top_margin = spaces[0]
    line_spacing = round(np.average(spaces),2)
    return lines, top_margin, line_spacing, lined_image
    
def extract_letter_size(lines):
    all_letter_sizes = []
    sized_lines = []
    for line in lines :
        line_letter_sizes = []
        up = 0
        down = 0
        thresh = threshold(lines, 160)
        dilated = dilate(thresh, (5,5))
        (h, w) = line.shape[:2]
        for j in range(0,w,5):
            for i in range(0,h,1):
                if dilated[i:i+1,j:j+1] > 0 :
                    up=i
                    break
            for i in range(h,0,-1):
                if dilated[i:i+1,j:j+1] > 0 :
                    down=i  
                    break
            dilated[up:down,j:j+1]=0    
            letter_size = down - up
            up = 0
            down = 0
            if letter_size != 0 :
                line_letter_sizes.append(letter_size)
        all_letter_sizes.append(np.average(line_letter_sizes))
        sized_lines.append(dilated)   
    return all_letter_sizes, sized_lines

def extract_letter_size_2(lines):
    all_letter_sizes = []
    sized_lines = []
    for line in lines :
        line_letter_sizes = []
        up = 0
        down = 0
        thresh = threshold(line, 160)
        dilated = dilate(thresh, (5,5))
        n_line = line.copy()
        (h, w) = line.shape[:2]
        for j in range(0,w,10):
            for i in range(0,h,1):
                if dilated[i:i+1,j:j+1] > 0 :
                    up=i
                    break
            for i in range(h,0,-1):
                if dilated[i:i+1,j:j+1] > 0 :
                    down=i  
                    break
            n_line[up:down,j:j+1]= [255,0,0]  
            letter_size = down - up
            up = 0
            down = 0
            if letter_size != 0 :
                line_letter_sizes.append(letter_size)
        all_letter_sizes.append(np.average(line_letter_sizes))
        sized_lines.append(n_line)   
    return all_letter_sizes, sized_lines

def extract_words_indices(line, a, b):
    filtered = bilateralFilter(line, 5)
    thresh = threshold(filtered, 160)
    dilated = dilate(thresh, (a,b))
    vpList = verticalProjection(dilated)
    start = 0
    end = 0
    space_flag = False
    word_flag = False
    words_indices = []
    space_indices = []
    for i, sum in enumerate(vpList):
        if sum==0 :
            if space_flag==False :
                start = i
                space_flag = True
        else :
            if space_flag==True :
                end = i
                space_indices.append([start,end])
                space_flag=False  
    for i, sum in enumerate(vpList):
        if sum!=0 :
            if word_flag==False :
                start = i
                word_flag = True
        else :
            if word_flag==True :
                end = i
                words_indices.append([start,end])
                word_flag=False   
    return vpList, dilated, words_indices, space_indices 

def extract_words(line, dilated_line, word_indices, spaces_indices):
    h = line.shape[0]
    words = []
    spaces = []
    word_spacing = 0
    line_n = line.copy()
    for indices in word_indices :
        dilated_line[0:h,indices[0]:indices[0]+1] = 255
        dilated_line[0:h,indices[1]:indices[1]+1] = 255
        line_n[0:h,indices[0]:indices[0]+1] = [255,0,0]
        line_n[0:h,indices[1]:indices[1]+1] = [255,0,0]
        word = line[:,indices[0]:indices[1]]
        words.append(word)
    for indices in spaces_indices :
        space = indices[1]-indices[0]
        spaces.append(space)
    word_spacing = np.average(spaces[1:])
    return words, word_spacing, line_n, dilated_line


def extract(img):
    
    original = cv2.imread(img)
    filtered = bilateralFilter(original, 3)
    thresh = threshold(filtered, 160)
    dilated = dilate(thresh, (1,180))
    straightened, rendered, baseline_angle, dilated_c, threshed_c, threshed_s = straighten(original, dilated, thresh)
    threshed_ss = threshold(straightened, 160)
    
    filtered = bilateralFilter(straightened, 3)
    thresh = threshold(filtered, 160)
    dilated = dilate(thresh, (1,180))
    straightened2, rendered, baseline_angle, dilated_c, threshed_c, threshed_s = straighten(straightened, dilated, thresh)
    
    sfiltered = bilateralFilter(straightened, 5)
    sthresh = threshold(sfiltered, 160)
    hplist, lines_indices, spaces_indices = extract_lines_indices(sthresh, 20)
    lines, top_margin, line_spacing, lined_image = extract_lines(straightened, lines_indices, spaces_indices)
    
    all_letter_sizes, sized_lines = extract_letter_size_2(lines)
    av_letter_size = round(np.average(all_letter_sizes),2)

    vp_lists = []
    dilated_lines = []
    all_words = []
    all_word_spacing = []
    for line in lines :
        vp_list, dilated_line, words_indices, spaces_indices = extract_words_indices(line, 1, 25)    
        words, word_spacing, line_n, line_ns = extract_words(line, dilated_line, words_indices, spaces_indices)
        vp_lists.append(vp_list)
        dilated_lines.append(dilated_line)
        all_words.append(words)
        all_word_spacing.append(word_spacing)
    #avg_word_spacing = round(np.average(all_word_spacing),2)
    avg_word_spacing = round(np.average(all_word_spacing[:-1]),2)

    #print("-> Average BaseLine Angle : ",baseline_angle)
    #print("-> Top Margin :", top_margin)
    #print("-> Average Line Spacing :", line_spacing)
    #print("-> Average Letter Size :", av_letter_size)
    #print("-> Average Word Spacing :", avg_word_spacing)

    return baseline_angle, top_margin, line_spacing, av_letter_size, avg_word_spacing
    



#extract("images/Sample_13.jpg")