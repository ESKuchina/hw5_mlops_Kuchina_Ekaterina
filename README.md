# HW5 MLOps — обеспечение воспроизводимости эксперимента

Репозиторий проекта:
https://github.com/ESKuchina/hw5_mlops_Kuchina_Ekaterina

## Цель проекта

Цель проекта — собрать минимальный, но полноценный MLOps-контур для воспроизводимого эксперимента машинного обучения. В работе реализованы версионирование данных через DVC, воспроизводимый пайплайн подготовки данных и обучения модели, а также логирование параметров, метрик и артефактов через MLflow.

## Структура проекта

data/ — данные и DVC-артефакты  
src/ — скрипты подготовки данных и обучения модели  
notebooks/ — вспомогательные материалы и пример Marimo  
dvc.yaml — описание DVC-пайплайна  
params.yaml — параметры подготовки и обучения  
requirements.txt — зависимости проекта  
README.md — документация по проекту  

## Как запустить

1. Клонировать репозиторий:
git clone https://github.com/ESKuchina/hw5_mlops_Kuchina_Ekaterina.git

2. Перейти в папку проекта:
cd hw5_mlops_Kuchina_Ekaterina

3. Создать и активировать виртуальное окружение:
python3 -m venv .venv
source .venv/bin/activate

4. Установить зависимости:
pip install -r requirements.txt

5. Получить данные и воспроизвести пайплайн:
dvc pull
dvc repro

6. Запустить MLflow UI:
mlflow ui --backend-store-uri sqlite:///mlflow.db

## Краткое описание пайплайна

Пайплайн состоит из двух стадий.

prepare — загрузка исходного датасета, разбиение на train/test и сохранение подготовленных данных в папку data/processed.

train — обучение модели LogisticRegression, расчет accuracy, сохранение модели и метрик, логирование параметров, метрик и артефактов в MLflow.

## Где смотреть UI MLflow

После запуска команды
mlflow ui --backend-store-uri sqlite:///mlflow.db

интерфейс MLflow доступен по адресу:
http://127.0.0.1:5000

## Используемые инструменты

Git — контроль версий кода  
DVC — контроль версий данных и пайплайна  
MLflow — логирование экспериментов  
scikit-learn — обучение модели  
pandas — обработка табличных данных  
Marimo — пример альтернативы классическому ноутбуку  
Feast — для этапа Feature Store

## Feature Store

В проекте также реализовано хранилище признаков на Feast с использованием PostgreSQL.

Конфигурация Feature Store находится в папке:
feature_repo/feature_repo

Для инициализации и применения конфигурации использовался шаблон Postgres. В качестве online store и offline store используется PostgreSQL, запущенный локально в Docker.

### Как запустить Feature Store

1. Запустить контейнер PostgreSQL:
docker run --name feast-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=feast \
  -p 5433:5432 \
  -d postgres:16

2. Перейти в папку feature repository:
cd feature_repo/feature_repo

3. Применить конфигурацию Feast:
feast apply

4. Материализовать признаки в online store:
feast materialize 2026-04-24T21:00:00 2026-04-26T21:15:00

5. Запустить feature server:
feast serve

### Как проверить endpoint

Пример запроса к endpoint:

curl -X POST "http://127.0.0.1:6566/get-online-features" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      "driver_hourly_stats:conv_rate",
      "driver_hourly_stats:acc_rate",
      "driver_hourly_stats:avg_daily_trips"
    ],
    "entities": {
      "driver_id": [1001, 1003, 1005]
    }
  }'

В ответе возвращаются значения признаков для указанных driver_id. Это подтверждает, что Feature Store не только настроен, но и отдает данные через endpoint.