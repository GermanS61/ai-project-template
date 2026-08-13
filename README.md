# AI Project Template

Универсальный шаблон GitHub-репозитория для проектов, которые разрабатываются человеком совместно с AI Coding Agent.

Цель шаблона — сделать разработку последовательной, проверяемой и передаваемой: другой разработчик или другой AI-агент должен быстро понять, что строится, почему архитектура устроена именно так, что уже работает, что запланировано и как безопасно продолжить работу.

## Основные принципы

- **Skeleton First** — сначала минимальный рабочий каркас, затем функциональные модули.
- **Incremental Delivery** — Stage 0 завершается валидированным проектным контуром, а начиная со Stage 1 после каждого этапа проект остаётся работоспособным.
- **Fit-for-purpose Architecture** — standalone, embedded mode и extension points добавляются только при наличии подтверждённого сценария.
- **GitHub as Source of Truth** — код, решения, документация, backlog и история развития живут в репозитории.
- **Idea != Task** — идея будущей функции не является разрешением на её реализацию.
- **Reviewability** — изменения должны быть понятны человеку, который не участвовал в их написании.

## Как начать новый проект

1. Создайте новый репозиторий из этого template repository.
2. Выберите профиль заполнения [PROJECT_BOOTSTRAP.md](PROJECT_BOOTSTRAP.md): **Lite** для небольшой утилиты или **Standard** для сервиса/системы. Неизвестное помечайте `TBD`, неприменимое — `N/A` с причиной.
3. Передайте AI Coding Agent инструкцию из [PROJECT_INIT_PROMPT.md](PROJECT_INIT_PROMPT.md).
4. На Stage 0 агент персонализирует README/SECURITY, согласует подтверждённые режимы работы, архитектуру, этапы и первоначальный backlog.
5. На Stage 1 реализуется Working Skeleton; затем функциональность наращивается отдельными этапами и PR.

### Профили bootstrap

- **Lite** — заполните Identity, Problem Statement, Scope, Constraints, Working Skeleton, MVP и Testing Expectations. Остальные разделы допускают `N/A` с причиной, но требования безопасности и сохранности данных всё равно оцениваются.
- **Standard** — пройдите все применимые разделы для сервиса, интеграции или проекта с эксплуатационным контуром.

## Ключевые файлы

- [AGENTS.md](AGENTS.md) — постоянные правила для AI Coding Agent.
- [CLAUDE.md](CLAUDE.md) — подключает те же правила в Claude Code без дублирования.
- [PROJECT_BOOTSTRAP.md](PROJECT_BOOTSTRAP.md) — исходный паспорт конкретного проекта.
- [PROJECT_INIT_PROMPT.md](PROJECT_INIT_PROMPT.md) — готовая команда для инициализации проекта агентом.
- [PROJECT_PLAN.md](PROJECT_PLAN.md) — этапы реализации и критерии готовности.
- [ARCHITECTURE.md](ARCHITECTURE.md) — актуальная архитектура и границы модулей.
- [ROADMAP.md](ROADMAP.md) — только принятые направления развития.
- [CONTRIBUTING.md](CONTRIBUTING.md) — ветки, коммиты, PR и проверки.
- [docs/decisions/](docs/decisions/) — Architecture Decision Records.
- [docs/proposals/](docs/proposals/) — предложения будущего функционала и технические идеи.
- [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) — формы Feature Request, Bug, Technical Proposal, Research Spike и Implementation Task.

## Жизненный цикл функции

```text
Idea / Request
      ↓
Feature Request → Status: Triage
      ↓
Product + Technical Evaluation
      ↓
Ready / Needs Research / Deferred / Rejected
      ↓
Roadmap / Milestone (для Ready)
      ↓
Implementation Task → Status: Ready
      ↓
In Progress → PR → In Review → Done
```

## Что настраивается вручную после копирования

После копирования настройте labels, GitHub Project и branch protection по [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md). Режим **Template repository** включается только один раз у мастер-шаблона, а не у каждого созданного проекта.

Этот шаблон не навязывает конкретный язык или framework. Стек выбирается исходя из задачи и фиксируется в документации проекта.

## Лицензия

Перед публичным переиспользованием мастер-шаблона выберите лицензию для его содержимого. При создании нового проекта явно подтвердите, замените или удалите унаследованный `LICENSE` в соответствии с политикой проекта; выбор лицензии не должен выполняться AI-агентом без решения владельца.
