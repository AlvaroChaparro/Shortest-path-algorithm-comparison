import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
from pandas import DataFrame
import mplleaflet

class GenerateGPX:

    def __init__(self, listaPuntos):
        # Creating a new file:
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        for punto in listaPuntos:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(punto[0], punto[1]))

        file = open("ruta.gpx", "w")
        file.truncate()
        file.write(gpx.to_xml())
        file.close()

    def crearVista(self):
        gpx = gpxpy.parse(open("ruta.gpx"))

        track = gpx.tracks[0]
        segment = track.segments[0]
        data = []
        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude])

        columns = ['Longitude', 'Latitude']
        df = DataFrame(data, columns=columns)
        df.head()

        fig, ax = plt.subplots()
        df = df.dropna()
        ax.plot(df['Longitude'], df['Latitude'], color='b', linewidth=5, alpha=0.5)
        ax.plot(df['Longitude'], df['Latitude'], "rs")
        mplleaflet.show()
