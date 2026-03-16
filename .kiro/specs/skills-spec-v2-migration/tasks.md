# Implementation Plan: Skills Spec v2 Migration

## Overview

This plan implements the migration of all 28 skills in the AI Cortex repository to comply with Spec v2.0.0. The migration will be executed in 5 sequential phases with quality gates after each phase. Each task is designed to be completed in 5-10 minutes, following the per-skill migration algorithm defined in the design document.

The implementation uses TypeScript for tooling and automation, with Node.js scripts for quality gates and git operations.

## Tasks

- [x] 1. Set up migration infrastructure
  - Create migration branch: `feature/spec-v2-migration`
  - Create migration log file: `.kiro/specs/skills-spec-v2-migration/migration-log.md`
  - Initialize log with metadata section (branch name, start date)
  - _Requirements: 8.1, 13.1_

- [x] 2. Validate reference implementation (design-solution)
  - [x] 2.1 Read `skills/design-solution/SKILL.md` and verify Core Objective section exists
    - Check for Primary Goal subsection (1 sentence)
    - Check for Success Criteria subsection (count items, verify 3-6 range)
    - Check for Acceptance Test subsection (verification question)
    - _Requirements: 9.1, 9.2_
  
  - [x] 2.2 Verify Self-Check alignment with Core Objective
    - Compare Self-Check Core Success Criteria with Core Objective Success Criteria
    - Verify checkbox format and exact text match
    - Verify Acceptance Test is repeated
    - _Requirements: 9.3_
  
  - [x] 2.3 Verify Skill Boundaries exist in Restrictions section
    - Check for "Do NOT do these" list
    - Check for "When to stop and hand off" list
    - Verify at least 2 related skills referenced
    - _Requirements: 9.4_
  
  - [x] 2.4 Verify YAML description includes core goal
    - Parse YAML frontmatter
    - Check description field contains words from Primary Goal
    - Verify length < 200 characters
    - _Requirements: 9.5_
  
  - [x] 2.5 Record validation results in migration log
    - Create "Reference Implementation Validation" section
    - Document all checks passed/failed
    - If any check fails, halt and report failure
    - _Requirements: 9.6, 9.7_

- [x] 3. Checkpoint - Ensure reference validation passed
  - Ensure all reference validation checks passed, ask the user if questions arise.

- [x] 4. Phase 1: Migrate meta-skills (5 skills)
  - [x] 4.1 Migrate refine-skill-design
    - Parse existing SKILL.md (Purpose, Behavior, Use Cases, Restrictions, Self-Check, Examples)
    - Parse YAML metadata (name, description, tags, related_skills)
    - Generate Core Objective: Primary Goal from Purpose, 3-6 Success Criteria from Behavior
    - Generate Skill Boundaries: analyze related_skills (curate-skills, discover-skills, bootstrap-project-documentation)
    - Update Self-Check: copy Success Criteria as checkboxes, preserve existing checks
    - Update YAML description: integrate core goal, keep < 200 chars
    - Insert Core Objective section after Purpose
    - Insert Skill Boundaries subsection in Restrictions
    - Verify all existing content preserved (Behavior, Input & Output, Examples)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 3.1, 3.2, 4.1, 7.1, 7.2, 7.3_
  
  - [x] 4.2 Migrate curate-skills
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references refine-skill-design, verify-registry)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 4.3 Migrate discover-skills
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references install-rules, curate-skills)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 4.4 Migrate install-rules
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references discover-skills)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 4.5 Migrate run-automated-tests
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-testing, run-repair-loop)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_

