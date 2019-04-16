import math
from aero.phy_const import *


class AeroCalc:
    @staticmethod
    def optical_horizon(observer_h):
        dist = math.sqrt(observer_h * (observer_h + 2 * PhyConst.kEarthRadiusM))
        alpha = math.acos(PhyConst.kEarthRadiusM / (PhyConst.kEarthRadiusM + observer_h))
        s_dist = PhyConst.kEarthRadiusM * alpha
        return dist, s_dist, math.degrees(alpha)

    @staticmethod
    def plot_optical_horizon():
        import plotly
        import plotly.graph_objs as go

        heights = list(range(500, 40000, 500))
        dists = []
        surfs = []
        angles = []
        t_dists = []
        t_surfs = []
        t_angles = []
        for height in heights:
            dist, surf, alpha = AeroCalc.optical_horizon(height)
            dists.append(dist)
            surfs.append(surf)
            angles.append(alpha)
            t_dists.append(f'выс {height/1000}км прям гор {dist/1000:.2f}км')
            t_surfs.append(f'выс {height/1000}км сфер гор {surf/1000:.2f}км')
            t_angles.append(f'выс {height/1000}км угол {alpha:.2f}')

        n1 = go.Scatter(x=heights, y=dists, name='прям горизонт', text=t_dists, mode='markers', hoverinfo='text')
        n2 = go.Scatter(x=heights, y=surfs, name='сфер горизонт', text=t_surfs, mode='markers', hoverinfo='text')
        n3 = go.Scatter(x=heights, y=angles, name='сфер угол', text=t_angles,  mode='markers', hoverinfo='text', yaxis='y2')
        layout = go.Layout(title='Optical horizon',
                           xaxis={'title': 'высота, метры'},
                           yaxis={'title': 'дистанция, метры'},
                           yaxis2={'title': 'угол', 'overlaying': 'y', 'side': 'right'})
        plotly.offline.plot({'data': [n1, n2, n3], 'layout': layout}, filename='aero_plots.html', auto_open=True)


def main():
    AeroCalc.plot_optical_horizon()


if __name__ == '__main__':
    main()
