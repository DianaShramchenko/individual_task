from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np

# Создание экземпляра FastAPI
app = FastAPI()

# Модель входных данных
class InputData(BaseModel):
    nearest_shop_distance: float
    population_density: float

# Загрузка модели
with open('gb_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Эндпоинт для предсказания
@app.post("/predict/")
async def predict(input_data: InputData):
    try:
        # Преобразование входных данных в массив numpy
        input_array = np.array([[input_data.nearest_shop_distance, input_data.population_density]])
        
        # Предсказание с использованием модели
        prediction = model.predict(input_array)
        
        # Возвращение предсказания
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)