# tppo_5121
## lab1_tppo
- для запуска сервера:
```ruby
python3 tppo_server_5121.py 127.0.0.1 12345
```
- для запуска клиента:
```ruby
python3 tppo_client_5121.py 127.0.0.1 12345
```
- Команды для клиента:
  - Установить проценты сдвига полотна:
      ```ruby
      set shift_percent <value>
      ```
  - Установить проценты сдвига пропуска светового потока:
      ```ruby
      set luminous_flux_percent <value>
      ```
  - Получить значения процентов сдвига полотна:
      ```ruby
      get shift_percent
      ```
  - Получить значения процентов пропуска светового потока:
      ```ruby
      get luminous_flux_percent
      ```
  - Получить значения текущей освещенности с внешней стороны.:
      ```ruby
      get current_illumination
      ```
  - Отключить от сервера:
      ```ruby
      exit
      ```