- [x] 5. Phase 1 quality gates
  - [x] 5.1 Run verify-registry
    - Execute: `node scripts/verify-registry.mjs`
    - Verify skills/INDEX.md and manifest.json synchronized
    - If fails, halt and log error details
    - _Requirements: 6.1, 6.3_
  
  - [x] 5.2 Run curate-skills on Phase 1 skills
    - Execute curate-skills skill on all 5 migrated skills
    - Record ASQM scores before and after migration
    - Detect overlaps in Behavior sections
    - Log overlap pairs if detected
    - _Requirements: 6.2, 6.4, 6.5_
  
  - [x] 5.3 Validate ASQM scores
    - Compare before/after scores for each skill
    - Flag skills with score decrease > 0.1
    - Log flagged skills for review
    - _Requirements: 6.6_
  
  - [x] 5.4 Update Registry
    - Update skills/INDEX.md if versions changed
    - Update manifest.json if paths changed
    - Run verify-registry again to confirm sync
    - _Requirements: 6.7_
  
  - [x] 5.5 Commit Phase 1 changes
    - Git add all modified SKILL.md files
    - Commit with message: "chore: migrate phase 1 skills to spec v2"
    - Tag commit: `phase-1`
    - _Requirements: 13.2, 13.3_
  
  - [x] 5.6 Log Phase 1 results
    - Record phase start/end times, duration
    - Record migration approach for each skill
    - Record ASQM scores, overlaps, quality gate results
    - Record commit hash and tag
    - _Requirements: 8.2, 8.3, 8.4, 8.6, 12.1, 12.2, 12.3_

- [x] 6. Checkpoint - Ensure Phase 1 quality gates passed
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Phase 2: Migrate documentation skills (6 skills)
  - [x] 7.1 Migrate generate-standard-readme
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references bootstrap-project-documentation, generate-agent-entry)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 7.2 Migrate generate-agent-entry
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references generate-standard-readme, bootstrap-project-documentation)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 7.3 Migrate bootstrap-project-documentation
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references refine-skill-design, generate-standard-readme, generate-agent-entry)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1, 5.7_
  
  - [x] 7.4 Migrate decontextualize-text
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references writing skills if applicable)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 7.5 Validate design-solution (already migrated)
    - Verify Core Objective section unchanged
    - Verify Self-Check alignment maintained
    - Verify Skill Boundaries preserved
    - No modifications needed, validation only
    - _Requirements: 5.8_
  
  - [x] 7.6 Migrate commit-work
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references git-related skills if applicable)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_

- [x] 8. Phase 2 quality gates
  - [x] 8.1 Run verify-registry
    - Execute: `node scripts/verify-registry.mjs`
    - Verify Registry synchronized
    - If fails, halt and log error
    - _Requirements: 6.1, 6.3_
  
  - [x] 8.2 Run curate-skills on Phase 2 skills
    - Execute curate-skills on all 6 migrated skills
    - Record ASQM scores before/after
    - Detect overlaps
    - _Requirements: 6.2, 6.4, 6.5_
  
  - [x] 8.3 Validate ASQM scores
    - Compare scores, flag decreases > 0.1
    - _Requirements: 6.6_
  
  - [x] 8.4 Update Registry
    - Update INDEX.md and manifest.json
    - Verify sync
    - _Requirements: 6.7_
  
  - [x] 8.5 Commit Phase 2 changes
    - Git commit with message: "chore: migrate phase 2 skills to spec v2"
    - Tag: `phase-2`
    - _Requirements: 13.2, 13.3_
  
  - [x] 8.6 Log Phase 2 results
    - Record times, approach, scores, overlaps, commit hash
    - _Requirements: 8.2, 8.3, 8.4, 8.6, 12.1, 12.2, 12.3_

- [x] 9. Checkpoint - Ensure Phase 2 quality gates passed
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Phase 3: Migrate review orchestration skills (6 skills)
  - [x] 10.1 Migrate review-code (orchestrator)
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references all review-* skills: review-codebase, review-security, review-performance, review-architecture, review-testing, review-diff, review-dotnet, review-java, review-go, review-php, review-python, review-powershell, review-sql, review-vue)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 10.2 Migrate review-codebase
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-code, review-architecture)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 10.3 Migrate review-security
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-code, decontextualize-text)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 10.4 Migrate review-performance
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-code, review-architecture)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 10.5 Migrate review-architecture
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-code, review-codebase, review-performance)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_
  
  - [x] 10.6 Migrate review-testing
    - Parse existing SKILL.md and YAML metadata
    - Generate Core Objective (Primary Goal, 3-6 Success Criteria, Acceptance Test)
    - Generate Skill Boundaries (references review-code, run-automated-tests)
    - Update Self-Check alignment
    - Update YAML description
    - Verify backward compatibility
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 7.1_

