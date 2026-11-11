# Quest HTTP API

The Flask app uses the existing Python quest functions and SQLite helpers.
Start it with `pipenv run python app.py`, then open `http://127.0.0.1:8000/`.
The creation form includes its request token automatically.

## Reading quests

- `GET /quests` returns a JSON array in saved order.
- `GET /quests?status=pending` or `status=completed` filters the array.
- `GET /quests/<id>` returns a saved quest, including all seven standard fields.

Read requests do not need a CSRF token. Empty lists return `[]`. Unknown IDs
return JSON 404; invalid status values and blank IDs return JSON 400.

## Request token

For POST, PATCH, and DELETE, send an `X-CSRF-Token` header with the token for
the same browser session. API clients first call `GET /csrf-token`, keep the
returned session cookie, and use the `csrfToken` value. The token response has
`Cache-Control: no-store`. Missing, invalid, or another session's tokens return
JSON 403. An explicit cross-origin request also returns 403.

The form already obtains its token from the rendered page and adds this header.
For browser JavaScript on the app's own origin:

```javascript
const { csrfToken } = await fetch("/csrf-token").then(response => response.json());

const response = await fetch(`/quests/${questId}`, {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
  },
  body: JSON.stringify({ title: "Go swimming", durationMinutes: 45 }),
});
const updatedQuest = await response.json();
```

Use an actual saved ID as `questId`. New API clients must retain the cookie as
well as the token. A token alone is insufficient. Refresh the page/token after
restarting the app. An optional `SECRET_KEY` environment variable can keep the
session signing key stable across restarts; otherwise a random key is used for
each app instance. Keep that value private. No login or multiuser system is added.

## Creating

`POST /quests` accepts a JSON object with `title` and `durationMinutes`, plus
the request token header. A successful response is the saved pending quest with
status 201. Creation does not award total XP.

## Editing

`PATCH /quests/<id>` accepts a nonempty JSON object containing only `title`,
`durationMinutes`, or both. Titles must be nonblank strings; new titles are
trimmed using the shared input validator. Duration must be a positive whole
number within the validator's safe range. Booleans, fractional numbers, strings,
and null durations are rejected.

- A title edit updates both title and fantasy description using the shared
  rename helper. This HTTP endpoint uses the default description templates.
- A duration-only edit preserves the saved title and description and updates
  duration and planned XP together.
- The existing storage helper saves the edited fields in one transaction and
  checks the current stored status and the quest snapshot used by the request.
  If another request has already changed that snapshot, the stale edit is
  rejected with 409 instead of overwriting the newer values. Reload and retry
  the intended change. No fields are saved if validation or the write fails.
- A successful response is the saved quest JSON with status 200.
- Completed quests or concurrent edit conflicts return 409, unknown IDs 404,
  and invalid payloads 400.

The endpoint does not accept status, completion time, planned reward, or total
XP from the client. Editing never awards XP. Custom template options remain
available in the Python functions; they are not accepted by this HTTP endpoint.

For integration code, `update_pending_quest(path, updated,
expected_quest=original)` enables the same conflict check in the storage layer.
The optional original snapshot must contain the seven standard fields and the
same ID. Existing calls without that keyword keep their previous behavior.
The comparison and update happen under the same SQLite write transaction.

## Deleting

`DELETE /quests/<id>` needs the request token header and no body. It checks the
stored status through the existing transactional helper. Only pending quests
can be deleted. Success returns `{"deleted": "<id>"}` with status 200.

Completed quests return 409. Unknown or already-deleted IDs return 404.
Deletion preserves other quests and total XP.

## Errors and tests

Errors use a JSON `error` field. Database failures return a generic 500 message;
paths, SQL details, and traces are logged server-side rather than returned.

Run `pipenv run python -m pytest` for the full source suite. The Flask app is
not part of the installable Python library, so the CI wheel-only phase excludes
the source-only API and form test modules. It still runs them in the source phase.

These routes do not implement completion or award earned XP yet. Completion
and progress routes are the next backend steps. Editing/deleting controls will
be connected in the later UI steps.
