function readQuestInput(form) {
  const title = form.elements.namedItem("title").value.trim();
  const minutes = form.elements.namedItem("durationMinutes").value.trim();
  const durationMinutes = Number(minutes);
  const errors = {};

  if (!title) {
    errors.title = "Enter a quest title.";
  }

  if (
    !/^[0-9]+$/.test(minutes) ||
    !Number.isSafeInteger(durationMinutes) ||
    durationMinutes <= 0
  ) {
    errors.durationMinutes = "Enter a positive whole number of minutes.";
  }

  return { data: { title, durationMinutes }, errors };
}

function showFieldErrors(form, errors) {
  for (const name of ["title", "durationMinutes"]) {
    const field = form.elements.namedItem(name);
    const message = errors[name] ?? "";
    document.getElementById(`${field.id}-error`).textContent = message;
    field.setAttribute("aria-invalid", String(Boolean(message)));
  }
}

async function submitQuest(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  const status = document.getElementById("quest-status");

  if (button.disabled) return;

  const { data, errors } = readQuestInput(form);
  status.textContent = "";
  showFieldErrors(form, errors);

  if (Object.keys(errors).length > 0) return;

  button.disabled = true;

  try {
    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": form.dataset.csrfToken,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Quest save failed.");

    const quest = await response.json();
    form.reset();
    status.textContent = "Quest created.";

    form.dispatchEvent(
      new CustomEvent("quest:created", { detail: quest, bubbles: true })
    );
  } catch {
    status.textContent = "Could not save the quest. Try again.";
  } finally {
    button.disabled = false;
  }
}

document.getElementById("quest-form").addEventListener("submit", submitQuest);
