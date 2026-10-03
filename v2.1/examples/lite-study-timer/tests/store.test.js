import { test } from "node:test";
import assert from "node:assert/strict";
import { loadCount, saveCount, loadLabel, saveLabel } from "../src/store.js";

function fakeStorage() {
  const data = new Map();
  return { getItem: (k) => (data.has(k) ? data.get(k) : null), setItem: (k, v) => data.set(k, v) };
}

test("count_survives_reload", () => {
  const storage = fakeStorage();
  const day = new Date(2026, 9, 1);
  saveCount(storage, day, 3);
  assert.equal(loadCount(storage, day), 3);
});

test("count_resets_on_a_new_day", () => {
  const storage = fakeStorage();
  saveCount(storage, new Date(2026, 9, 1), 3);
  assert.equal(loadCount(storage, new Date(2026, 9, 2)), 0);
});

test("bad_or_blocked_storage_falls_back_safely", () => {
  const broken = { getItem() { throw new Error("blocked"); }, setItem() { throw new Error("full"); } };
  assert.equal(loadCount(broken, new Date()), 0);
  assert.equal(loadLabel(broken), "");
  saveCount(broken, new Date(), 1); // must not throw
  saveLabel(broken, "x");           // must not throw
  const junk = { getItem: () => "not a number" };
  assert.equal(loadCount(junk, new Date()), 0);
});

test("label_round_trips_as_plain_text", () => {
  const storage = fakeStorage();
  saveLabel(storage, "organic chemistry");
  assert.equal(loadLabel(storage), "organic chemistry");
});
