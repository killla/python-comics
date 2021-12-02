# Публикатор комиксов в сообщество VK

Программа для отправки комиксов с сайта [https://xkcd.com/](https://xkcd.com/) в сообщество VK.

При запуске скачивается случайный комикс и публикуется в сообществе.

### Как установить

Для запуска программы необходим токен для API VK. 

Для генерации токена необходимо:
- Создать [группу](https://vk.com/groups?tab=admin) [VK](https://vk.com/). Или использовать уже созданную, на которую у Вас есть права управления группой.
- Создать `standalone` приложение VK на [странице для разработчиков](https://vk.com/dev). Через это приложение будут поститься картинки на стену.
- Получить `client_id` созданного приложения. При редактировании приложения его client_id отображается в адресной строке.
- Получить личный токен по [инструкции](https://vk.com/dev). 
  - Перейти по ссылке, подставив свой {client_id}`https://oauth.vk.com/authorize?client_id={client_id}&display=page&scope=photos,groups,wall,offline.&response_type=token&v=5.131`
  - Нажать `Разрешить`
  - Сохранить access_token, который появится в адресной строке

Также необходимо получить id группы VK. Оно отображается в адресной строке после `club`, при переходе в группу.

Личный токен и id группы следует задать в переменные окружения:

`VK_ACCESS_TOKEN` - личный токен

`VK_GROUP_ID` - id группы VK

Python 3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Как запустить
Для запуска программы нужно перейти в данную папку и выполнить команду:

```
python main.py
```

### Результат
Результатом работы программы является публикация одного случайного комикса (картинка и описание комикса) в сообществе VK.

Пример: https://vk.com/club209221952

### Цель проекта
Проект написан в целях изучения API [VK](https://vk.com/).