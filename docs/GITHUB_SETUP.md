# GitHub Setup

После создания нового проекта из шаблона рекомендуется один раз настроить GitHub UI.

## 1. Template Repository

Для самого мастер-шаблона включите:

`Settings → General → Template repository`

После этого новые репозитории удобно создавать через **Use this template**.

## 2. Labels

Рекомендуемые custom labels:

```text
type:feature
type:improvement
type:technical-debt
type:research

status:idea
status:needs-review
status:under-review
status:approved
status:planned
status:in-progress
status:implemented
status:deferred
status:rejected
status:needs-research

priority:critical
priority:high
priority:medium
priority:low

area:core
area:api
area:frontend
area:integration
area:security
area:infrastructure
```

Не обязательно создавать все labels заранее — оставьте только полезные конкретному проекту.

## 3. GitHub Project

Рекомендуемый workflow:

```text
Ideas
↓
Needs Review
↓
Research
↓
Approved
↓
Planned
↓
In Development
↓
Review
↓
Done
```

Полезные поля:

```text
Priority
Stage
Area
Complexity
User Value
Expected Demand
Architecture Risk
Owner
Target Release
```

## 4. Branch Protection

Для `main` рекомендуется:

- require pull request before merging;
- require review для критичных проектов;
- require status checks после появления CI;
- prohibit force push;
- не разрешать прямые изменения без явной причины.

Не включайте required checks, которых ещё не существует — это может заблокировать development workflow.

## 5. Merge Strategy

Для большинства небольших/средних проектов удобно использовать squash merge для чистой истории PR. Если проект требует сохранения granular commits, решение фиксируется в `CONTRIBUTING.md`.

## 6. Issues

Используйте формы из `.github/ISSUE_TEMPLATE/` и сохраняйте rejected/deferred идеи как историю продуктовых решений.