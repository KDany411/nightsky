# nightsky
Attempt at creating a night sky map in python 

This app is a Stellarium-like app that allows you to see the positions of the stars on the sky based on your location and time
My goal was to implement my mathematical knowledge into the solutions of some problems I was facing during the development.

USER GUIDE:
    First install into your code editor all the required libraried from requirements.txt.
    Then go to src -> night_sky -> main.py and run it
    First some data will be downloaded.
    You will be prompted to enter the coordinates from which you will see the sky, please enter it in the format: <latitude>,<longitude>
    The time is taken from your local machine. 
    After a while the app launches and you should see the map, below it there are 3 buttons for toggling the horizon and the coordinates
    You can look around the sky by using the left and right mouse buttons:
        Left one pans around faster 
        Right one is for finer adjustments
    You can track the position you are ooking at using the crosshair in the middle of the widget.

PROGRAMATORS GUIDE:
    The program is mainly designed around the 3 libraries:
    
        PySide6 -   good for making a basic app, and user friendly UI customization.

                    I used it for designing the layout of my app, adding all the widgets inclusing the OpenGL view widget, the azimuth and altitude tracker, the                       crosshair and the buttons

        pyqtgraph - used for graphing but I used it because it is user friendly when it comes to rendering objects in a widget, one can make
                    objects in OpenGL without much prior knowledge.

                    In pyqtgraph I plotted all of the stars and adjusted their apparent size based on their real life magniuted,
                    rendered the plane of ground, the coordinate grids and the sun with the moon

        skyfield -  extremely useful for working with astronomical data, they offer a large and highly accurate astronomical database and tools to
                    work with those data as desired.

                    I used it to retreive star data, including their apparent postion on the sky and magnitude based on the time and location on earth.

The structer of the code is as follows:

main.py serves for structuring the app layout, the main app launches and closes in there so all of the intermediate steps as generating the widget view and dynamic layouts have to be done in there. Mostly I work here with the Widget hiarchy as PySide6 offeres it:
Widget is like a box and it can be devided either horizontally (QHBoxLayout), vertically(QVBoxLayout), or they can stack on top of each other (QStackedLayout).
The main window fits one "central widget" which can be devided into cells this way. Each cell then can host another widget that can be further devided, this allows for this fractal-like behaviour which, however can be sometimes tedious.
Parent Widgets override attributes of the child widgets so you have to be careful about the structure of the window.
Mine is as follows:

            -:main_window
                -:central_widget (vertical)
                    -:main_widget (stacked)
                        -:overlay (vertical)
                            -:alt, az label
                            -:crosshair
                        -:view_widget - OpenGL
                    -:buttons_bar
                        -:horizon_button
                        -:horizontal_coordinates_button
                        -:equatorial_coordinates_button

gui.py hosts functions for UI of the app: namely the button actions and the dynamic label with alt, az

reder.py generates all of the necesarry renders for OpenGL including some helper functions such as rotational function around an arbitrary axis or a covertor between spherical and carthesian coordinates.

stars.py covers functions around data handling.

I haven't used any noteworthy data structures or algorithms in building this code.



Thank you for using my app, DK



    
