from astropy.coordinates import get_body
import numpy as np
import astropy.units as u

MOON_RADIUS = 1737.4 * u.km


def separation_to_moon(observer, time, target):
    moon = get_body("moon", time, observer.location)
    moon_distance = moon.distance
    moon_ang_radius = np.arcsin(MOON_RADIUS / moon_distance).to(u.deg)
    separation = moon.separation(target.transform_to(moon.frame)) - moon_ang_radius
    return separation
