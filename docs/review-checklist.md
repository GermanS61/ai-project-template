# Code Review Checklist

## Scope

- [ ] PR решает заявленную задачу.
- [ ] Нет скрытого scope creep.
- [ ] Новые идеи вынесены отдельно.

## Architecture

- [ ] Соблюдены существующие module boundaries.
- [ ] Новая связность оправдана.
- [ ] Публичные contracts ясны.
- [ ] Нет ненужного overengineering.
- [ ] Breaking changes явно обозначены.

## Code

- [ ] Код читаемый и поддерживаемый.
- [ ] Имена отражают смысл.
- [ ] Нет лишнего дублирования.
- [ ] Ошибки и edge cases обработаны соразмерно риску.

## Verification

- [ ] Tests релевантны изменению.
- [ ] Lint/typecheck/pre-commit выполнены, если предусмотрены.
- [ ] Smoke/manual verification описаны при необходимости.
- [ ] PR честно указывает непроведённые проверки.

## Security

- [ ] Нет secrets/credentials.
- [ ] Права и внешние inputs обработаны безопасно.
- [ ] Для destructive change есть rollback/backup consideration.

## Documentation / Handoff

- [ ] README/API/architecture/runbook обновлены при необходимости.
- [ ] ADR создан для существенного решения.
- [ ] Следующий разработчик понимает что изменилось и почему.