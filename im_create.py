from PIL import Image
import random
import im_analyze as ima

random.seed() #seed the random generator


#NOTES
#make generateRandomRGB take the viable Markov states into account
#
#
#



#width and height of the image
width = 48
height = 48
order = 2

src_name = "frog.png" #name of the image the markov chains are to be based off of
markov_chain = ima.imageToMarkov(src_name, order)

img = Image.new('RGBA', (width, height))
img_name = "test.png" #what to save the image as

done = False #used to determine if image is done


#small class to make the code more explicit
class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0


current_pixel = Coord() #the current pixel that needs to be set
pixels_in_order = [] #list of the pixels in the current order, rgba values


#randomly choose an link from the markov_chain
def getRandomLink():
    global markov_chain
    return markov_chain[random.randrange(0, len(markov_chain))]


#generates a random rgba value from the markov_chain
def generateRandomRGBA():
    selected_link = getRandomLink() #get a random chain use it so that the resulting rgba is valid
    pixel_index = random.randrange(0, order) #determines which pixel rgba values to get out of the
    
    red = selected_link.reds[pixel_index]
    blue = selected_link.greens[pixel_index]
    green = selected_link.blues[pixel_index]
    alpha = selected_link.alphas[pixel_index]
    return (red, blue, green, alpha)


#generates a PixelLink from the pixels_in_order list
def rgbaToLink():
    global pixels_in_order

    reds = []
    greens = []
    blues = []
    alphas = []
    
    for p in pixels_in_order:
        reds.append(p[0])
        greens.append(p[1])
        blues.append(p[2])
        alphas.append(p[3])

    return ima.PixelLink(order, reds, greens, blues, alphas)


#generates an rgba value that takes pixels_in_order into account
def generateSmartRGBA():
    global pixels_in_order, markov_chain

    #create a PixelLink for comparison to markov_chain
    order_link = rgbaToLink()

    viable_links = []
    for l in markov_chain:
        if l.compareRGBA(order_link):
            viable_links.append(l)

    roll = random.uniform(0.01, 100.0)

    total = 0.0
    for l in viable_links:
        total += l.probability * 100
        if total >= roll:
            return l.dest_rgba
    
    #return the selected links dest_rgba
    return viable_links[random.randrange(len(viable_links))].dest_rgba
    

#increments the current pixel value (takes height and width of image into account)
def incPixel(rgba):
    global current_pixel, width, height, done, pixels_in_order

    if len(pixels_in_order) is order:
        pixels_in_order.pop(0)
    pixels_in_order.append(rgba)


    if current_pixel.x is width-1:
        current_pixel.x = 0
        if current_pixel.y is height-1: #image is generated if we reach the end of this row
            done = True
        else:
            current_pixel.y += 1
    else:
        current_pixel.x += 1
        

#sets a number of starting pixels to randomized RGBA values equal to the order of the Markov chain
def setStartingPixels():
    global img, order, current_pixel

    link = getRandomLink()
    for x in range(0, order):
        rgba = (link.reds[x], link.greens[x], link.blues[x], link.alphas[x])
        img.putpixel((current_pixel.x, current_pixel.y), (rgba[0], rgba[1], rgba[2], rgba[3]))
        incPixel(rgba)


#sets the next pixel of the image
def setCurrentPixel():
    global img, order, current_pixel    

    rgba = generateSmartRGBA()
    img.putpixel((current_pixel.x, current_pixel.y), (rgba[0], rgba[1], rgba[2], rgba[3]))
    incPixel(rgba)
    

#calls the above functions in the correct order
def generateImage():
    global img, img_name, done
    
    setStartingPixels()
    while not done:
        setCurrentPixel()
    img.save(img_name)


generateImage()



