from skyfield.api import Star, Loader, load, wgs84
from skyfield.data import hipparcos
import skyfield.units
load = Loader('nightsky/src')
import matplotlib.pyplot as plt

class StarBall(Star):
    def __init__(self, alt, az, magnitude):
        self.alt = alt
        self.az = az
        self.magnitude = magnitude
        self.color = "white"
    
def load_stars(max_magnitude=5.4):
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]

def observe_stars(position=wgs84.latlon(50.093977480399595, 14.450417726625702)):
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    stars = []
    for index, row in load_stars().iterrows():
        star = Star.from_dataframe(row)
        astro = (earth + position).at(t).observe(star).apparent()
        alt, az, distance = astro.altaz()
        stars.append(StarBall(alt.radians, az.radians, row['magnitude']))

    return stars

observe_stars()

    










    

