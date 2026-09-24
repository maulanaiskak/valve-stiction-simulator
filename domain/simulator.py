"""Simulator domain logic (PRD FR-1): a synthetic valve PV/OP signal
generator, with a toggle to inject stiction. Pure computation -- no I/O,
no MQTT awareness. See delivery/mqtt for the publishing loop.

Not the thesis's publish.py (which replayed real CSVs) -- FR-1 asks for a
synthetic generator. Deliberately not a closed-loop PI controller: tried
that first and found the controller could self-oscillate from integral
windup against the OP saturation limits even with a perfectly healthy
valve, confounding the exact signal this project needs to be clean.
Instead OP is directly scripted as a triangle wave (mimicking a
controller actively driving the valve), and PV follows it through the
same stick-slip model valve-stiction-ml's test fixtures
(tests/test_classic.py's make_stick_slip) use -- when stiction is on, PV
holds at its last position until OP's deviation exceeds a stick band,
then snaps to catch up. Verified end-to-end through the real classic
detector before wiring this into the pipeline: stiction=True gives
ellipse_index=1.90/kano=True, stiction=False gives 0.12/False -- clean
separation, not a coin flip.
"""

from __future__ import annotations

import os

import numpy as np

# Validated together (see module docstring) -- don't change one without
# rechecking against valve_stiction_ml.classic like the docstring did.
PERIOD_SAMPLES = int(os.environ.get("PERIOD_SAMPLES", "50"))
AMPLITUDE = float(os.environ.get("AMPLITUDE", "20.0"))
STICK_BAND = float(os.environ.get("STICK_BAND", "7.0"))
NOISE_STD = float(os.environ.get("NOISE_STD", "0.4"))
CENTER = float(os.environ.get("CENTER", "50.0"))


class Simulator:
    def __init__(self, stiction_enabled: bool, seed: int = 0):
        self.stiction_enabled = stiction_enabled
        self.n = 0
        self.valve_position = CENTER
        self.rng = np.random.default_rng(seed)

    def step(self) -> tuple[float, float]:
        phase = (self.n % PERIOD_SAMPLES) / PERIOD_SAMPLES
        op = CENTER + AMPLITUDE * (2 * abs(2 * phase - 1) - 1)  # triangle wave
        op += self.rng.normal(0, NOISE_STD)

        if self.stiction_enabled:
            if abs(op - self.valve_position) > STICK_BAND:
                self.valve_position = op  # snap to catch up
            # else: stuck, valve_position unchanged
        else:
            self.valve_position = op

        pv = self.valve_position + self.rng.normal(0, NOISE_STD)
        self.n += 1
        return pv, op
