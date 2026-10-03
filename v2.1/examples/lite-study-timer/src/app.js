// Connects the page to the logic. This is the only file that touches the screen.
import { DEFAULT_LENGTHS, createState, start, pause, tick, remainingSeconds, formatTime, parseDebugSeconds } from "./timer.js";
import { renderLabel, cleanLabel } from "./label.js";
import { loadCount, saveCount, loadLabel, saveLabel } from "./store.js";

const debugSeconds = parseDebugSeconds(window.location.search);
const lengths = debugSeconds ? { focus: debugSeconds, break: debugSeconds } : DEFAULT_LENGTHS;

const el = (id) => document.getElementById(id);
let state = { ...createState(lengths), completed: loadCount(window.localStorage, new Date()) };
let muted = false;

function beep() {
  if (muted) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    osc.connect(ctx.destination);
    osc.frequency.value = 880;
    osc.start();
    osc.stop(ctx.currentTime + 0.25);
  } catch {
    /* no audio available: the screen change is the only signal */
  }
}

function render() {
  const now = Date.now();
  const result = tick(state, now, lengths);
  state = result.state;
  if (result.switched) {
    saveCount(window.localStorage, new Date(), state.completed);
    beep();
  }
  el("time").textContent = formatTime(remainingSeconds(state, now));
  el("phase").textContent = state.phase === "focus" ? "Focus" : "Break";
  el("count").textContent = String(state.completed);
  el("start").disabled = state.running;
  el("pause").disabled = !state.running;
}

el("start").addEventListener("click", () => { state = start(state, Date.now()); render(); });
el("pause").addEventListener("click", () => { state = pause(state, Date.now()); render(); });
el("mute").addEventListener("click", () => {
  muted = !muted;
  el("mute").textContent = muted ? "Unmute" : "Mute";
});

const input = el("label-input");
input.value = cleanLabel(loadLabel(window.localStorage));
renderLabel(el("label-shown"), input.value);
input.addEventListener("input", () => {
  renderLabel(el("label-shown"), input.value);
  saveLabel(window.localStorage, cleanLabel(input.value));
});

setInterval(render, 250);
render();
