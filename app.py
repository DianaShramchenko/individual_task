import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Заголовок приложения
st.title("Прогнозирование оптимального расположения магазинов в Венесуэле")

# Описание
st.write("""
Это приложение использует модель машинного обучения для прогнозирования оптимального расположения магазинов на основе расстояния до ближайшего магазина и плотности населения.
""")

# Поля для ввода данных
st.header("Введите данные")
latitude = st.number_input("Широта (latitude):", value=10.4806)  # Пример: широта Каракаса
longitude = st.number_input("Долгота (longitude):", value=-66.9036)  # Пример: долгота Каракаса
nearest_shop_distance = st.number_input("Расстояние до ближайшего магазина (км):", min_value=0.0, value=1.5)
population_density = st.number_input("Плотность населения (чел/км²):", min_value=0.0, value=0.02)

# Кнопка для запуска прогнозирования
if st.button("Прогнозировать"):
    # Подготовка данных для отправки
    input_data = {
        "nearest_shop_distance": nearest_shop_distance,
        "population_density": population_density
    }

    # Отправка запроса на сервер FastAPI
    try:
        response = requests.post(
            "https://individual-task.onrender.com/predict/",  # Ваш публичный URL
            json=input_data
        )
        response.raise_for_status()

        # Получение и отображение результата
        prediction = response.json()["prediction"]
        st.success(f"Оптимальное расстояние для нового магазина: {prediction:.2f} метров")

        # Создание карты
        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        # Добавление маркера для текущего местоположения
        folium.Marker(
            location=[latitude, longitude],
            popup="Текущее местоположение",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        # Добавление маркера для предсказанного местоположения
        folium.Marker(
            location=[latitude, longitude + 0.01],  # Пример: сдвиг по долготе для визуализации
            popup=f"Оптимальное расстояние: {prediction:.2f} метров",
            icon=folium.Icon(color="red")
        ).add_to(m)

        # Отображение карты в Streamlit
        folium_static(m)

    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        st.error(f"Ошибка при обработке ответа: {e}")