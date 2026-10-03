import { test } from "node:test";
import assert from "node:assert/strict";
import { renderLabel, cleanLabel, MAX_LABEL_LENGTH } from "../src/label.js";

test("label_is_shown_as_text_not_html", () => {
  let innerHtmlTouched = false;
  const fake = {
    textContent: "",
    set innerHTML(_value) { innerHtmlTouched = true; },
  };
  const hostile = "<img src=x onerror=alert(1)>";
  renderLabel(fake, hostile);
  assert.equal(fake.textContent, hostile); // shown literally, as text
  assert.equal(innerHtmlTouched, false);
});

test("label_is_trimmed_and_limited", () => {
  assert.equal(cleanLabel("   maths  "), "maths");
  assert.equal(cleanLabel("x".repeat(500)).length, MAX_LABEL_LENGTH);
  assert.equal(cleanLabel(null), "");
});
