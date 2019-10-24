def main():
    from _plotly_future_ import v4_subplots
    import plotly.subplots
    import plotly.graph_objs as go
    import os
    import collections

    with open(os.path.expanduser('~/Downloads/details.csv'), encoding='cp1251') as vtb:
        transactions = vtb.read().split('\n')

    dates = []
    shops = []
    sum_values = []
    sum_colors = []
    owner_values = []
    owner_colors = []
    categ_values = []
    categ_colors = []
    fill_colors = []
    total_income = 0.0
    total_outcome = 0.0
    card_owner_d = {'1113': {'name': 'Kir счет', 'sum': 0.0, 'color': 'lightblue' },
                    '6447': {'name': 'Kir Master', 'sum': 0.0, 'color': 'cyan' },
                    '1850': {'name': 'Kir VISA', 'sum': 0.0, 'color': 'aquamarine' },
                    '8082': {'name': 'Credit VISA', 'sum': 0.0, 'color': 'lightred' },
                    '0657': {'name': 'Kse VISA', 'sum': 0.0, 'color': 'lightgreen' },
                    '0664': {'name': 'Nata VISA', 'sum': 0.0, 'color': 'pink' }}
    Category = collections.namedtuple('Category', ['name', 'color', 'sum', 'shops'])
    categories = [Category(name='траспорт', color='paleturquoise', sum=0.0, shops=['BPMAZK', 'TAXI']),
                  Category(name='банкомат', color='red', sum=0.0, shops=['Снятие']),
                  Category(name='ипотека', color='red', sum=0.0, shops=['Перевод на счет *2150']),
                  Category(name='медицина', color='paleturquoise', sum=0.0, shops=['KLINIKA', 'APTEKA', 'TSENTRMEDFARMA']),
                  Category(name='магазины', color='mediumorchid', sum=0.0, shops=['DECATHLON', 'IKEA', 'RESPUBLIKA', 'IL DE BOTE', 'DETSKIY MIR']),
                  Category(name='связь', color='cyan', sum=0.0, shops=['TELE2', 'ITUNES.COM', 'Билайн', 'AWS']),
                  Category(name='власть', color='moccasin', sum=0.0, shops=['GOSUSLUGI', 'GIBDD']),
                  Category(name='еда', color='yellow', sum=0.0, shops=['KONDITERSKAYA', 'PYATEROCHKA', 'COFFEE', 'CINNABON', 'Yandex.Eda', 'CAFE', 'PlovBerry', 'PIZZA', 'MCDONALDS', 'STARBUCKS', 'KOFE', 'MIRATORG', 'RESTAURANT', 'VKUSVILL', 'AZBUKAVKUSA', 'SODEKSO', 'KFC', 'FOOD'])
                  ]
    category_sum_d = collections.OrderedDict({x.name: 0.0 for x in categories})
    category_sum_d['неизвестно'] = 0.0
    for i, transaction in enumerate(transactions, start=1):
        if not transaction:
            continue
        x = transaction.split(';')
        if len(x) == 9:
            try:
                value = float(x[3].replace(',', '.').replace(' ', ''))
                sum_values.append(value)
                if value > 0 :
                    sum_colors.append('paleturquoise')
                    total_income += value
                else:
                    sum_colors.append('lavender')
                    total_outcome += value
                fill_colors.append('lavender')
                dates.append(x[1])
                card = x[0][-4:]
                owner_values.append(card_owner_d[card]['name'])
                owner_colors.append(card_owner_d[card]['color'])
                if value < 0:
                    card_owner_d[card]['sum'] += -value
                shop = x[7]
                shops.append(shop)
                for category in categories:
                    if any([x in shop for x in category.shops]):
                        categ_values.append(category.name)
                        categ_colors.append(category.color)
                        if value < 0:
                            category_sum_d[category.name] += -value
                        break
                else:
                    categ_values.append('неизвестно')
                    categ_colors.append('lavender')
                    if value < 0:
                        category_sum_d['неизвестно'] += -value
            except ValueError:
                continue
    tbl = go.Table(header=dict(values=['Дата', 'Сумма', 'Кто', 'Магазин', 'Категория']),
                   cells=dict(values=[dates, sum_values , owner_values, shops, categ_values], fill_color = [fill_colors, sum_colors, owner_colors, fill_colors, categ_colors]),

                   )
    pie_cat_names = []
    pie_cat_sums = []
    for cat, cat_sum in category_sum_d.items():
        pie_cat_names.append(cat)
        pie_cat_sums.append(cat_sum)

    cat_pie = go.Pie(labels=pie_cat_names, values=pie_cat_sums, name='Траты на', textinfo='label+percent', showlegend=False, hole=.3)

    pie_own_names = []
    pie_own_sums = []
    for _, own_d in card_owner_d.items():
        pie_own_names.append(own_d['name'])
        pie_own_sums.append(own_d['sum'])

    own_pie = go.Pie(labels=pie_own_names, values=pie_own_sums, name='Карта', textinfo='label+percent', showlegend=False, hole=.3)

    fig = plotly.subplots.make_subplots(rows=3, cols=1, specs=[[{'type': 'table'}], [{'type': 'pie'}], [{'type': 'pie'}]])
    fig.add_trace(tbl, row=1, col=1)
    fig.add_trace(cat_pie, row=2, col=1)
    fig.add_trace(own_pie, row=3, col=1)
    plotly.offline.plot({'data': fig}, filename='VTB.html', auto_open=True)

if __name__ == '__main__':
    main()