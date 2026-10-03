// Pure timer logic. No screen code here, so it can be tested without a browser.
// All times are in milliseconds since 1970 (Date.now()). The remaining time is
// always worked out from the clock, never by counting ticks, so a sleeping
// browser tab cannot make the timer drift (NFR-001).

export const DEFAULT_LENGTHS = { focus: 25 * 60, break: 5 * 60 }; // seconds

export function formatTime(totalSeconds) {
  const s = Math.max(0, Math.ceil(totalSeconds));
  const mm = String(Math.floor(s / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  return `${mm}:${ss}`;
}

// "?debug=5" makes each block 5 seconds long so you can test by hand.
// Only a whole number from 1 to 60 is accepted; anything else is ignored.
export function parseDebugSeconds(search) {
  const value = new URLSearchParams(search).get("debug");
  if (value === null || !/^\d{1,2}$/.test(value)) return null;
  const n = Number(value);
  return n >= 1 && n <= 60 ? n : null;
}

export function createState(lengths = DEFAULT_LENGTHS) {
  return { phase: "focus", running: false, remainingMs: lengths.focus * 1000, endsAt: null, completed: 0 };
}

export function start(state, now) {
  if (state.running) return state;
  return { ...state, running: true, endsAt: now + state.remainingMs };
}

export function pause(state, now) {
  if (!state.running) return state;
  return { ...state, running: false, remainingMs: Math.max(0, state.endsAt - now), endsAt: null };
}

export function remainingSeconds(state, now) {
  const ms = state.running ? Math.max(0, state.endsAt - now) : state.remainingMs;
  return ms / 1000;
}

// Call this often. When the current block has run out it switches phase,
// counts a finished focus block, and keeps running into the next block.
export function tick(state, now, lengths = DEFAULT_LENGTHS) {
  if (!state.running || now < state.endsAt) return { state, switched: false };
  const finishedFocus = state.phase === "focus";
  const phase = finishedFocus ? "break" : "focus";
  const lengthMs = lengths[phase] * 1000;
  return {
    state: {
      phase,
      running: true,
      remainingMs: lengthMs,
      endsAt: now + lengthMs,
      completed: state.completed + (finishedFocus ? 1 : 0),
    },
    switched: true,
  };
}
