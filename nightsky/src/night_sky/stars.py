from skyfield.api import Star, Loader, load, wgs84
from skyfield.data import hipparcos
import skyfield.positionlib as pos
import skyfield.units
load = Loader('nightsky/src')
import matplotlib.pyplot as plt



class StarBall(Star):
    def __init__(self, alt, az, magnitude):
        self.alt = alt
        self.az = az
        self.magnitude = magnitude
        self.color = "white"
    
def load_stars(max_magnitude=6):
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]

def get_observer():
    pos = input("Enter latitude and longitude separated by a comma (or press Enter to use default location - Prague): ")
    if pos.strip() == "":
        return wgs84.latlon(50.093977480399595, 14.450417726625702)
    else:
        lat, lon = map(float, pos.split(","))
        return wgs84.latlon(lat, lon)
    
observer_location = get_observer()
 
def observe_stars():
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    stars = []
    for index, row in load_stars().iterrows():
        star = Star.from_dataframe(row)
        astro = (earth + observer_location).at(t).observe(star).apparent()
        alt, az, distance = astro.altaz()
        stars.append(StarBall(alt.radians, az.radians, row['magnitude']))

    return stars

def get_radec_pole_position():
    pole = Star(ra_hours=0, dec_degrees=90)
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    observer = earth + observer_location
    topocentric = observer.at(t).observe(pole).apparent()
    alt, az, distance = topocentric.altaz()
    return alt.radians, az.radians












    

