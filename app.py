from flask import Flask, render_template, request, redirect, url_for
import sys
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query

app = Flask(__name__)
Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)


# engine = create_engine('sqlite:///weather.db', echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


# # add sample cities
# city_1 = City(name='Toronto')
# city_2 = City(name='New York')
# city_3 = City(name='Vancouver')
# session.add(city_1)
# session.add(city_2)
# session.add(city_3)
# session.commit()


def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=881166ae591cf527cd96554a9bc95d65'
    r = requests.get(url)
    weather = r.json()
    return weather


@app.route('/')
def index_get():
    engine = create_engine('sqlite:///weather.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = Query(City, session)
    all_rows = query.all()
    session.close()
    context = []
    for row in all_rows:
        # print(row.name)
        row_weather = get_weather(row.name)
        print(row_weather)
        weather_dict = {
            'city': row.name,
            'temp': row_weather['main']['temp'],
            'description': row_weather['weather'][0]['description']
        }
        context.append(weather_dict)

    return render_template('index.html', context=context)


@app.route('/', methods=['POST'])
def index_post():
    city = request.form.get('city_name')
    print(city)
    # weather = get_weather(city)
    # print(weather)
    # city = city.title()
    # return render_template('index.html', weather=weather, city=city)
    engine = create_engine('sqlite:///weather.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    city_add = City(name=city)
    session.add(city_add)
    session.commit()
    session.close()
    return redirect(url_for('index_get'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
