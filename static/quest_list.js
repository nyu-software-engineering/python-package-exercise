const list = document.getElementById("quest-list");
const filter = document.getElementById("quest-filter");
const listMessage = document.getElementById("list-message");
const detail = document.getElementById("quest-detail");
const detailMessage = document.getElementById("detail-message");
const progressSummary = document.getElementById("progress-summary");
const progressMessage = document.getElementById("progress-message");
const actionMessage = document.getElementById("action-message");
const editForm = document.getElementById("quest-edit-form");
const actions = document.getElementById("quest-actions");
const deleteConfirmation = document.getElementById("delete-confirmation");
const creationForm = document.getElementById("quest-form");
let selectedQuest = null;
let actionPending = false;
let needsReload = false;
let listRequest = 0;
let detailRequest = 0;
let progressRequest = 0;

function clearDetail() {
  detailRequest += 1;
  detail.hidden = true;
  detailMessage.textContent = "";
  selectedQuest = null;
  needsReload = false;
  editForm.hidden = true;
  deleteConfirmation.hidden = true;
  actions.hidden = true;
  document.getElementById("completed-note").hidden = true;
}

function showDetail(quest) {
  selectedQuest = quest;
  needsReload = false;
  editForm.hidden = true;
  deleteConfirmation.hidden = true;
  actions.hidden = quest.status !== "pending";
  document.getElementById("completed-note").hidden = quest.status !== "completed";
  for (const button of actions.querySelectorAll("button")) button.disabled = actionPending;
  document.getElementById("save-quest").disabled = actionPending;
  document.getElementById("confirm-delete").disabled = actionPending;
  document.getElementById("detail-title").textContent = quest.title;
  document.getElementById("detail-description").textContent = quest.fantasyDescription;
  document.getElementById("detail-duration").textContent = `${quest.durationMinutes} minutes`;
  document.getElementById("detail-status").textContent = quest.status === "completed" ? "Completed" : "Pending";
  document.getElementById("detail-reward").textContent = `${quest.xpReward} XP`;
  document.getElementById("detail-id").textContent = quest.id;
  const completed = document.getElementById("detail-completed");
  completed.replaceChildren();
  if (quest.completedAt) {
    const time = document.createElement("time");
    time.dateTime = quest.completedAt;
    const date = new Date(quest.completedAt);
    time.textContent = Number.isNaN(date.getTime()) ? quest.completedAt : date.toLocaleString();
    completed.append(time);
  } else {
    completed.textContent = "Not completed";
  }
  detail.hidden = false;
  document.getElementById("detail-heading").focus();
}

async function loadDetail(questId) {
  if (actionPending) return;
  clearDetail();
  actionMessage.textContent = "";
  const requestNumber = detailRequest;
  detailMessage.textContent = "Loading details…";
  try {
    const response = await fetch(`/quests/${encodeURIComponent(questId)}`, { cache: "no-store" });
    if (!response.ok) {
      if (requestNumber !== detailRequest) return;
      detailMessage.textContent = response.status === 404
        ? "Quest not found. Refresh the list and try again."
        : "Could not load details. Try View details again.";
      return;
    }
    const quest = await response.json();
    if (requestNumber !== detailRequest) return;
    showDetail(quest);
    detailMessage.textContent = "Quest details loaded.";
  } catch {
    if (requestNumber !== detailRequest) return;
    detailMessage.textContent = "Could not load details. Try View details again.";
  }
}

function showQuests(quests) {
  list.replaceChildren();
  for (const quest of quests) {
    const row = document.createElement("li");
    const title = document.createElement("h3");
    title.textContent = quest.title;
    title.dir = "auto";
    const information = document.createElement("p");
    const status = quest.status === "completed" ? "Completed" : "Pending";
    information.textContent = `${status} | ${quest.durationMinutes} minutes | ${quest.xpReward} XP`;
    const view = document.createElement("button");
    view.type = "button";
    view.textContent = "View details";
    view.setAttribute("aria-label", `View details for ${quest.title}`);
    view.addEventListener("click", () => loadDetail(quest.id));
    row.append(title, information, view);
    list.append(row);
  }
}

