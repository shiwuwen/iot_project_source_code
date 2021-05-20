class Hygrometer:
    def __init__(self):
        self.humidity = 0
        self.sensor_humidity = 50
        self.threshold = 65

    def get_sensor_humidity(self, sensor_humidity):
        self.sensor_humidity = sensor_humidity

    def change_humidity(self, sensor_humidity):
        self.get_sensor_humidity(sensor_humidity)

        if self.sensor_humidity > self.threshold + 5:
            self.humidity = self.sensor_humidity - 5
        elif self.sensor_humidity < self.threshold - 5:
            self.humidity = self.sensor_humidity + 5
        else:
            self.humidity = self.sensor_humidity

        return self.humidity, self.sensor_humidity

    def set_threshold(self, threshold):
        self.threshold = float(threshold)
