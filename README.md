# Sprint_7 — тесты API «Яндекс Самокат»

Автотесты для учебного API: https://qa-scooter.praktikum-services.ru/docs/



## Структура

Sprint_7/
├── conftest.py                       # фикстуры (создание/удаление тестовых данных)
├── utils.py                          # константы, генерация данных курьера и заказа
├── pytest.ini
├── requirements.txt
└── tests/
    ├── test_courier_create.py        # создание курьера
    ├── test_courier_login.py         # логин курьера
    ├── test_courier_delete.py        # удаление курьера
    ├── test_order_create.py          # создание заказа (параметризация по цвету)
    ├── test_orders_list.py           # список заказов
    ├── test_order_accept.py          # принятие заказа курьером
    └── test_order_get_by_track.py    # получение заказа по номеру