async function loadQuests(keepDetail = false) {
  if (actionPending && !keepDetail) return;
  const requestNumber = ++listRequest;
  const status = filter.value;
  if (!keepDetail) clearDetail();
  listMessage.textContent = "Loading quests…";
  list.setAttribute("aria-busy", "true");
  for (const button of list.querySelectorAll("button")) button.disabled = true;
  try {
    const url = status ? `/quests?status=${encodeURIComponent(status)}` : "/quests";
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error("Could not load quests.");
    const quests = await response.json();
    if (requestNumber !== listRequest) return;
    if (!keepDetail) clearDetail();
    showQuests(quests);
    if (quests.length === 0) {
      listMessage.textContent = status ? `No ${status} quests.` : "No quests yet. Create one to get started.";
    } else {
      listMessage.textContent = `${quests.length} ${quests.length === 1 ? "quest" : "quests"} shown.`;
    }
  } catch {
    if (requestNumber !== listRequest) return;
    listMessage.textContent = "Could not load quests. The list has not been updated. Try Refresh quests.";
  } finally {
    if (requestNumber === listRequest) {
      list.setAttribute("aria-busy", "false");
      for (const button of list.querySelectorAll("button")) button.disabled = actionPending;
    }
  }
}

async function loadProgress() {
  const requestNumber = ++progressRequest;
  progressMessage.textContent = "";
  try {
    const response = await fetch("/progress", { cache: "no-store" });
    if (!response.ok) throw new Error("Could not load progress.");
    const progress = await response.json();
    if (requestNumber !== progressRequest) return;
    progressSummary.textContent = `${progress.totalXP} XP | Level ${progress.level}`;
  } catch {
    if (requestNumber !== progressRequest) return;
    if (progressSummary.textContent === "Loading progress…") progressSummary.textContent = "Progress unavailable";
    progressMessage.textContent = "Could not update progress. Try Refresh quests.";
  }
}

function refreshPlanner() {
  if (actionPending) return;
  return Promise.all([loadQuests(), loadProgress()]);
}

function canChangeQuest() {
  if (actionPending || needsReload || !selectedQuest || selectedQuest.status !== "pending") return false;
  if (creationForm.querySelector('button[type="submit"]').disabled) {
    actionMessage.textContent = "Wait for the new quest to finish saving.";
    return false;
  }
  return true;
}

function setActionBusy(busy) {
  actionPending = busy;
  actions.setAttribute("aria-busy", String(busy));
  filter.disabled = busy;
  document.getElementById("refresh-quests").disabled = busy;
  for (const field of creationForm.querySelectorAll("input, button")) field.disabled = busy;
  for (const field of editForm.querySelectorAll("input, button")) field.disabled = busy;
  for (const button of actions.querySelectorAll("button")) button.disabled = busy || needsReload;
  document.getElementById("save-quest").disabled = busy || needsReload;
  document.getElementById("confirm-delete").disabled = busy || needsReload;
  document.getElementById("cancel-delete").disabled = busy;
  for (const button of list.querySelectorAll("button")) {
    button.disabled = busy || list.getAttribute("aria-busy") === "true";
  }
}

function showEditErrors(errors = {}) {
  for (const name of ["title", "minutes"]) {
    const field = document.getElementById(`edit-${name}`);
    document.getElementById(`edit-${name}-error`).textContent = errors[name] || "";
    field.setAttribute("aria-invalid", String(Boolean(errors[name])));
  }
}

