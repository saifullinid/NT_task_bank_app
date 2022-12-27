# NT_task_bank_app
1. Запуск приложения производится путем запуска скрипта start_app.sh:  
sh start_app.sh  
Данная команда развернет два docker контейнера (posgreSQL и само приложение) и зайдет в терминал контейнера с приложением.  
2. Остановка приложения производится путем запуска скрипта stop_app.sh:  
sh stop_app.sh  
3. Доступ к функционалу приложение производится через команду "bank".  
4. Доступные команды:  
Запуск приложения (без запуска приложения остальные команды будут прерываться с соответствующим описанием):  
bank start  
Остановка приложения:  
bank stop  
Регистрация пользователя:  
bank client-registration --client=<'client_name'>  
Удаление пользователя:  
bank client-delete --client=<'client_name'>  
Пополнение счета на сумму:  
bank deposit --client=<'client_name'> --amount=<'amount'> --description=<'description'>  
Снятие со счета суммы:  
bank withdraw --client=<'client_name'> --amount=<'amount'> --description=<'description'>  
Состояние счета по датам:  
bank show-bank-statement --client=<'client_name'> --since=<'date'> --till=<'date'>  
5. Типы входных данных:  
client: str ('John')  
amount: str ('1000', '1000.50'; далее выполнится преобразование типов с проверкой)  
date: str (формат: 'YYYY-MM-DD HH:MM:SS')  
6. Перед выполнением каждой команды будет запрашиваться пароль пользователя, который указан при регистрации.
7. Тесты можно запустить командой:  
pytest tests
