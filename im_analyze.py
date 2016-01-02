from PIL import Image


#represents a "link" in a markov chain for the pixels of an image (RGB format)
#rs, gs, bs, and als are the red, green, blue, and alpha values respectively (lists)
#ds_rgba is the destination state's rgba value (4-tuple)
class PixelLink:
        def __init__(self, order, rs=[], gs=[], bs=[], als=[], ds_rgba=(0,0,0,0)):
                self.reds = rs
                self.greens = gs
                self.blues = bs
                self.alphas = als
		
                self.dest_rgba = ds_rgba
		
                self.probability = 0.0


        def compareRGBA(self, link):
                if (self.reds == link.reds) and (self.greens == link.greens) and (self.blues == link.blues) and (self.alphas == link.alphas):
                        return True
                return False


        def compare(self, link):
                if self.compareRGBA(link):
                        if self.dest_rgba == link.dest_rgba:
                                return True
                return False


#used to get all red, green, blue, and alpha values from an array of pixels
def getSubarrayValues(array, index):
        subarr_elems = []
        for elm in array:
                subarr_elems.append(elm[index])
        return subarr_elems


#get the first set of pixels
def getFirstPixels(img, pixels, order, current_pos):
        selected_pixels = []
        for y in range(0, img.height):
                for x in range(0, img.width):
                        if current_pos[1] * img.height + current_pos[0] is order:
                                break
                        selected_pixels.append(pixels[y * img.height + x])
                        current_pos[0] += 1
                if current_pos[1] * img.height + current_pos[0] is order:
                        break
                current_pos[1] += 1
                
        return selected_pixels


#create the initial links for the chain (no probabilities yet)
def forgeLinks(img, pixels, order):

        #sets an array with a number of pixels equal to order
        current_pos = [0, 0]
        selected_pixels = getFirstPixels(img, pixels, order, current_pos)

        links = []

        #cycle through pixels until end of image is reached
        for y in range(current_pos[1], img.height):
                for x in range(current_pos[0], img.width):
                        
                        reds = getSubarrayValues(selected_pixels, 0)
                        greens = getSubarrayValues(selected_pixels, 1)
                        blues = getSubarrayValues(selected_pixels, 2)
                        alphas = getSubarrayValues(selected_pixels, 3)
                        
                        links.append(PixelLink(order, reds, greens, blues, alphas, pixels[y*img.height+x]))
                        
                        #update selected pixels
                        del selected_pixels[0]
                        selected_pixels.append(pixels[y * img.height + x])
        return links


#determines is a PixelLink is already in an array
def checkDup(arr, target):
        for elm in arr:
                if elm.compare(target):
                        return True


#determines probability of a state transition
def calcProbability(links):
        for i in range(0, len(links)):
                total = links[i].probability
                for j in range(i, len(links)):
                        if links[i].compareRGBA(links[j]):
                                total += links[j].probability
                links[i].probability = links[i].probability / total


#end user function
#generates the probability table for markov chains of the specified order
def imageToMarkov(img_name, order):
        img = Image.open(img_name)
        pixels = list(img.getdata())

        links = forgeLinks(img, pixels, order)


        sep = [] #separated links (used to gather the amount of a single state)
        for i in range(0, len(links)):
                count = 0 #number of times that the state is seen
                if not checkDup(sep, links[i]):
                        for j in range(i, len(links)):
                                if links[i].compare(links[j]):
                                        count += 1

                        links[i].probability = count
                        sep.append(links[i])

        calcProbability(sep)
        return sep

