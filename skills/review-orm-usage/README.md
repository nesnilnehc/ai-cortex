# Review ORM Usage

**Status**: validated

## What it does

Reviews ORM usage patterns at the library level across ORM libraries (Prisma, Entity Framework, SQLAlchemy, Sequelize, TypeORM, Hibernate, Django ORM, ActiveRecord, etc.): N+1 query detection, connection management, migration safety, transaction handling, query efficiency, and model design. Emits a findings list in the standard format. Does not perform scope selection, security, architecture, or raw SQL review.

## When to use

- Orchestrated review: used as the library step when review-code runs for projects using an ORM.
- ORM-only review: when the user wants only ORM usage patterns checked across their data layer.
- Pre-PR ORM checklist: ensure N+1 queries, transaction handling, and migration safety are correct.
- Migration review: focused check on migration files for backwards-compatibility and rollback safety.

## Inputs

- Code scope (files, directories, or diff) containing ORM code (models, migrations, repositories, queries), provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=library-orm, Severity, Title, Description, optional Suggestion.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 5     |
| cognitive        | 4     |
| composability    | 5     |
| stance           | 5     |
| **asqm_quality** | 19    |

## Ecosystem

| Field                                 | Value                                                                    |
| :------------------------------------ | :----------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-sql, nesnilnehc/ai-cortex:review-performance |
| market_position                       | differentiated                                                           |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
