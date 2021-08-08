import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import imutils as mut


path = str(input('What is the directory path to the images?\n'))
maxL = int(input('\nWhat is the maximum pixel length?\n'))
bgcolor = (255,255,255)
count=0

for subdir, dirs, files in os.walk(path):
    for file in np.sort(files):
        if file.endswith('.jpg') or\
        file.endswith('.JPG') or\
        file.endswith('.jpeg') or\
        file.endswith('.JPEG') or\
        file.endswith('.png') or\
        file.endswith('.PNG'):
            if 'resized' not in file:

                print(f'\nResizing {file}.... ',end=""),
                filename=os.path.join(subdir,file)
                #read the image in rgb format : [...,::-1], omit to not mess with colors
                img=cv.imread(f'{filename}')

                height,width = img.shape[:-1]

                #resize image based on aspect ratio and determine offsets
                if height >= width:
                    img_resized = mut.resize(img,height=maxL)

                    new_width=img_resized.shape[1]
                    height_offset = 0
                    width_offset = int((maxL-new_width)/2)

                else:
                    img_resized = mut.resize(img,width=maxL)

                    new_height=img_resized.shape[0]
                    width_offset=0
                    height_offset=int((maxL-new_height)/2)

                #create a blank background
                blank_img = np.empty((maxL,maxL,3))
                white_background = cv.rectangle(blank_img,(0,0),(maxL,maxL),
                                               color=bgcolor,thickness=maxL)

                #superimpose resized image onto square background
                white_background[height_offset:height_offset+img_resized.shape[0],
                                width_offset:width_offset+img_resized.shape[1]] = img_resized

                #scale color values??
                final_img = (white_background/256).astype(np.float64)

                #add 'resized' to the end of each filename
                name = filename.split('/')[-1]
                name_without_ext = name.split('.')[0]
                new_name = f'{name_without_ext} resized.jpg'

                #create a destination folder if it does not already exist
                destination = f'{path}/resized'
                if not os.path.exists(destination):
                    os.makedirs(destination)


                #save each image into the folder!
                cv.imwrite(f'{destination}/{new_name}',final_img*255)
                count +=1

                print(' done.')

print(f'\n{count} photos resized and saved!\n')            
