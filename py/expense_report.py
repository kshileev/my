def main():
    import datetime
    import gspread.exceptions
    import gspread.models
    from oauth2client.service_account import ServiceAccountCredentials
    import os

    today = datetime.datetime.now()
    report_title = f'Expenses {today:%Y %b %d}'
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.expanduser('~/Google Drive/CiscoExpenseReportCredentials.json'), scope)
    gs = gspread.authorize(credentials=creds)

    try:
        report = gs.open(title=report_title)
    except gspread.exceptions.SpreadsheetNotFound:
        print('Coping template', 'as', report_title )
        cisco_expense_report_template = gs.open(title='Cisco expense report template')
        report = gs.copy(file_id=cisco_expense_report_template.id, title=report_title)
        report.share('kshileev@gmail.com', perm_type='user', role='writer')

    page1= report.sheet1
    with open(os.path.expanduser('~/Downloads/Amex.csv')) as amex:
        transactions = amex.read().split('\n')

    page1.update_acell('Z15', value=f'{today:%d/%b/%y}')

    cells_to_be_updated = []
    current_row = 62
    total = 0.0
    for i, transaction in enumerate(transactions, start=1):
        if not transaction:
            continue
        current_row += 1
        date, amount, facility, _, _ = transaction.split('\t')
        if 'HOTEL' in facility or 'Hotel' in facility or 'hotel' in facility or 'SUITES' in facility:
            facility = 'HOTEL'
        elif 'UBER' in facility or 'TRIP' in facility or 'CAR RENTAL' in facility or 'LAX' in facility or 'RAIL' in facility:
            facility = 'Transport'
        else:
            facility = 'food'
        amount = float(amount.strip('" '))
        total += amount
        if current_row <= 97:
            num_cell = gspread.models.Cell(row=current_row, col = 1, value=i)
            date_cell = gspread.models.Cell(row=current_row, col = 6, value=date)
            type_cell = gspread.models.Cell(row=current_row, col = 16, value=facility)
            amount_cell = gspread.models.Cell(row=current_row, col = 31, value=amount)
            cells_to_be_updated.extend([num_cell, date_cell, type_cell, amount_cell])
        else:
            page1.insert_row([i, date, facility, amount])


    page1.add_rows(rows=current_row - 97)
    page1.update_cells(cells_to_be_updated)


if __name__ == '__main__':
    main()