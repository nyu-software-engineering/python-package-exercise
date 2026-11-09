# NYU Software Engineering Project 3: Team Roles

## Project Overview
Build an RPG-style task planner that turns everyday tasks into fantasy quests. A user enters a task and planned duration, receives a fantasy description, manages quests, and earns XP and levels by completing them.

**Example:** “Study math for 60 minutes” → “Decipher an Ancient Scroll” → complete the quest → earn 60 XP.

## MVP Flow
1. Enter a task title and planned duration in whole minutes.
2. Validate the input and generate a fantasy description while preserving the original task.
3. Save the quest and display it in the quest list.
4. View, edit, or delete a pending quest; mark a quest complete.
5. Award XP once, persist progress, and display the updated XP and level.

**MVP progression rule:** 1 planned minute = 1 XP; start at level 1; level = `1 + floor(total XP / 100)`. Completion is final, and repeated completion requests must never award extra XP.

## Individual Deliverables and Tests

| Team Member | Ownership and Deliverables | Test Responsibilities |
| --- | --- | --- |
| **Yuyang** | Set up the backend, database schema/migrations, persistence helpers, setup instructions, and GitHub CI. | Test backend startup, database setup, and saving/reloading quests and progress. Verify CI passes valid changes and catches failures. |
| **Ali** | Build the quest creation form, submission flow, validation, and error messages. Share validation rules with Sirius. | Test valid submissions, blank titles, missing/zero/negative/fractional/nonnumeric durations, failed requests, and duplicate submission prevention. |
| **Yvonne** | Implement reusable XP and leveling functions, document progression rules, and deliver automated tests. | Test zero XP, normal awards, level boundaries, multiple-level gains, and invalid inputs. Co-own the repeated-completion integration test with Sirius. |
| **Sirius** | Implement quest CRUD APIs, list/detail controls, editing, deletion, and completion; integrate persistence and progression. | Test CRUD, unknown IDs, server-side validation, persistence, and completion. Verify quest status and XP update together and retries never duplicate rewards. |
| **Zihan** | Translate tasks into fantasy descriptions using templates/keywords; provide a generic fallback and integrate with creation/title edits. | Test common and unfamiliar tasks, invalid input, consistent descriptions, and fallback behavior. Confirm original task details remain available. |

## Shared GitHub Workflow
- Create an issue for each feature or bug, with an owner and acceptance criteria.
- Branch from the latest `main`: for example, `feature/xp-leveling` or `fix/quest-validation`.
- Make focused, meaningful commits; link issues in PRs.
- Include a change summary, testing evidence, and integration notes in each PR.
- Require one teammate’s review and passing CI before merging; avoid direct pushes to `main`.
- Sync after merges. Owners maintain their tests; everyone joins the final end-to-end check.

## Integration Notes
- Agree on API routes and payloads first. Quest fields: `id`, `title`, `durationMinutes`, `fantasyDescription`, `status`, `xpReward`, `completedAt`. Persist `totalXP`; derive the level.
- Ali owns the creation interface; Sirius owns CRUD/completion; Yuyang owns infrastructure/database setup. Coordinate shared-file changes through PRs.
- Validate on both client and server. Use Yvonne’s progression module; save completion and its XP award atomically.
- Only pending quests can be edited/deleted. Update descriptions and rewards when inputs change; completed quests are read-only.
- Shared check: create → reload → edit → complete → verify XP/level → retry completion without extra XP. Also test pending-quest deletion.

## Scope Limits
Support one local user, text quests, persistence, template-based descriptions, and simple XP/levels. Exclude authentication, multiplayer, combat, inventory, leaderboards, timers, notifications, and external AI dependencies. Prioritize an integrated demo and setup documentation before visual polish.
