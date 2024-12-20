
1)Для запуска соберите контейнер используя файлы из папки `dockerfile` например так:

```docker build -t arma3-wine dockerfile/```

В docker-compose.yml даны некоторые коментарии по настройке. Необходимо отключить двухфакторную аутентификацию в Steam для пользователя от имени которого запускается сервер. Покупать клиента АРМА3 не нужно, поэтому можно создать нового пользователя.

1.1)При первом запуске необходимо установить библиотеки wine, для установки которых нужен GUI, по этому нужно поставить на паузу запуск (PAUSE_START: true)

1.2)Затем запуская по очереди команды в контейнере arma3-wine:

docker-compose exec arma3-wine winetricks vcrun2013

docker-compose exec arma3-wine winetricks vcrun2015

docker-compose exec arma3-wine winetricks d3dx11_43

docker-compose exec arma3-wine winetricks mdac28

и используя Open vnc (http://localhost:6901 from the server by default) 
прожать кнопки далее в появляющихся окнах vnc-сессии

1.3)Остановить контейнер arma3-wine, убрать паузу при запуске (PAUSE_START: false).

2)Запустить контейнер arma3-wine, при запуске/перезапуске будут скачаны/проверены файлы сервера ARMA3, сформированы bat-файлы с учетом настроек докер, cfg-файлов, модов в папке /mods и т.п. и запущен (или запущены несколько, если используются безголовые клиенты) через wine нужный bat файл.

При составлениия использовались два проекта:

https://github.com/BrettMayson/Arma3Server

https://github.com/aaaler/arma3-wine

