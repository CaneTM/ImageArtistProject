""" ImageArtist Project v1.7 (Client #3: Product)
Authored by Canaan Matias and Antonio Ricardo Reyes

Files needed:
- Tech logo image
- Images folder from 1.4.5 (accredited to PLTW)
"""


from PIL import Image, ImageOps
from pylab import *
import os


# get_images method is accredited to PLTW
def get_images(directory=os.path.join(os.getcwd(), "Images")):
   """ Returns PIL.Image objects for all the images in directory.

   If directory is not specified, use current directory.
   Returns a 2-tuple containing
   a list with a  PIL.Image object for each image file in root_directory, and
   a list with a string filename for each image file in root_directory
   """

   image_list = []
   file_list = []

   directory_list = os.listdir(directory)  # Get list of images
   for entry in directory_list:
       absolute_filename = os.path.join(directory, entry)
       try:
           image = Image.open(absolute_filename)
           file_list += [entry]
           image_list += [image]
       except IOError:
           pass  # do nothing with errors trying to open non-images
   return image_list, file_list


def silhouette():
   """
   Create a silhouetted version of a specified image
   """

   # create new figure and pixel array
   fig, axes = plt.subplots(1, 2)
   img = Image.open('tech-logo.png')
   im = np.copy(img)

   height = len(im)
   width = len(im[0])

   # convert to silhouette
   for row in range(height):
       for column in range(width):
           if im[row][column][0] != 255 or im[row][column][1] != 255 or im[row][column][2] != 255:
               im[row][column] = [0, 0, 0]

   axes[0].imshow(img)
   axes[1].imshow(im)

   fig.show()
   plt.pause(10)


def overlay():
   """
   Make a specified image translucent and overlay onto another image to create a watermark effect
   """

   # create new directory to store modified images
   directory = os.getcwd()
   new_directory = os.path.join(directory, 'Overlay')
   try:
       os.mkdir(new_directory)
   except OSError:
       pass

   # make image translucent and resize
   im_rgb = Image.open('tech-logo.png')

   im_rgba = im_rgb.copy()
   im_rgba.putalpha(128)
   im_rgba.save('tech-logo-watermark.png')

   logo_small = im_rgba.resize((89, 87))
   logo_small.save("tech-logo-small.png")

   image_list, file_list = get_images()

   # apply watermark to each image in directory
   for n in range(len(image_list)):
       try:
           print(n)
           filename, filetype = os.path.splitext(file_list[n])

           curr_image = image_list[n]

           width, height = curr_image.size
           mark_width, mark_height = logo_small.size

           x = (width - mark_width) / 2
           y = (height - mark_height) / 2

           pos_x = int(x)
           pos_y = int(y)

           curr_image.paste(logo_small, (pos_x, pos_y), mask=logo_small)
           new_image_filename = os.path.join(new_directory, filename + '.png')
           curr_image.save(new_image_filename)
       except:
           pass


def add_border(border, color=0):
   """
   Creates a frame around an image and applies a logo to each corner
   :param border: frame width in pixels
   :param color: tuple or string
   """

   # create new directory to store modified images
   directory = os.getcwd()
   new_directory = os.path.join(directory, 'Frame')
   try:
       os.mkdir(new_directory)
   except OSError:
       pass

   # open logo four times, one for each corner
   im3 = Image.open('tech-logo-small.png')
   im4 = Image.open('tech-logo-small.png')
   im5 = Image.open('tech-logo-small.png')
   im6 = Image.open('tech-logo-small.png')

   image_list, file_list = get_images()

   # apply a frame to each image in directory and paste logo onto corners
   for n in range(len(image_list)):
       try:
           print(n)
           filename, filetype = os.path.splitext(file_list[n])

           curr_image = image_list[n]

           if isinstance(border, int) or isinstance(border, tuple):
               bimg = ImageOps.expand(curr_image, border=border, fill=color)
           else:
               raise RuntimeError('Border is not an integer or tuple!')

           back_im = bimg.copy()

           width, height = back_im.size
           mark_width, mark_height = im3.size
           offset = 5

           back_im.paste(im3, (offset, offset))
           back_im.paste(im4, (width - mark_width - offset, offset))
           back_im.paste(im5, (offset, height - mark_height - offset))
           back_im.paste(im6, (width - mark_width - offset, height - mark_height - offset))

           new_image_filename = os.path.join(new_directory, filename + '.png')
           back_im.save(new_image_filename, quality=95)
       except:
           pass


def run(option):	# includes parameter of manipulation
   """
   Main method to activate silhouette, overlay, or frame options
    - 0 : make silhouette
    - 1 : make watermark (overlay)
    - 2 : make frame and apply logo (add_border)
   :param option: integer
   """
   if option == 0:
       silhouette()
   elif option == 1:
       overlay()
   elif option == 2:
       add_border(
              border=100,
              color='green')


run(0)      # execute function
