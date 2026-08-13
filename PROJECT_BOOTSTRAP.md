# PROJECT BOOTSTRAP

> Исходный паспорт нового проекта. Заполняется владельцем проекта и уточняется совместно с разработчиком/AI-агентом. Неизвестные данные помечайте `TBD`. Будущий функционал здесь является гипотезой, пока не прошёл оценку и одобрение.

## 1. Identity

**Название:** `[PROJECT_NAME]`

**Краткое описание:**  
`TBD`

**Основная цель:**  
`TBD`

**Кто будет использовать:**  
`TBD`

## 2. Problem Statement

**Какую проблему решаем:**  
`TBD`

**Как она решается сейчас:**  
`TBD`

**Что не устраивает в текущем решении:**  
`TBD`

**Как выглядит успешный результат:**  
`TBD`

## 3. Scope

### Входит в проект

- TBD

### Не входит

- TBD

### Возможный будущий функционал

- TBD

> После инициализации существенные идеи должны быть перенесены в отдельные GitHub Feature Requests.

## 4. Пользователи и роли

| Роль | Кто это | Основные возможности |
|---|---|---|
| TBD | TBD | TBD |

## 5. Core Use Cases

### UC-01 — `[название]`

**Actor:** TBD  
**Trigger:** TBD  
**Основной сценарий:** TBD  
**Ожидаемый результат:** TBD

## 6. Functional Requirements

### FR-001 — `[требование]`

Описание: TBD

**Acceptance Criteria:**

- TBD

## 7. Non-Functional Requirements

**Performance:** TBD  
**Reliability:** TBD  
**Security:** TBD  
**Scalability:** TBD  
**Availability:** TBD  
**Compatibility:** TBD  
**Maintainability:** TBD

## 8. Constraints

**Технологические:** TBD  
**Инфраструктурные:** TBD  
**Финансовые:** TBD  
**Сроки:** TBD  
**Legal/Regulatory:** TBD

## 9. Existing Environment

```text
Servers: TBD
Databases: TBD
APIs: TBD
Domains: TBD
Authentication: TBD
Networks: TBD
External Services: TBD
```

## 10. External Integrations

| Система | Назначение | Интерфейс | Статус |
|---|---|---|---|
| TBD | TBD | API/Webhook/Event/etc | idea |

## 11. Data

**Основные сущности:** TBD  
**Источники:** TBD  
**Хранение:** TBD  
**Retention:** TBD  
**Backup:** TBD  
**Sensitive data:** TBD

## 12. Предпочтения по стеку

Если есть обязательные или желательные технологии — указать здесь. Если нет, агент должен предложить минимально сложный стек, соответствующий требованиям.

```text
Language: TBD
Framework: TBD
Database: TBD
Runtime/Hosting: TBD
Other constraints: TBD
```

## 13. Standalone Mode

Как проект должен работать самостоятельно:

```text
Startup: TBD
Configuration: TBD
Storage: TBD
Auth: TBD
External interfaces: TBD
```

## 14. Embedded / Integration Mode

Как проект потенциально может стать компонентом большей системы:

```text
Integration contract: TBD
Lifecycle: TBD
Configuration: TBD
Data exchange: TBD
```

## 15. Extension Points

Вероятные точки расширения, которые стоит учитывать, но не обязательно реализовывать заранее:

- Providers: TBD
- Adapters: TBD
- Plugins: TBD
- Integrations: TBD
- Storage: TBD

## 16. Working Skeleton

Опишите минимальный end-to-end путь, который должен заработать раньше сложной функциональности.

```text
Input
↓
Interface/API
↓
Application
↓
Core
↓
Storage/External Adapter
↓
Result
```

### Skeleton Acceptance Criteria

- [ ] проект запускается;
- [ ] конфигурация работает;
- [ ] главный end-to-end сценарий проходит;
- [ ] базовые ошибки обрабатываются;
- [ ] есть logging;
- [ ] есть smoke/health check;
- [ ] есть инструкция запуска.

## 17. MVP

### Обязательно

- TBD

### Желательно

- TBD

### Не входит в MVP

- TBD

## 18. Deployment

**Environment:** TBD  
**Deployment method:** TBD  
**Rollback:** TBD  
**Backup:** TBD

## 19. Testing Expectations

**Unit:** TBD  
**Integration:** TBD  
**E2E:** TBD  
**Smoke:** TBD  
**Manual verification:** TBD

## 20. Observability

**Logs:** TBD  
**Metrics:** TBD  
**Health checks:** TBD  
**Alerts:** TBD

## 21. Known Risks

| Риск | Вероятность | Влияние | План |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 22. Open Questions

1. TBD
2. TBD

Не блокирующие вопросы не должны мешать созданию Working Skeleton.

## 23. Definition of Project Success

- TBD

## 24. Что должен сделать агент после bootstrap

После анализа этого файла агент должен:

1. выявить существенные противоречия и критические пробелы;
2. зафиксировать разумные допущения;
3. определить MVP и Working Skeleton;
4. предложить архитектурные границы и основные модули;
5. определить integration contracts;
6. разбить реализацию на этапы;
7. обновить `ARCHITECTURE.md`, `PROJECT_PLAN.md` и `ROADMAP.md`;
8. сформировать первоначальный backlog;
9. отделить утверждённый scope от будущих идей;
10. создать необходимые ADR;
11. только после этого начать реализацию Stage 0 / Working Skeleton.