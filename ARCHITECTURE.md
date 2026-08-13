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
[Interface]
      ↓
[Application]
      ↓
[Core / Domain]
      ↓
[Ports / Contracts]
      ↓
[Adapters / Infrastructure]
```

Диаграмма является примером и должна быть адаптирована к реальному проекту.

## 4. Components / Modules

| Модуль | Ответственность | Public Contract | Зависимости |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 5. Core Contracts

Для каждого важного контракта фиксируйте:

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

TBD

## 8. Standalone Mode

Как система запускается и работает независимо: TBD.

## 9. Embedded / Integration Mode

Как система может быть встроена в большую систему: TBD.

## 10. Extension Points

Реальные ожидаемые точки расширения: TBD.

## 11. Configuration

TBD

## 12. Security Boundaries

TBD

## 13. Observability

TBD

## 14. Failure Modes / Recovery

TBD

## 15. Architecture Decisions

См. `docs/decisions/`.

## 16. Known Architectural Debt

- None / TBD
