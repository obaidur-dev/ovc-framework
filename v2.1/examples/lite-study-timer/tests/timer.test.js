import { test } from "node:test";
import assert from "node:assert/strict";
import { createState, start, pause, tick, remainingSeconds, formatTime, parseDebugSeconds, DEFAULT_LENGTHS } from "../src/timer.js";

test("counts_down_from_25_minutes", () => {
  const s = start(createState(), 0);
  assert.equal(remainingSeconds(s, 0), 1500);
  assert.equal(remainingSeconds(s, 1000), 1499);
});

test("switches_phase_at_zero", () => {
  const s = start(createState(), 0);
  const early = tick(s, 1499 * 1000);
  assert.equal(early.switched, false);
  const { state, switched } = tick(s, 1500 * 1000);
  assert.equal(switched, true);
  assert.equal(state.phase, "break");
  assert.equal(state.completed, 1);
  assert.equal(remainingSeconds(state, 1500 * 1000), DEFAULT_LENGTHS.break);
});

test("break_end_switches_back_without_counting", () => {
  let s = start(createState(), 0);
  s = tick(s, 1500 * 1000).state;
  const { state } = tick(s, (1500 + 300) * 1000);
  assert.equal(state.phase, "focus");
  assert.equal(state.completed, 1);
});

test("remaining_time_follows_the_clock", () => {
  // Simulates a sleeping tab: no ticks for 10 minutes, then we look again.
  const s = start(createState(), 0);
  assert.equal(remainingSeconds(s, 600 * 1000), 900);
});

test("pause_keeps_remaining_time", () => {
  let s = start(createState(), 0);
  s = pause(s, 10 * 1000);
  assert.equal(s.running, false);
  assert.equal(remainingSeconds(s, 999 * 1000), 1490);
  s = start(s, 50 * 1000);
  assert.equal(remainingSeconds(s, 60 * 1000), 1480);
});

test("format_time_pads_and_rounds_up", () => {
  assert.equal(formatTime(1499.2), "25:00");
  assert.equal(formatTime(65), "01:05");
  assert.equal(formatTime(-3), "00:00");
});

test("debug_value_must_be_a_small_whole_number", () => {
  assert.equal(parseDebugSeconds("?debug=5"), 5);
  assert.equal(parseDebugSeconds("?debug=0"), null);
  assert.equal(parseDebugSeconds("?debug=61"), null);
  assert.equal(parseDebugSeconds("?debug=abc"), null);
  assert.equal(parseDebugSeconds("?debug=5;alert(1)"), null);
  assert.equal(parseDebugSeconds(""), null);
});
