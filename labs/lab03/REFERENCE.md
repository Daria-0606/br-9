# Ledger: справка для ЛР3

Журнал хранит неизменяемые записи движения денег. Новый entry_id создаёт новую запись; повторный ID не заменяет старую.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `LedgerEntry(entry_id, transaction_id, account_id, amount, entry_type, reverses_entry_id=None)` | `entry_id`, `transaction_id`, `account_id`, `amount`, `entry_type`, `reverses_entry_id`, `signed_amount()` | `app/domain/ledger.py` |
| `PostingRule()` | `check(entry)` | `app/domain/posting_rules.py` |
| `AllowedEntryTypeRule(types)` | `check(entry)` | `app/domain/posting_rules.py` |
| `MaximumEntryAmountRule(maximum)` | `check(entry)` | `app/domain/posting_rules.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `LedgerService(repository, rules=())` |
| `record` | `record(entry)` |
| `entries_for_transaction` | `entries_for_transaction(transaction_id)` |
| `signed_total` | `signed_total(account_id, code)` |
| `record_debit` | `record_debit(entry_id, transaction_id, account_id, amount)` |
| `record_credit` | `record_credit(entry_id, transaction_id, account_id, amount)` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

Состав исполнителей в этой заготовке задан. Функция сборки уже готова; `app/services/assembly.py` не меняется. Задача — реализовать общий вызов и распределить поведение между указанными объектами.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`CheckResult(True)` означает разрешение. `CheckResult(False, code)` означает отказ, а не изменение статуса объекта. Некорректный тип результата правила вызывает `INVALID_RESULT`. При записи или списании сервис преобразует предусмотренный отказ в `DomainError` до изменения данных.

`Money` хранит `Decimal` и валюту. Для учебных данных используются EUR и USD. Заданная сумма создаётся готовой `money("10", "EUR")`; арифметика выполняется готовыми методами Money. Курс и коэффициент не округляются как денежная сумма. В Account денежный модуль — `app/domain/money.py`, в остальных вариантах он предоставлен в `app/support/`.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab03`.
