# GitHub Setup

После создания нового проекта из шаблона рекомендуется один раз настроить GitHub UI.

## 1. Template Repository

Для самого мастер-шаблона включите:

`Settings → General → Template repository`

После этого новые репозитории удобно создавать через **Use this template**.

До публичного переиспользования выберите лицензию мастер-шаблона. В каждом созданном проекте отдельно подтвердите, замените или удалите унаследованный `LICENSE`; AI-агент не должен выбирать лицензию без решения владельца.

## 2. Labels

Labels классифицируют работу, но не показывают её этап выполнения. Используйте только три измерения:

- `type:*` — что это за работа;
- `priority:*` — насколько она срочная;
- `area:*` — какую часть проекта затрагивает.

Рекомендуемый минимальный набор custom labels:

```text
type:feature
type:bug
type:implementation
type:technical-proposal
type:research

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

После triage назначайте ровно один `type:*`; `priority:*` и `area:*` добавляйте только когда они полезны. Не создавайте `status:*`: канонический статус хранится в поле `Status` GitHub Project.

Issue Forms намеренно не ссылаются на custom labels. Поле `labels` в форме применяет только уже существующие labels и не создаёт их, а набор labels нового репозитория может отличаться от мастер-шаблона. Сначала создайте нужные labels в `Issues → Labels`, затем при желании добавьте их автоматическое назначение. Не обязательно создавать весь список — адаптируйте `area:*` и уровни priority под проект.

## 3. GitHub Project

Создайте Project и используйте его single-select поле `Status` как единственный источник истины для workflow. Рекомендуемые значения:

```text
Triage
Needs Research
Ready
In Progress
In Review
Done
Deferred
Rejected
```

Основной поток:

```text
Triage → Ready → In Progress → In Review → Done
       ↘ Needs Research ↗
       ↘ Deferred / Rejected
```

- `Triage` — новый Issue ещё не получил решения;
- `Needs Research` — решение отложено до получения конкретных данных;
- `Ready` — работа одобрена и достаточно определена для планирования;
- `Deferred` и `Rejected` — конечное решение фиксируется комментарием с причиной.

Статус назначает и меняет владелец проекта или ответственный за triage. Автор Issue не выбирает governance status в форме.

Полезные дополнительные поля:

```text
Stage
Complexity
User Value
Expected Demand
Architecture Risk
Owner
Target Release
```

Сделайте `Stage` single-select полем со значениями из `PROJECT_PLAN.md`. Для `Implementation Task` оно должно совпадать со Stage, выбранным в Issue Form; при последующем переносе задачи текущим значением считается поле Project. Не дублируйте `Priority` и `Area` полями Project, если они уже представлены labels.

Настройте встроенное automation правило Project как минимум для добавления нового Issue в `Triage`. Перевод в `Ready`, `Deferred` и `Rejected` оставьте ручным решением, чтобы автоматизация не подменяла approval. Созданный для согласованной работы `Implementation Task` также сначала попадёт в `Triage`: ответственный должен проверить его основание, scope и acceptance criteria, затем вручную перевести в `Ready` до начала реализации. Отключите встроенный workflow `item closed → Done`, если он может перезаписать `Deferred` или `Rejected`; конечный статус в таком проекте меняйте вручную или собственной автоматизацией, которая сохраняет эти решения.

## 4. Branch Protection

Для `main` рекомендуется:

- require pull request before merging;
- require review для критичных проектов;
- require conversation resolution;
- require status checks после появления CI;
- prohibit force push;
- prohibit branch deletion;
- не разрешать прямые изменения без явной причины.

Не включайте required checks, которых ещё не существует — это может заблокировать development workflow.

Для solo-проекта обязательное чужое approval может создать тупик; используйте PR, conversation resolution и проверки без требования недоступного ревьюера. Для командного проекта настройте минимум одно approval и при необходимости CODEOWNERS.

## 5. Merge Strategy

Для большинства небольших/средних проектов удобно использовать squash merge для чистой истории PR. Если выбран этот профиль, оставьте включённым только squash merge, формируйте итоговый commit из заголовка PR и включите автоматическое удаление ветки после merge. Если проект требует сохранения granular commits, разрешённые стратегии явно фиксируются в `CONTRIBUTING.md` и настройках репозитория.

## 6. Issues

Blank Issues отключены для обычных авторов: выбирайте подходящую форму из `.github/ISSUE_TEMPLATE/`. Пользователи с правом записи всё равно могут видеть вариант blank issue для maintainers, а обязательность полей Issue Forms применяется GitHub только в публичных репозиториях; это ограничение интерфейса, а не полная enforcement-граница. Если появляется устойчивый новый тип запроса, добавьте отдельную форму вместо включения свободного ввода.

Lifecycle Issue:

1. Автор создаёт `Feature Request`, `Bug Report`, `Technical Proposal` или `Research / Spike` без выбора статуса.
2. Ответственный добавляет Issue в Project, ставит `Status = Triage` и назначает labels классификации.
3. После решения статус меняется на `Ready`, `Needs Research`, `Deferred` или `Rejected`; для двух последних вариантов причина фиксируется комментарием.
4. Для согласованной реализации создаётся `Implementation Task` со ссылкой на исходный Issue/ADR/план, Stage, scope, dependencies, acceptance criteria и способом проверки; после проверки ответственный вручную переводит его из автоматического `Triage` в `Ready`.
5. Только `Implementation Task` со статусом `Ready` можно взять в работу; выполнение проходит через `In Progress → In Review → Done`.

Сохраняйте deferred/rejected Issues как историю решений. Не дублируйте поле `Status` с помощью labels, текстовых маркеров в заголовке или dropdown-полей Issue Form.