async function changeQuest(method, payload) {
  if (!canChangeQuest()) return;
  const questId = selectedQuest.id;
  setActionBusy(true);
  progressRequest += 1;
  actionMessage.textContent = "Saving changes…";
  const options = { method, headers: { "X-CSRF-Token": creationForm.dataset.csrfToken } };
  if (payload) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(payload);
  }
  let deleted = false;
  try {
    const suffix = method === "POST" ? "/complete" : "";
    const response = await fetch(`/quests/${encodeURIComponent(questId)}${suffix}`, options);
    if (!response.ok) {
      if (response.status === 403) {
        actionMessage.textContent = "Your page session expired. Reload the page and try again.";
      } else if (response.status === 404) {
        clearDetail();
        actionMessage.textContent = "This quest no longer exists. Refresh the list.";
      } else if (response.status === 409) {
        needsReload = true;
        actionMessage.textContent = "Quest changed or is no longer pending. Refresh quests before trying again.";
      } else {
        throw new Error("Quest change failed.");
      }
      return;
    }
    const result = await response.json();
    if (method === "DELETE") {
      deleted = true;
      clearDetail();
      actionMessage.textContent = "Quest deleted.";
    } else if (method === "PATCH") {
      showDetail(result);
      actionMessage.textContent = "Quest updated.";
    } else {
      showDetail(result.quest);
      progressSummary.textContent = `${result.totalXP} XP | Level ${result.level}`;
      actionMessage.textContent = result.awardedXP === 0
        ? "Quest was already completed. No extra XP awarded."
        : `Quest completed. ${result.awardedXP} XP awarded.`;
    }
    await Promise.all([loadQuests(true), loadProgress()]);
  } catch {
    actionMessage.textContent = method === "POST"
      ? "Could not confirm completion. Refresh quests or try again."
      : "Could not save changes. Your inputs have been kept. Try again.";
  } finally {
    setActionBusy(false);
    if (deleted) document.getElementById("refresh-quests").focus();
  }
}

document.getElementById("edit-quest").addEventListener("click", () => {
  if (!canChangeQuest()) return;
  showEditErrors();
  document.getElementById("edit-title").value = selectedQuest.title;
  document.getElementById("edit-minutes").value = selectedQuest.durationMinutes;
  editForm.hidden = false;
  deleteConfirmation.hidden = true;
  document.getElementById("edit-title").focus();
});

editForm.addEventListener("submit", event => {
  event.preventDefault();
  if (!canChangeQuest()) return;
  const titleText = document.getElementById("edit-title").value;
  const title = titleText.trim();
  const minutesText = document.getElementById("edit-minutes").value.trim();
  const durationMinutes = Number(minutesText);
  const errors = {};
  if (!title) errors.title = "Enter a quest title.";
  if (!/^[0-9]+$/.test(minutesText) || !Number.isSafeInteger(durationMinutes) || durationMinutes <= 0) {
    errors.minutes = "Enter a positive whole number of minutes.";
  }
  showEditErrors(errors);
  if (Object.keys(errors).length) {
    document.getElementById(errors.title ? "edit-title" : "edit-minutes").focus();
    return;
  }
  const payload = {};
  if (titleText !== selectedQuest.title && title !== selectedQuest.title) payload.title = title;
  if (durationMinutes !== selectedQuest.durationMinutes) payload.durationMinutes = durationMinutes;
  if (!Object.keys(payload).length) {
    actionMessage.textContent = "No changes to save.";
    return;
  }
  changeQuest("PATCH", payload);
});

document.getElementById("cancel-edit").addEventListener("click", () => {
  if (actionPending) return;
  editForm.hidden = true;
  document.getElementById(needsReload ? "refresh-quests" : "edit-quest").focus();
});
document.getElementById("delete-quest").addEventListener("click", () => {
  if (!canChangeQuest()) return;
  editForm.hidden = true;
  deleteConfirmation.hidden = false;
  document.getElementById("cancel-delete").focus();
});
document.getElementById("cancel-delete").addEventListener("click", () => {
  if (actionPending) return;
  deleteConfirmation.hidden = true;
  document.getElementById(needsReload ? "refresh-quests" : "delete-quest").focus();
});
document.getElementById("confirm-delete").addEventListener("click", () => {
  if (!deleteConfirmation.hidden) changeQuest("DELETE");
});
document.getElementById("complete-quest").addEventListener("click", () => {
  if (!editForm.hidden) {
    actionMessage.textContent = "Save or cancel your edit before completing the quest.";
    return;
  }
  changeQuest("POST");
});

filter.addEventListener("change", () => loadQuests());
document.getElementById("refresh-quests").addEventListener("click", refreshPlanner);
document.getElementById("quest-form").addEventListener("quest:created", refreshPlanner);
refreshPlanner();

