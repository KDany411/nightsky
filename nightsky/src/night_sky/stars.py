from skyfield.api import Star, Loader, load, wgs84
from skyfield.data import hipparcos
import skyfield.positionlib as pos
import skyfield.units
import numpy as np
load = Loader('nightsky/src')
import matplotlib.pyplot as plt

# these are frequently used objects from the skyfield library so I set them up globally instead of rewriting them in every function
ts = load.timescale()
t = ts.now()
planets = load('de421.bsp')
earth = planets['earth']

class StarBall(Star):
    """Here I made a class for the star data"""
    def __init__(self, alt, az, magnitude):
        self.alt = alt
        self.az = az
        self.magnitude = magnitude
        self.color = "white"
    
def load_stars(max_magnitude=6):
    """Loading the star data based on the stars' magnitudes, everything below the number 
    in the parameter is omitted, you can adjust it but it loads super slow above 6 and lags quite a bit"""
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]

def get_observer():
    """Prompts you in the terminal to enter the coordinates from which you see the sky"""
    pos = input("Enter latitude and longitude separated by a comma (or press Enter to use default location - Prague): ")
    if pos.strip() == "":
        return wgs84.latlon(50.093977480399595, 14.450417726625702)
    else:
        lat, lon = map(float, pos.split(","))
        return wgs84.latlon(lat, lon)
    
observer_location = get_observer()
 
def observe_stars():
    """Here I take the filtered data a trasfer each star into my cunstom class"""
    stars = []
    
    for index, row in load_stars().iterrows():
        star = Star.from_dataframe(row)
        astro = (earth + observer_location).at(t).observe(star).apparent()
        alt, az, distance = astro.altaz()
        stars.append(StarBall(alt.radians, az.radians, row['magnitude']))

    return stars

def get_radec_pole_position():
    """This function serves getting the horizontal position of the celestial pole,
    I know it doesn't change at all, but what if my code is uncovered by some future civilization and the pole 
    shifted a bit by then. They will still be able to use my program!"""
    pole = Star(ra_hours=0, dec_degrees=90)
    observer = earth + observer_location
    topocentric = observer.at(t).observe(pole).apparent()
    alt, az, distance = topocentric.altaz()
    return alt.radians, az.radians

    
def get_ra_angle():
    """Gets the RA angle of a point right below the pole, useful for drawing the RA lines"""
    pole_alt, pole_az = get_radec_pole_position()
    observer = earth + observer_location
    p = observer.at(t).from_altaz(alt_degrees=np.rad2deg(pole_alt)-10, az_degrees=np.rad2deg(pole_az))
    ra, dec, _ = p.radec()
    return ra.radians

def get_sun_position():
    """Speaks for itself"""
    sun = planets['sun']
    observer = earth + observer_location
    topocentric = observer.at(t).observe(sun).apparent()
    alt, az, distance = topocentric.altaz()
    return alt.radians, az.radians

def get_moon_position():
    """Moon"""
    moon = planets['moon']
    observer = earth + observer_location
    topocentric = observer.at(t).observe(moon).apparent()
    alt, az, distance = topocentric.altaz()
    return alt.radians, az.radians












    

