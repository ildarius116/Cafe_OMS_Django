# Система управления заказами в кафе на фреймворке Django

_Техническое задание:_
```text
1. Разработать полнофункциональное веб-приложение на Django для управления заказами в кафе. Приложение должно позволять добавлять, удалять, искать, изменять и отображать заказы, через Веб-интерфейс.
2. Дополнительно, предоставить API для работы с заказами (добавление, удаление, поиск и т. д.).
```
Полный текст ТЗ можно прочесть здесь: [Техническое задание.docx](%D2%E5%F5%ED%E8%F7%E5%F1%EA%EE%E5%20%E7%E0%E4%E0%ED%E8%E5.docx)

__Доступные адреса (эндпоинты) и функции:__

* `/admin/` - адрес административной панели
* `/` - адрес отображения списка заказов
* `/<int:pk>/` - адрес просмотра и редактирования деталей заказа
* `/<int:pk>/edit/` - адрес просмотра и редактирования статуса заказа
* `/<int:pk>/delete/` - адрес POST-запроса на удаление заказа
* `/new/` - адрес страницы создания нового заказа 
* `/revenue/` - адрес просмотра отчета о выручке
* `/menu-item/new/` - адрес создания элемента (блюда) Меню
* `/api/orders/` - адрес API-функционала CRUD операций с заказами
* `/api/menu-items/` - адрес API-функционала CRUD операций с Меню
* `/api/schema/` - адрес yaml-схемы API-функционала
* `/api/docs/` - адрес swagger-схемы API-функционала
* `/api/redoc/` - адрес redoc-схемы API-функционала


## Примеры:

* #### _Отображение списка заказов:_
* ![orders_list.JPG](README%2Forders_list.JPG)
* #### _Детали заказа:_
* ![order_detals_pending.JPG](README%2Forder_detals_pending.JPG)
* #### _Обновление статуса заказа:_
* ![update_status.JPG](README%2Fupdate_status.JPG)
* #### _Создание нового заказа:_
* ![create_order.JPG](README%2Fcreate_order.JPG)
* #### _Просмотр отчета о выручке:_
* ![revenue.JPG](README%2Frevenue.JPG)
* #### _Создание элемента (блюда) Меню (не было в ТЗ):_
* ![menu_item_add.JPG](README%2Fmenu_item_add.JPG)
* #### _Swagger API:_
* ![api.JPG](README%2Fapi.JPG)


## Порядок запуска:
* Клонировать: `git clone https://github.com/ildarius116/Cafe_OMS_Django`
* Установить зависимости: `pip install -r requirements.txt`
* Применить миграции: `python manage.py migrate`
* Создать суперпользователя (администратора): `python manage.py createsuperuser`
* ```text
    Имя пользователя:
    Адрес электронной почты: (не обязательно)
    Password: 
    Password (again):
    ```
* Запустить сервер: `python manage.py runserver`
* По необходимости, запустить тесты: `python manage.py test`


### _Примечания:_
1. По необходимости, запустить тесты: `python manage.py test`
2. По необходимости, создайте тестовые данные заказов и блюд: `python manage.py createtestitems`
