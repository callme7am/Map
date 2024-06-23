# GeoAnalyst: Инновационный Сервис для Геоанализа и Подбора Территорий


## Описание проекта

Мы предлагаем инновационный сервис, который автоматизирует процесс поиска, подбора и анализа земельных участков в Москве. Цель проекта — повысить эффективность использования городских территорий и снизить трудозатраты сотрудников Департамента городского имущества (ДГИ).

## Основные преимущества

- **Автоматизация**: Сокращение времени на поиск и анализ территорий благодаря автоматизированным алгоритмам.
- **Удобство**: Интуитивно понятный интерфейс, позволяющий легко выбирать территории в ручном и автоматизированном режимах.
- **Гибкость**: Возможность экспортировать данные в различные форматы для последующего анализа.
- **Аналитика**: Введение архива отчетов для проведения последующей аналитики и оптимизации запросов.
- **Классификация**: Классификация объектов и соотношение их с земельным участком с космоснимков в формате tif.

## Основные функции

1. **Выбор территории**:
   - Ручной выбор территории путем клика по полигонам.
   - Автоматизированный поиск по фильтрам.

2. **Экспорт данных**:
   - Экспорт данных в форматы xlsx, shp для дальнейшей обработки и анализа.

3. **Архив отчетов**:
   - Хранение отчетов для последующего анализа и оптимизации длительных запросов.

4. **Классификация объектов**:
   - Анализ и классификация объектов с использованием космоснимков в формате tif.

## Масштабирование

1. **Дообогащение данных**:
   - **Связь с транспортными моделями**: Интеграция с городскими транспортными моделями для анализа доступности участков и планирования инфраструктуры.
   - **Обработка данных об окружающей среде**: Включение данных о качестве воздуха, уровне шума и других экологических показателях для комплексной оценки земельных участков.

2. **Модуль прогнозирования спроса на земельные участки**:
   - **Прогнозирование рыночных трендов**.
   - **Анализ демографических данных**.

3. **3D-моделирование участков**:
   - Создание 3D-моделей участков с использованием камер и интеграция с IoT-датчиками для сбора данных о местности.

4. **Автоматическая кластеризация объектов**:
   - Использование нейросети для автоматической кластеризации объектов по индивидуальным характеристикам.

## Используемые технологии

- **Python**: Основной язык программирования.
- **FastAPI**: Фреймворк для разработки веб-приложений и API.
- **Docker**: Контейнеризация и оркестрация сервисов.
- **PostgreSQL**: Основная база данных.
- **JavaScript, HTML, CSS**: Для frontend разработки.
- **YOLO**: Модель для анализа изображений в контексте машинного обучения.

## Установка и запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/
    ```
2. Создать файл .env в .docker
3. Скопировать данные из .docker/.env.example в .docker/.env
4. Заполнить данные в .docker/.env
5. Создать файл .env в configs/
6. Скопировать данные из configs/.env.example в backend/configs/.env
7. Заполнить данные в configs/.env
8. Установите зависимости и сборка контейнеров:
    ```bash
    docker-compose up --build
    ```

## Примеры использования

### Интерфейс

#### Авторизация
Войдите в систему с использованием вашего логина и пароля. Сервис использует JWT для обеспечения безопасности доступа.

#### Подбор территорий

1. **Шаг 1**: Войдите в систему под своим логином и паролем.
2. **Шаг 2**: На карте отображаются участки, сформированные сервисом по заранее заданным параметрам.
3. **Шаг 3**: Откройте форму поиска и выберите округ, диапазон площадей и другие параметры.
4. **Шаг 4**: Нажмите кнопку "Подобрать территорию" для отображения подходящих участков на карте.
5. **Шаг 5**: Кликните по подходящему участку для просмотра подробной информации и добавления его в реестр.

#### Экспорт данных

Экспортируйте основные и дополнительные параметры территорий в форматах xlsx/shp для последующего анализа.

## Соответствие с ТЗ
### Выполненные:
1. **Развернут веб-сервис** - [тык](https://194.113.34.22.sslip.io)
2. **Обеспечен вход по логину/паролю** - страница /auth
3. **Сервис предоставляет данные в виде сформированных контуров** - вывод каждой территории в виде layer на карте leaflet
4. **Отображение информации о географическом положении и дополнительных сведений** - popup на каждом layer с доп информацией
5. **Ручная настройка параметров обработки территорий** - настроенные фильтры по всем полям, которые есть в бд у поля
6. **Поиск и выбор определенных территорий по параметрам** - настроенные фильтры по всем полям, которые есть в бд у поля
7. **Сохранение объектов в отдельный слой/реестр** ??
8. **Внесение комментариев по территории из веб-приложения** - возможность вносить комментарии на карте ЗУ
9. **Отображение сведений из пересекаемых картографических слоев** - данный функционал реализован на /intersections
10. **Подсветка выявленных территорий по принципу светофора** ??
11. **Измерение расстояний и площадей** - возможность рисовать линии, прямоугольники и слои для измерение площадей и расстояний
12. **Экспорт выбранных объектов в SHP** - с помощью правой кнопкой мыши выбираться слой(он выделяется красным), если требуется импортировать всю карту, то не надо выбирать не один слой, и потом нажимается экспорт в shp
13. **Экспорт параметров территории в xlsx/doc** - с помощью правой кнопкой мыши выбираться слой(он выделяется красным), если требуется импортировать всю карту, то не надо выбирать не один слой и потом нажимается экспорт в xlsx
14. **Подключение открытых карт (гугл, яндекс)** - подключен leaflet
15. **Ручное исключение/добавление объектов в перечень подобранных территорий** - с помощью правой кнопкой мыши выбираться слой(он выделяется красным)
16. **Архив запросов** - каждый запрос сохраняется, отчет по запросам можно найти на страниц /archive
17. **Поиск земельного участка по кадастровому номеру** - на странице /maps есть отдельное поле
18. **Пересчет системы координат из МСК в WGS-84** - в архиве sql.zip находятся координаты в WGS-84
19. **Выгрузка результата в виде отчета** - реализованно выгрузка в виде отчета xlsx
20. **Подключение сторонних сервисов для получения дополнительной информации** - возможность просмотр панорамы данного layer
21. **Поиск земельного участка по адресу** - на странице /maps есть отдельное поле
22. **Формирование диаграмм/дашбордов на основе данных** - данный функционал находиться на страницу /dashboards
23. **Подсветка пересечений, которые не обрезают, но пересекают территорию** - данный функционал можно найти на странице /intersection
24. **Категоризация территории по космоснимкам** - данный функционал можно найти на странице /space, тестовые данные находятся в test_data

### Невыполненные:(доделать или расписать алгортим как мы бы это реализовали)
1. **Автоматизированное вычленение и подсвечивание длинных/узких территорий**
2. **Нейросеть, выдающая рекомендации по способу вовлечения территории**
3. **Нейросеть для оценки стоимости аренды/продажи** 
4. **Рекомендации по территории**
5. **Выбор территории для анализа от конкретной точки с указанием радиуса**

## Заключение

Наш Сервис предлагает передовые решения для автоматизации процессов поиска, подбора и анализа земельных участков, делая работу сотрудников Департамента городского имущества более эффективной и продуктивной. Присоединяйтесь к нам и начните использовать инновационные инструменты для управления городскими территориями уже сегодня!

