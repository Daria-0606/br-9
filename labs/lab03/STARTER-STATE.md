# Исходные проверки ЛР3

Успешных проверок: **2**. Ожидаемых падений: **7**.

Не завершены общий интерфейс, алгоритмы исполнителей и основной метод сервиса. Поэтому один незаполненный метод может вызвать несколько падений — это не несколько независимых задач.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_refused_entry_does_not_reserve_id`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_abc_is_abstract`
- `tests.test_contract::test_duplicate_id_does_not_replace_record`
- `tests.test_contract::test_empty_and_independent_repository`
- `tests.test_contract::test_policies_used_before_record`
- `tests.test_contract::test_signed_journal_and_order`
- `tests.test_contract::test_types_and_cap_boundaries`

## Порядок проверки

Из корня проекта: `python check.py lab03`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
