## Продавец

### Регистрация

**Endpoint:** `[POST] /supplier/register`

**Входные данные:** объект продавца без ID

**Выходные данные:** созданный объект продавца с ID и JWT токен

### Авторизация

**Endpoint:** `[POST] /supplier/login`

**Входные данные:** логин и пароль

**Выходные данные:** JWT токен

### Просмотр профиля

**Endpoint:** `[GET] /supplier/{id}`

**Входные данные:** JWT токен

**Выходные данные:** объект продавца

### Обновление профиля

**Endpoint:** `[PUT] /supplier/update/{id}`

**Входные данные:** JWT токен и новый объект продавца

**Выходные данные:** обновленный объект продавца

## Покупатель

### Регистрация

**Endpoint:** `[POST] /customer/register`

**Входные данные:** объект покупателя без ID

**Выходные данные:** созданный объект покупателя с ID и JWT токен

### Авторизация

**Endpoint:** `[POST] /customer/login`

**Входные данные:** логин и пароль

**Выходные данные:** JWT токен

### Просмотр профиля

**Endpoint:** `GET /customer/{id}`

**Входные данные:** JWT токен

**Выходные данные:** объект покупателя


### Обновление профиля

**Endpoint:** `PUT /customer/update/{id}`

**Входные данные:** JWT токен и новый объект покупателя

**Выходные данные:** обновленный объект покупателя

## Товары

### Получение всех товаров с витрины

**Endpoint:** `[GET] /items/`

**Входные данные:** JWT токен

**Выходные данные:** Список товаров

### Получение информации о товаре

**Endpoint:** `[GET] /items/{id}`

**Входные данные:** JWT токен, ID товара

**Выходные данные:** Информация о товаре

### Обновление информации о товаре

**Endpoint:** `[PUT] /items/{id}`

**Входные данные:** JWT токен, ID товара, объект товара

**Выходные данные:** Измененный объект товара.

### Добавление товара на витрину

**Endpoint:** `[POST] /items/`

**Входные данные:** JWT токен, объект товара

**Возвращаемые данные:** ID товара и объект товара.

### Снятие товара с витрины

**Endpoint:** `[DELETE] /items/{id}`

**Входные данные:** JWT токен, ID товара

**Возвращаемые данные:** -

### "Избранные" товары

#### Получение всех избранных товаров

**Endpoint:** `[GET] /items/favorite`

**Входные данные:** JWT токен

**Возвращаемые данные:** список избранных товаров пользователя

#### Добавление товара в "избранное"

**Endpoint:** `[POST] /items/{id}/favorite`

**Входные данные:** JWT токен, ID товара

**Выходные данные:** -

#### Удаление товара из "избранное"

**Endpoint:** `[DELETE] /items/{id}/favorite`

**Входные данные:** JWT токен, ID товара

**Выходные данные:** -

## Заказы

### Создание заказа

**Endpoint:** `[POST] /orders/`

**Входные данные:** JWT токен, объект заказа

**Выходные данные:** ID заказа и объект заказа.

### Получение информации о заказе

**Endpoint:** `[GET] /orders/{id}`

**Входные данные:** JWT токен, ID заказа

**Выходные данные:** Объект заказа

### Обновление статуса заказа

**Endpoint:** `[PUT] /orders/{id}/state`

**Входные данные:** JWT токен, ID заказа, новый статус

**Выходные данные:** Измененный объект заказа