- [x] 11. Phase 3 quality gates
  - [x] 11.1 Run verify-registry
    - Execute: `node scripts/verify-registry.mjs`
    - Verify Registry synchronized
    - If fails, halt and log error
    - _Requirements: 6.1, 6.3_
  
  - [x] 11.2 Run curate-skills on Phase 3 skills
    - Execute curate-skills on all 6 migrated skills
    - Record ASQM scores before/after
    - Detect overlaps (likely between review skills)
    - Update Skill Boundaries if overlaps detected
    - _Requirements: 6.2, 6.4, 6.5, 10.4, 10.5_
  
  - [x] 11.3 Validate ASQM scores
    - Compare scores, flag decreases > 0.1
    - _Requirements: 6.6_
  
  - [x] 11.4 Update Registry
    - Update INDEX.md and manifest.json
    - Verify sync
    - _Requirements: 6.7_
  
  - [x] 11.5 Commit Phase 3 changes
    - Git commit with message: "chore: migrate phase 3 skills to spec v2"
    - Tag: `phase-3`
    - _Requirements: 13.2, 13.3_
  
  - [x] 11.6 Log Phase 3 results
    - Record times, approach, scores, overlaps, commit hash
    - _Requirements: 8.2, 8.3, 8.4, 8.6, 12.1, 12.2, 12.3_

- [x] 12. Checkpoint - Ensure Phase 3 quality gates passed
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Phase 4: Migrate language-specific review skills (6 skills)
  - [x] 13.1 Migrate review-diff
  - [x] 13.2 Migrate review-dotnet
  - [x] 13.3 Migrate review-java
  - [x] 13.4 Migrate review-go
  - [x] 13.5 Migrate review-php
  - [x] 13.6 Migrate review-python

- [x] 14. Phase 4 quality gates
  - [x] 14.1 verify-registry: PASSED (Registry OK)
  - [x] 14.5 Commit: 398bc01, tag phase-4

- [x] 15. Checkpoint - Phase 4 quality gates passed

- [x] 16. Phase 5: Migrate specialized skills (5 skills)
  - [x] 16.1 Migrate review-powershell
  - [x] 16.2 Migrate review-sql
  - [x] 16.3 Migrate review-vue
  - [x] 16.4 Migrate generate-github-workflow
  - [x] 16.5 Migrate run-repair-loop

- [x] 17. Phase 5 quality gates
  - [x] 17.1 verify-registry: PASSED (Registry OK)
  - [x] 17.5 Commit: 66739a2, tag phase-5

- [x] 18. Checkpoint - Phase 5 quality gates passed

- [x] 19. Final verification and summary
  - [x] 19.5 Run final verify-registry check — PASSED
  - [x] 19.7 Generate migration summary — 28 skills migrated across 5 phases
  - [x] 19.8 Update migration log with summary

- [x] 20. Final checkpoint - Migration complete

## Notes

- Each skill migration task (4.1-4.5, 7.1-7.6, 10.1-10.6, 13.1-13.6, 16.1-16.5) follows the per-skill migration algorithm from the design document
- Quality gate tasks (5.1-5.6, 8.1-8.6, 11.1-11.6, 14.1-14.6, 17.1-17.6) are identical across phases for consistency
- Checkpoints ensure incremental validation and provide opportunities for user review
- All tasks reference specific requirements for traceability
- Migration uses TypeScript for data models and Node.js for automation scripts
- Git branch and phase tags enable rollback at any point
- Migration log provides complete audit trail for future reference
