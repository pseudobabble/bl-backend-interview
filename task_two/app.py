from datetime import datetime, timedelta

from flask import Flask
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from requests import Session

from infrastructure import repository
from infrastructure.repository import transaction
from infrastructure.repository.sqlalchemy_adaptor import SqlAlchemyAdaptor


app = Flask(__name__)


class CityWeather(repository.Base):
    __tablename__ = 'city_weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    temperature = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def is_stale(self) -> bool:
        four_hours_ago = datetime.now() - timedelta(hours=4)
        return self.timestamp > four_hours_ago

    @property
    def data(self) -> dict:
        return {
            'city': self.city,
            'temperature': self.temperature,
            'timestamp': self.timestamp
        }


class CityWeatherRepository(SqlAlchemyAdaptor):

    entity = CityWeather

    def get_by_city(self, city: str) -> CityWeather:
        return self.session.query(self.entity)\
                           .filter_by(city=city)\
                           .order_by(self.entity.timestamp)\
                           .first()


class WeatherClient:

    def __init__(self):
        self.session = Session()

    def get_weather(self, city: str) -> float:
        response = self.session.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=cdcd7fd7935f7cd4c338dab780c9c976&units=metric'
        )

        result = response.json()
        temperature = result['main']['temp']

        return temperature


class CityWeatherService:

    def __init__(
            self,
            repository: CityWeatherRepository = CityWeatherRepository(),
            weather_client: WeatherClient = WeatherClient()
    ) -> None:
        self.repository = repository
        self.weather_client = weather_client

    def get_weather(self, city: str) -> CityWeather:
        weather = self.repository.get_by_city(city)
        if not weather or weather.is_stale():
            self._update_weather(city)
            weather = self.repository.get_by_city(city)

        return weather.data

    @transaction
    def _update_weather(self, city: str) -> None:
        new_temperature = self.weather_client.get_weather(city)
        new_city_weather = CityWeather(
            city=city,
            temperature=new_temperature
        )
        self.repository.save(new_city_weather)


@app.route("/<city>")
def weather(city) -> dict:
    weather_service = CityWeatherService()
    city_weather = weather_service.get_weather(city)

    return city_weather


if __name__ == "__main__":
    repository.create_all()
    app.run(host='0.0.0.0', port=8080)
