from PIL import Image
import random

random.seed() #seed the random generator


#NOTES
#make generateRandomRGB take the viable Markov states into account
#
#
#



#width and height of the image
width = 100
height = 100
order = 2

img = Image.new('RGBA', (width, height))

done = False #used to determine if image is done
img_name = "test.png" #what to save the image as


#small class to clear up some of the code
class Pixel:
    def __init__(self):
        this.x = 0
        this.y = 0


current_pixel = Pixel() #the current pixel that needs to be set


#generates a random rgba value
def generateRandomRGB():
    red = random.randrange(256)
    blue = random.randrange(256)
    green = random.randrange(256)
    return (red, blue, green)


#increments the current pixel value
def incPixel():
    global current_pixel, width, height, done
    if current_pixel.x is width-1:
        current_pixel.x = 0
        if current_pixel.y is height-1: #image is generated if we reach the end of this row
            done = True
        else:
            current_pixel.y += 1
    else:
        current_pixel.x += 1
         

#sets a number of starting pixels to randomized RGBA values equal to the order of the Markov chain
def orderedRandomPixels():
    global img, order
    for x in range(0, order):
        rgb = generateRandomRGB() 
        img.putpixel((current_pixel.x, current_pixel.y), (rgb[0], rgb[1], rgb[2]))
        incPixel()


#sets the next pixel of the image
def setCurrentPixel():
    global img, order, current_pixel
    img.putpixel((current_pixel.x, current_pixel.y), (0, 0, 0))
    incPixel()
    

#calls the above functions in the correct order
def generateImage():
    global done
    orderedRandomPixels()
    while not done:
        setCurrentPixel()
    img.save(img_name)
    

        
