const list = document.getElementById("quest-list");
const filter = document.getElementById("quest-filter");
const listMessage = document.getElementById("list-message");
const detail = document.getElementById("quest-detail");
const detailMessage = document.getElementById("detail-message");
const progressSummary = document.getElementById("progress-summary");
const progressMessage = document.getElementById("progress-message");
let listRequest = 0;
let detailRequest = 0;
let progressRequest = 0;

function clearDetail() {
  detailRequest += 1;
  detail.hidden = true;
  detailMessage.textContent = "";
}

function showDetail(quest) {
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
  clearDetail();
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

async function loadQuests() {
  const requestNumber = ++listRequest;
  const status = filter.value;
  clearDetail();
  listMessage.textContent = "Loading quests…";
  list.setAttribute("aria-busy", "true");
  for (const button of list.querySelectorAll("button")) button.disabled = true;
  try {
    const url = status ? `/quests?status=${encodeURIComponent(status)}` : "/quests";
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error("Could not load quests.");
    const quests = await response.json();
    if (requestNumber !== listRequest) return;
    clearDetail();
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
      for (const button of list.querySelectorAll("button")) button.disabled = false;
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
  loadQuests();
  loadProgress();
}

filter.addEventListener("change", loadQuests);
document.getElementById("refresh-quests").addEventListener("click", refreshPlanner);
document.getElementById("quest-form").addEventListener("quest:created", refreshPlanner);
refreshPlanner();
