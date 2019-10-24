def time_of_kse_move(x):
    import math

    m = 1
    ms = 1
    l1 = 50 * m
    l2 = 50 * m
    L = 40 * m
    V1 = 10 * ms
    V2 = V1 / 10

    return math.sqrt(l1 * l1 + (L - x) *  (L -x)) / V1 + math.sqrt(l2 * l2 + x * x) / V2


def frange(x1, x2, step):
    elements = []
    current = x1
    while current <= x2:
        elements.append(current)
        current = current + step
    return elements

def ele_price(hour, kwt):
    msk1 = 5.47
    msk2_7_23, msk2_23_7 = 6.29, 2.13
    msk3_7_23, msk3_23_7, msk3_23_7 = 6.57, 5.47, 2.13

    mse1 = 4.65
    mse2_7_23, mse2_23_7 = 5.03, 1.37
    mse3_7_23, mse3_23_7, mse3_ = 5.25, 4.37, 1.37

    tro1 = 5.47
    tro2_7_23, tro2_23_7 = 6.29, 2.45
    tro3_7_23, tro3_23_7, tro3_ = 6.57, 5.47, 2.45


    tre1 = 4.37
    tre2_7_23, tre2_23_7 = 4.82, 1.73
    tre3_7_23, tre3_23_7, tre3_ = 5.01, 4.18, 1.73


def kse():
    import plotly
    import plotly.graph_objs as go


    Xn = frange(2.95, 3.0, 0.001)
    Yn = [time_of_kse_move(x) for x in Xn]

    [print(x[0], x[1]) for x in zip(Xn, Yn) ]

    n1 = go.Scatter(x=Xn, y=Yn, mode='markers', name='nodes', marker={'symbol': 'square'})
    n2 = go.Scatter(x=Xn, y=Yn, mode='markers', name='nodes', marker={'symbol': 'square'})

    plotly.offline.plot({'data': [n1]}, filename='ksenia_example.html', auto_open=True)
    plotly.offline.plot({'data': [n2]}, filename='electricity_expenses.html', auto_open=True)


if __name__ == '__main__':
    kse()
