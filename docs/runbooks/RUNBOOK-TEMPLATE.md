# Runbook — [система / сервис / операция]

**Owner:** TBD  
**Last reviewed:** YYYY-MM-DD  
**Last successful test:** YYYY-MM-DD / TBD  
**Sensitivity:** public / internal / restricted

Не помещайте сюда secrets, реальные credentials, чувствительные внутренние адреса или подробности инцидентов. Для закрытых данных используйте безопасные aliases и ссылки на контролируемую систему.

## Purpose and impact

Что делает процедура, когда применяется и кого затрагивает.

## Prerequisites and permissions

- необходимые права и доступы без их значений;
- требуемые инструменты и версии;
- исходное состояние и зависимости;
- источник истины для конфигурации и данных.

## Environments

| Окружение | Безопасный идентификатор | Источник инструкций доступа | Примечания |
|---|---|---|---|
| dev | TBD | TBD | |
| prod | TBD | контролируемая система / TBD | |

## Normal procedure

Для каждого шага укажите платформу, точную команду или действие, ожидаемый результат и условие остановки.

```text
Platform: Bash / PowerShell / application UI / other
Step: TBD
Expected result: TBD
Stop and escalate if: TBD
```

## Verification / health check

```text
Command or procedure: TBD
Expected result: TBD
```

## Logs and diagnostics

- безопасный путь, команда или ссылка: TBD;
- ключевые признаки нормальной работы: TBD;
- первые диагностические проверки: TBD;
- данные, которые запрещено копировать в Issue или публичный чат: TBD.

## Common failures

| Симптом | Вероятная причина | Безопасная диагностика | Действие / stop criteria |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Rollback / recovery

**Rollback trigger:** TBD  
**Procedure:** TBD  
**Verification after rollback:** TBD  
**Escalation:** TBD

## Backup and restore

- что защищается и где находится source of truth: TBD;
- механизм, retention и контроль доступа: TBD;
- последняя успешная проверка восстановления: TBD;
- перед изменением создаваемый versioned rollback snapshot: TBD / N/A с причиной.

Соседняя копия файла на том же носителе может быть rollback snapshot, но не заменяет полноценный backup. Для IaC и immutable infrastructure изменяйте декларативный источник, а не сервер вручную.

## Escalation and incident record

**Кому и при каких условиях эскалировать:** TBD  
**Контролируемая система учёта изменений и инцидентов:** TBD

В runbook хранится ссылка на журнал, а не чувствительные подробности инцидентов.
