// Saves today's finished-block count and the label in the browser's own
// storage. The storage object is passed in, so tests can use a fake one.
// Every call is wrapped so a blocked or full storage never crashes the page.

const LABEL_KEY = "study-timer-label";

export function dayKey(date) {
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  return `study-timer-count-${date.getFullYear()}-${mm}-${dd}`;
}

export function loadCount(storage, date) {
  try {
    const n = Number.parseInt(storage.getItem(dayKey(date)), 10);
    return Number.isFinite(n) && n >= 0 ? n : 0;
  } catch {
    return 0;
  }
}

export function saveCount(storage, date, count) {
  try {
    storage.setItem(dayKey(date), String(count));
  } catch {
    /* storage unavailable: the count simply will not survive a reload */
  }
}

export function loadLabel(storage) {
  try {
    return storage.getItem(LABEL_KEY) ?? "";
  } catch {
    return "";
  }
}

export function saveLabel(storage, text) {
  try {
    storage.setItem(LABEL_KEY, text);
  } catch {
    /* ignore */
  }
}
