
# Table of Contents

1.  [Usage](#org68e8bfe)
2.  [Approach](#orge5ba65a)
3.  [Technical Choices](#orgf10069d)
    1.  [Libraries](#org2c03d1a)
    2.  [Approach](#org1e94b10)
    3.  [Architecture](#org2f5e038)
        1.  [`CityWeather` model](#org6cf3ff1)
        2.  [`CityWeatherRepository`](#orgba45e27)
        3.  [`CityWeatherService`](#orgd718536)
        4.  [`WeatherClient`](#orga985530)
4.  [Questions](#org8721568)


<a id="org68e8bfe"></a>

# Usage

    cd task_two
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py &
    curl localhost:8080/London
    # {"city":"London","temperature":17.45,"timestamp":"Sun, 23 Oct 2022 12:33:24 GMT"}


<a id="orge5ba65a"></a>

# Approach

Spent too long on Task One - should have spent the additional time here.


<a id="orgf10069d"></a>

# Technical Choices


<a id="org2c03d1a"></a>

## Libraries

-   Flask
    -   Simple, familiar, fast development
-   SqlAlchemy
    -   Familiar, rich functionality, good ORM, uses Data Mapper pattern not Active Record
-   `requests`
    -   Widely used and familiar, good `http` client
-   `pseudobabble/repository`
    -   Simple persistence abstraction I wrote for convenience


<a id="org1e94b10"></a>

## Approach

Trying to keep it readable, with domain relevant naming, logic for different purposes kept segregated, configurable with dependecies.

Out of time for tests and making it pretty.


<a id="org2f5e038"></a>

## Architecture

-   Service oriented architecture
-   Try to keep to SOLID
-   Stateless services, stateful models


<a id="org6cf3ff1"></a>

### `CityWeather` model

Fairly straightforward SqlAlchemy model, can tell callers if it is stale (domain rules).


<a id="orgba45e27"></a>

### `CityWeatherRepository`

Just a persistence wrapper for convenience.


<a id="orgd718536"></a>

### `CityWeatherService`

Encapsulates the logic required to perform the task. Dependencies injected for testability, extensibility, etc.


<a id="orga985530"></a>

### `WeatherClient`

Simple requests Session wrapper. Improvements would be: API token from env, add more complex parameter parsing and passing. More defensive code (`KeyError`), and similar.


<a id="org8721568"></a>

# Questions

The requirements say:

> If a request is made to your API for a city where the weather data was not requested before, OR previously requested more than 4 hours in the past, you should fetch the weather data from the third party OpenWeatherMap API and store the data in your SQL table. Once the data is stored in your database, you should return this data to the user.
> 
> If a request is made to your API for a city where the weather data was previously requested 2 hours or less in the past, you should return the response directly from the SQL table.

Does this mean that stale data is 2+ hours old, or 4+ hours old? There is a gap 2-4 hours where we will not get the data directly from the table, and we will also not update the data. 3hr old data will be returned directly from the OpenWeather API.

I have opted to say that 4+ hours is stale: stale data will trigger an update to persistence, and the new value will be shown to the user.

