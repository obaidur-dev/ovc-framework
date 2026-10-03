// The "what I'm studying" label is typed by the user, so it is treated as
// untrusted text. It is only ever shown with textContent, never innerHTML.

export const MAX_LABEL_LENGTH = 60;

export function cleanLabel(text) {
  return String(text ?? "").trim().slice(0, MAX_LABEL_LENGTH);
}

export function renderLabel(element, text) {
  element.textContent = cleanLabel(text);
}
