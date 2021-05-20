import datetime


class air_conditioning:
    def __init__(self):
        self.temperature = 20
        self.season = 0
        self.sensor_temperature = 24
        self.threshold = 2

    def get_sensor_temperature(self, sensor_temperature):
        self.sensor_temperature = sensor_temperature

    def start(self):
        self.get_season()
        if self.season == 1:
            self.temperature = 26
        elif self.season == 2:
            self.temperature = 20
        elif self.season == 3:
            self.temperature = 26
        else:
            self.temperature = 30

        return self.temperature, self.sensor_temperature

    def change_temperature(self, sensor_temperature):
        self.get_sensor_temperature(sensor_temperature)

        minus = self.temperature - self.sensor_temperature

        if minus > self.threshold:
            self.temperature = self.sensor_temperature - self.threshold
        elif minus < -self.threshold:
            self.temperature = self.sensor_temperature + self.threshold
        else:
            self.temperature = self.sensor_temperature

        return self.temperature, self.sensor_temperature

    def get_season(self):
        date = datetime.datetime.today()
        month = date.month
        if 1 <= month <= 3:
            self.season = 1
        elif 4 <= month <= 6:
            self.season = 2
        elif 7 <= month <= 9:
            self.season = 3
        else:
            self.season = 4

    def set_threshold(self, threshold):
        self.threshold = float(threshold)


if __name__ == '__main__':
    temp = air_conditioning()