# ImageProcessingCAT2
The pointilist school of painters created their paintings by dabbing their paintbrush perpendicularly on the canvas and creating one dab/point of color at a time. Each dab is similar to a single pixel in a digital image. The human viewer of the artwork would stand back and a smooth picture would be perceived. Implement a program to do pointilist art. The program should present a palette of colors and some other options, such as choosing paintbrush size or whether '+' or 'XOR' would be used for dabbing, etc.  When your program is working, create a painting of a starry night. Your program should work with an external file representing in progress so that a user could save the session for later continuation.

# Commands to run

1. pip install cv2,numpy,PyQt5
2. pip uninstall opencv-contrib-python 
3. pip install opencv-contrib-python-headless
4. also install some of the needed packages..
5. python tk_choosefile.py

# Process

Normal Image -> View Colour Palettes of that image  
                               |
                               |
                               V
                      Pointlist Image -> With direct Save option 
                              |
                              |--------> With Paint option to change some colour of the Image points ---> change brush colour
                                                                                                |
                                                                                                |-------> change brush size
                                                                                                |
                                                                                                |-------> save resulting image
