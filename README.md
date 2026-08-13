# AI Project Template

Универсальный шаблон GitHub-репозитория для проектов, которые разрабатываются человеком совместно с AI Coding Agent.

Цель шаблона — сделать разработку последовательной, проверяемой и передаваемой: другой разработчик или другой AI-агент должен быстро понять, что строится, почему архитектура устроена именно так, что уже работает, что запланировано и как безопасно продолжить работу.

## Основные принципы

- **Skeleton First** — сначала минимальный рабочий каркас, затем функциональные модули.
- **Incremental Delivery** — после каждого этапа проект остаётся работоспособным.
- **Modular / Composable Architecture** — проект может работать самостоятельно, встраиваться в более крупную систему и подключать внешние модули через явные контракты.
- **GitHub as Source of Truth** — код, решения, документация, backlog и история развития живут в репозитории.
- **Idea != Task** — идея будущей функции не является разрешением на её реализацию.
- **Reviewability** — изменения должны быть понятны человеку, который не участвовал в их написании.

## Как начать новый проект

1. Создайте новый репозиторий из этого template repository.
2. Заполните `PROJECT_BOOTSTRAP.md` настолько подробно, насколько известна задача. Неизвестное помечайте `TBD`.
3. Передайте AI Coding Agent инструкцию из `PROJECT_INIT_PROMPT.md`.
4. Агент должен изучить `AGENTS.md`, сформировать архитектуру, этапы и первоначальный backlog до начала большой разработки.
5. Сначала реализуется Working Skeleton, затем функциональность наращивается отдельными этапами и PR.

## Ключевые файлы

- `AGENTS.md` — постоянные правила для AI Coding Agent.
- `PROJECT_BOOTSTRAP.md` — исходный паспорт конкретного проекта.
- `PROJECT_INIT_PROMPT.md` — готовая команда для инициализации проекта агентом.
- `PROJECT_PLAN.md` — этапы реализации и критерии готовности.
- `ARCHITECTURE.md` — актуальная архитектура и границы модулей.
- `ROADMAP.md` — только принятые направления развития.
- `CONTRIBUTING.md` — ветки, коммиты, PR и проверки.
- `docs/decisions/` — Architecture Decision Records.
- `docs/proposals/` — предложения будущего функционала и технические идеи.
- `.github/ISSUE_TEMPLATE/` — формы Feature Request, Bug, Technical Proposal и Research Spike.

## Жизненный цикл функции

```text
Idea / Request
      ↓
Feature Request
      ↓
Product + Technical Evaluation
      ↓
Approved / Deferred / Rejected / Needs Research
      ↓
Roadmap / Milestone
      ↓
Implementation Issue
      ↓
Branch → Commits → PR → Review → Merge
      ↓
Documentation / Release
```

## Что настраивается вручную после копирования

GitHub labels, GitHub Project, branch protection и включение режима Template Repository описаны в `docs/GITHUB_SETUP.md`.

Этот шаблон не навязывает конкретный язык или framework. Стек выбирается исходя из задачи и фиксируется в документации проекта.