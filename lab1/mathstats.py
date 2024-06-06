class MathStats():
    """
    Класс для вычисления статистических показателей по данным.
    """

    def __init__(self, file):
        import csv

        self._file = file
        self._data = []
        self._mean = None
        self._max = None
        self._min = None
        self._disp = None
        self._sigma_sq = None

        with open(self._file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for _r in reader:
                row = {
                    'Date': _r[''],
                    'Offline': float(_r['Offline Spend']),
                    'Online': float(_r['Online Spend']),
                }
                self._data.append(row)

    @property
    def data(self) -> list[dict]:
        return self._data

    @property
    def mean(self) -> tuple[float, float]:
        if self._mean is None:
            offline_sum = 0
            online_sum = 0
            for row in self._data:
                offline_sum += row['Offline']
                online_sum += row['Online']

            self._mean = (offline_sum / len(self._data), online_sum / len(self._data))
        return self._mean

    @property
    def max(self) -> tuple[float, float]:
        if self._max is None:
            offline_max = float('-Inf')
            online_max = float('-Inf')
            for row in self._data:
                offline_max = max(offline_max, row['Offline'])
                online_max = max(online_max, row['Online'])

            self._max = (offline_max, online_max)
        return self._max

    @property
    def min(self) -> tuple[float, float]:
        if self._min is None:
            offline_min = float('Inf')
            online_min = float('Inf')
            for row in self._data:
                offline_min = min(offline_min, row['Offline'])
                online_min = min(online_min, row['Online'])

            self._min = (offline_min, online_min)
        return self._min

    @property
    def disp(self) -> tuple[float, float]:
        if self._disp is None:
            offline_sum = 0
            online_sum = 0
            offline_sq_sum = 0
            online_sq_sum = 0
            for row in self._data:
                offline_sum += row['Offline']
                online_sum += row['Online']
                offline_sq_sum += row['Offline'] ** 2
                online_sq_sum += row['Online'] ** 2

            N = len(self._data)
            offline_mean = offline_sum / N
            online_mean = online_sum / N

            offline_disp = offline_sq_sum / N - (offline_mean ** 2)
            online_disp = online_sq_sum / N - (online_mean ** 2)

            self._disp = (offline_disp, online_disp)

        return self._disp

    @property
    def sigma_sq(self) -> tuple[float, float]:
        if self._sigma_sq is None:
            disp = self.disp
            self._sigma_sq = (disp[0] ** 0.5, disp[1] ** 0.5)
        return self._sigma_sq
