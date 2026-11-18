# Исходные проверки ЛР5

Успешных проверок: **4**. Ожидаемых падений: **10**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_extra_lab05`
- `tests.test_progression::test_progression_posting_dependency_error_does_not_consume_id`
- `tests.test_progression::test_progression_refused_entry_does_not_reserve_id`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_dependency_error_does_not_append`
- `tests.test_contract::test_duplicate_id_does_not_replace_record`
- `tests.test_contract::test_empty_and_independent_repository`
- `tests.test_contract::test_injection_copy_and_repository_invariants`
- `tests.test_contract::test_policies_used_before_record`
- `tests.test_contract::test_signed_journal_and_order`
- `tests.test_review_contract::test_review_identical_duplicate_and_invalid_policy_cannot_write`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
