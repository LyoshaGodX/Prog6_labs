import datetime
import calendar
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from mathstats import MathStats
from collections import defaultdict
from typing import List, Dict
from datetime import datetime


def main():
    # Пример работы функциями-геттерами класса MathStats
    data_marketing = MathStats('MarketingSpend.csv')

    print(data_marketing.mean)  # (2843.5616438356165, 1905.8807397260264)
    print(data_marketing.max)  # (5000.0, 4556.93)
    print(data_marketing.min)  # (500.0, 320.25)
    print(data_marketing.disp)  # (904376.3557890793, 652456.9451865801)
    print(data_marketing.sigma_sq)  # (950.9870429133508, 807.7480703700753)

    # Пример работы функций из main.py
    data_retail = read_data('Retail.csv')

    print(count_invoice(data_retail))  # 16522

    print(count_different_values(data_retail, 'InvoiceNo'))  # 16522
    print(count_different_values(data_retail, 'InvoiceDate'))  # 292
    print(count_different_values(data_retail, 'StockCode'))  # 1178

    print(get_total_quantity(data_retail, '20979'))  # 1877
    print(get_total_quantity(data_retail, '15056'))  # 5216
    print(get_total_quantity(data_retail, '17001'))  # 1

    plot_data_marketing(data_marketing.data)
    plot_data_retail(data_retail)


def plot_data_marketing(data: List[Dict[str, float]]):
    """
    Горизонтальная столбчатая диаграмма продаж по месяцам.
    Цветом в каждом столбце отмечены продажи offline и online.
    """
    # Получаем уникальные месяцы и сортируем их
    months = sorted({_el['Date'][:7] for _el in data})
    months_labels = [calendar.month_name[int(month[-2:])] for month in months]

    # Инициализируем словари для продаж
    sales = defaultdict(lambda: {'Offline': 0, 'Online': 0})

    # Заполняем словари данными о продажах
    for _el in data:
        month = _el['Date'][:7]
        sales[month]['Offline'] += _el['Offline']
        sales[month]['Online'] += _el['Online']

    # Подготовка данных для построения графика
    offline_values = [sales[month]['Offline'] for month in months]
    online_values = [sales[month]['Online'] for month in months]
    y = range(len(months))

    # Создание графика
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.barh(y, offline_values, color='blue', label='Offline')
    ax.barh(y, online_values, color='red', label='Online', left=offline_values)

    # Настройка осей и меток
    ax.set_yticks(y)
    ax.set_yticklabels(months_labels)
    ax.invert_yaxis()
    ax.set_xlabel('Sales')
    ax.set_title('Sales by month')
    ax.legend()

    # Добавление текста на график
    for i, (offline_val, online_val) in enumerate(zip(offline_values, online_values)):
        total_val = offline_val + online_val
        ax.text(offline_val / 2, i, f'{int(offline_val)}', va='center', ha='center', color='white', fontweight='bold')
        ax.text(offline_val + online_val / 2, i, f'{online_val:.2f}', va='center', ha='center', color='white',
                fontweight='bold')
        ax.text(total_val * 1.01, i, f'{total_val:.2f}', va='center', ha='left', fontweight='bold')

    # Настройка пределов оси X
    max_value = max(offline + online for offline, online in zip(offline_values, online_values))
    ax.set_xlim(0, max_value * 1.1)

    # Сохранение и отображение графика
    plt.savefig('Marketing.png')
    plt.show()


def plot_data_retail(data: List[Dict[str, str]]):
    # Преобразование данных
    for item in data:
        item['Date'] = datetime.strptime(item['InvoiceDate'], '%Y-%m-%d').date()
        item['Quantity'] = int(item['Quantity'])

    # Группировка данных
    grouped_data = {}
    for item in data:
        date = item['Date']
        grouped_data[date] = grouped_data.get(date, 0) + item['Quantity']

    # Создание графика
    fig, ax = plt.subplots(figsize=(16, 10))

    # Построение точечного графика
    ax.scatter(grouped_data.keys(), grouped_data.values())

    # Настройка осей
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%j'))

    ax.set_xlabel('Day of the year')
    ax.set_ylabel('Quantity sold')
    ax.set_title('Quantity of products sold per day')

    plt.savefig('Retail.png')

    plt.show()



def read_data(file: str) -> List[dict]:
    import csv
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for _r in reader:
            row = _r
            data.append(row)
    return data


def count_invoice(data: List[dict]) -> int:
    from collections import Counter

    invoices = [_el['InvoiceNo'] for _el in data]

    count = len(Counter(invoices))
    return count


def count_different_values(data: List[dict], key: str) -> int:
    unique_values = set(_el[key] for _el in data)
    return len(unique_values)


def get_total_quantity(data: List[dict], stock_code: str) -> int:
    total_quantity = sum(int(_el['Quantity']) for _el in data if _el['StockCode'] == stock_code)
    return total_quantity


if __name__ == "__main__":
    main()
