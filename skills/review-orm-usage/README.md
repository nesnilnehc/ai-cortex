# Review ORM Usage

**Status**: Validated

## Purpose

Reviews ORM usage patterns at the library level across ORM libraries (Prisma, Entity Framework, SQLAlchemy, Sequelize, TypeORM, Hibernate, Django ORM, ActiveRecord, and others): N+1 query detection, connection management, migration safety, transaction handling, query efficiency, and model design. Emits a findings list in the standard format. Does not select scope and does not perform security, architecture, or raw SQL review.

## When to use

- Orchestrated review: the library step when orchestrate-code-review runs on a project that uses an ORM.
- ORM-only review: when the user wants ORM usage patterns checked in the data layer and nothing else.
- Pre-PR ORM checklist: confirm N+1 queries, transaction handling, and migration safety are right.
- Migration review: check migration files for backward compatibility and rollback safety.

## Inputs

- A code scope containing ORM code (models, migrations, repositories, queries) (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=library-orm, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-sql, nesnilnehc/ai-cortex:review-performance |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
