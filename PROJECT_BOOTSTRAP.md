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

> После инициализации существенные идеи должны быть подготовлены как отдельные GitHub Feature Requests. После разрешённой публикации оставьте здесь только ссылки; канонический workflow хранится в Project `Status`, а не дублируется в этом файле.

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

Указывайте только безопасные aliases и категории. Реальные credentials, секреты, чувствительные внутренние адреса и способы доступа храните в системе с подходящим контролем доступа, а здесь оставляйте ссылку или идентификатор без секрета.

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

| Система | Назначение | Интерфейс | Решение / Issue |
|---|---|---|---|
| TBD | TBD | API/Webhook/Event/etc | Confirmed / N/A / #Issue |

## 11. Data

Не перечисляйте реальные sensitive values или персональные данные. Фиксируйте классы данных, требования и ссылку на контролируемую документацию.

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

## 13. Operating Modes

Выбирайте только режимы, подтверждённые реальным use case. Для неприменимого режима укажите `N/A` и причину.

### Standalone Mode

**Статус:** required / N/A / TBD

**Подтверждённый сценарий или причина `N/A`:** TBD

```text
Startup: TBD
Configuration: TBD
Storage: TBD
Auth: TBD
External interfaces: TBD
```

### Embedded / Integration Mode

**Статус:** required / N/A / TBD

**Подтверждённый сценарий или причина `N/A`:** TBD

```text
Integration contract: TBD
Lifecycle: TBD
Configuration: TBD
Data exchange: TBD
```

## 14. Extension Points

Фиксируйте только расширения, для которых есть утверждённый сценарий. Если их нет: `N/A — подтверждённых extension points нет`. Не создавайте providers, adapters или plugin API «на будущее».

**Статус:** required / N/A / TBD

**Подтверждённый сценарий или причина `N/A`:** TBD

**Необходимые точки расширения и требования совместимости:** TBD

## 15. Working Skeleton

Опишите минимальный end-to-end путь, который должен заработать раньше сложной функциональности.

```text
Input / Trigger
↓
Minimal Implementation Path
↓
Required State or Integration (if any)
↓
Observable Result
```

### Skeleton Acceptance Criteria

- [ ] проект запускается;
- [ ] конфигурация работает;
- [ ] главный end-to-end сценарий проходит;
- [ ] базовые ошибки обрабатываются;
- [ ] есть минимальная воспроизводимая автоматическая или ручная проверка;
- [ ] применены базовые security controls и не раскрываются секреты;
- [ ] есть диагностические логи без чувствительных данных;
- [ ] есть smoke/health check;
- [ ] изменения данных безопасны и проверены; backup/recovery описаны либо обоснованно `N/A`;
- [ ] есть инструкция запуска.

## 16. MVP

### Обязательно

- TBD

### Желательно

- TBD

### Не входит в MVP

- TBD

## 17. Deployment

**Environment:** TBD  
**Deployment method:** TBD  
**Rollback:** TBD  
**Backup:** TBD

## 18. Testing Expectations

**Unit:** TBD  
**Integration:** TBD  
**E2E:** TBD  
**Smoke:** TBD  
**Manual verification:** TBD

## 19. Observability

**Logs:** TBD  
**Metrics:** TBD  
**Health checks:** TBD  
**Alerts:** TBD

## 20. Known Risks

| Риск | Вероятность | Влияние | План |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 21. Open Questions

1. TBD
2. TBD

Не блокирующие вопросы не должны мешать созданию Working Skeleton.

## 22. Definition of Project Success

- TBD

## 23. Что должен сделать агент после bootstrap

После анализа этого файла агент должен:

1. выявить существенные противоречия и критические пробелы;
2. зафиксировать разумные допущения;
3. определить MVP и Working Skeleton;
4. выбрать только подтверждённые режимы работы и архитектурные границы; остальные пометить `N/A` с причиной;
5. определить контракты только для реально требуемых интеграций и расширений;
6. персонализировать `README.md` и `SECURITY.md`, включая команды, конфигурацию и приватный канал для сообщений об уязвимостях;
7. разбить реализацию на этапы с базовыми требованиями к проверке, безопасности, наблюдаемости и сохранности данных; при адаптации этапов синхронизировать варианты Stage в `.github/ISSUE_TEMPLATE/implementation_task.yml` и поле `Stage` GitHub Project;
8. обновить `ARCHITECTURE.md`, `PROJECT_PLAN.md` и `ROADMAP.md`;
9. сформировать первоначальный backlog;
10. отделить утверждённый scope от будущих идей;
11. создать необходимые ADR;
12. завершить Stage 0 — Architecture / Bootstrap и только затем начать Stage 1 — Working Skeleton.
