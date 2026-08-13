# Module Documentation

Для существенного модуля создавайте отдельный документ, если его контракт и поведение невозможно ясно описать рядом с кодом.

Рекомендуемая структура:

```text
# Module: <name>
Purpose:
Responsibilities:
Out of scope:
Public interface:
Inputs/outputs:
Dependencies:
Configuration:
Failure modes:
Tests:
Extension points:
Related ADR/Issues:
```

Модуль должен иметь понятную область ответственности и не требовать знания его внутренней реализации для корректного использования через публичный контракт.