# Runbooks

Runbook описывает эксплуатационные действия так, чтобы их мог выполнить другой разработчик/оператор без знания истории проекта.

Для каждой критичной операции фиксируйте:

```text
Purpose
Prerequisites
Normal procedure
Verification
Common failures
Diagnostics
Rollback / Recovery
Backup implications
Escalation
```

Не помещайте реальные secrets в runbook.

Используйте [RUNBOOK-TEMPLATE.md](RUNBOOK-TEMPLATE.md) как заготовку и адаптируйте команды к платформе и способу развёртывания проекта.
