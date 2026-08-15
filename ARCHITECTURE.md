# ARCHITECTURE

> Актуальное описание архитектуры проекта. Не превращайте файл в исторический журнал — историю существенных решений храните в ADR.

## 1. System Context

Что представляет собой система, кто её использует и с чем она взаимодействует.

`TBD`

## 2. Architecture Goals

- TBD

## 3. High-Level Diagram

```text
[User/System]
      ↓
[Entry Point]
      ↓
[Application / Core]
      ↓
[Required Storage or Integration (if any)]
```

Диаграмма является примером и должна быть адаптирована к реальному проекту. Не добавляйте слои, порты или адаптеры без подтверждённой необходимости.

## 4. Components / Modules

| Модуль | Ответственность | Public Contract | Зависимости |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 5. Core Contracts

Для каждого важного подтверждённого контракта фиксируйте поля ниже. Если отдельных контрактов не требуется, укажите `N/A` с причиной.

```text
Name:
Purpose:
Inputs:
Outputs:
Errors:
Versioning/Compatibility:
```

## 6. Data Model

TBD

## 7. External Integrations

Опишите только утверждённые интеграции. Если их нет: `N/A — внешние интеграции не входят в принятый scope`.

## 8. Operating Modes

Независимо от выбранного режима ядро бизнес-логики, если оно есть, не зависит от CLI, HTTP, cron или import. Runtime- и environment-specific конфигурация приходит извне, а внешние системы вызываются через явную границу, не напрямую из бизнес-логики. Граница может быть простым модулем или функцией и сама по себе не требует отдельного interface, provider или plugin.

Полноценный режим и его contracts включаются в архитектуру только при наличии подтверждённого use case. Иначе укажите `N/A` и причину.

### Standalone Mode

**Статус:** required / N/A / TBD

**Use case или причина `N/A`:** TBD

**Запуск, конфигурация и границы:** TBD

### Embedded / Integration Mode

**Статус:** required / N/A / TBD

**Use case или причина `N/A`:** TBD

**Контракт, lifecycle и обмен данными:** TBD

## 9. Extension Points

Только утверждённые providers, adapters, plugins или другие точки расширения: TBD / N/A. Не создавать extension API для гипотетического будущего.

## 10. Configuration

TBD

## 11. Security Boundaries

Границы доверия, authentication/authorization, secrets и чувствительные данные: TBD.

## 12. Observability

Логи, health checks, метрики и диагностические данные без раскрытия чувствительной информации: TBD.

## 13. Data Safety / Failure Recovery

Отказы, целостность данных, безопасные миграции, rollback и backup/recovery: TBD / N/A с причиной.

## 14. Architecture Decisions

См. [docs/decisions/](docs/decisions/).

## 15. Known Architectural Debt

- None / TBD
