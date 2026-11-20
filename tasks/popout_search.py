"""Pop-out search: look to the one disc whose color differs. The lab's first training task.

Designed with the PI on 2026-11-07 (wl-xcon's
`docs/superpowers/specs/2026-11-07-popout-search-design.md`, §3; every number below marked "the
PI's" is his from there), and **revised after his try-out of the demo** on 2026-11-16 (wl-xcon's
`docs/superpowers/specs/2026-11-16-popout-revision-design.md`, approved that day, "Approve both";
§ numbers below without a design named are the first design's). An animal that already fixates
reliably learns to look to the odd one of a ring of discs, by its color alone.

**The trial** (§3.1, as revised, the revision's §3). The fixation point comes on after the gap
between trials, in its *hold* look, a gray disc; the animal looks to it within 2.0 s and holds it,
for a wait drawn each trial non-aging from 0.75 to 1.25 s, the PI's published foreperiod
[@westerberg2020priming]. Then the discs come on, **and the fixation point stays on**. After
`go_delay` it takes its *act* look, a gray ring of the same size ("Hollows out"): **that is the
go**, and the reaction time runs from it. `go_delay` starts at 0, so the discs and the go are one
frame, the reaction-time version (the PI: "option 1 [array on and dot changes together]"); above 0
it is the delayed-saccade version, and leaving the fixation point in the delay is an early saccade.
**The next saccade from fixation answers** ("anything other than looking at the target with the
next saccade from fix to the target is an error"): landing on the odd one and holding it 0.3 s is
correct and pays one reward; landing on another disc, landing on empty space or leaving the odd one
before its 0.3 s are errors, and so is leaving the fixation point before the go (an early saccade).
Each error blanks the screen for 2.0 s, no reward, and the trial keeps its own outcome. No saccade
within 1.0 s of the go is no response. A trial starts with 1.0 s of blank screen, the time between
trials.

**The fixation rule, the lab's for every task** (the PI, 2026-11-16; wl-xcon's TSK-79): "we should
have a fix color that indicates that the monkey should be looking at fixation, eg, a gray fix dot.
then when the monkey should "act" (or in the case of a catch, maintain fix), the fix dot changes in
some way". The point has two looks, each a setting -- its shape (a disc, a ring, a square), its
size, its ring's hole, its hue, its saturation and its brightness -- and it is never hidden as a go
cue. Each look's color is one of the four colors below at its own saturation, which starts at 0,
the set's gray at the point's brightness.

**Special trials** (the revision's §4; the PI: "A percentage per kind"). Each trial is drawn normal
or special between trials, each kind at its own percentage, 0 to start: **target absent**, every
disc in the distractor color; **odd one's place empty**, the distractors with the odd one's place
left empty; **a distractor alone**, one disc in the distractor color; three catches, where the right
answer is to keep looking at the fixation point for `catch_hold` after the go, paid as a correct
trial is, and looking away is an error with the timeout ("An error, counted"). The fourth, **the
odd one alone**, is a probe, scored as a search. A special trial follows its stage -- its pairing,
its set size from the stage's staircase -- counts in the stage's bars, and never steps a staircase
("Only normal trials move it").

**The stages** (§3.3), the plan `training`: **Alone**, the odd one alone on the ring; **Fade-in**,
four discs, the three distractors climbing from faint to the odd one's brightness on a staircase;
**Crowd**, every disc at full, from 4 discs up to 12 on a staircase. Within a stage a staircase
steps three right harder, one wrong easier [@levitt1971transformed] (wl-xcon's TSK-32, TSK-33);
between stages the rig suggests a move and the trainer confirms or holds it: up at 80% right of
the last 50 answers at the stage's hardest step, back below 50% of the last 50 (TSK-72). **The
full task** (the revision's §5) is Crowd at its hardest, all 12 discs with the distractors at full,
from every pairing.

**The colors** (§3.2): wl-style's isoluminant blue, purple and red and the PI's green, held equal
in macaque cone luminance at 15 cd/m² (`stimuli/isohue.json`, plain data; wl-xcon's COL-37). On
each trial one is the odd one and another fills the distractors, drawn from the pairings the
trainer has pooled; the pool starts small and widens when the rig suggests it and the trainer
picks (TSK-73).

**Every number is a setting the trainer may change in the console** (the PI, 2026-11-07: "i
mean, everything should be adjustable in the console, no?"; wl-xcon's TSK-75): each starts at the
PI's value, and a number stays fixed only with its reason written beside it. The bounds on the
engine's own waits are settings too since the revision (§3: "The fixed 0.3 s landing bound ... and
the other fixed bounds in the task file become settings"), and so are the blink and tracker-loss
graces (the PI, 2026-11-16, "Yes, a setting"). The stages' own
values (one disc in Alone, four in Fade-in, the distractors at full in Crowd) are conditions'
values, which a person's live value overrides like any other. **Each setting names its section**
of the console's Task parameters tab, or of its Training tab (wl-xcon's console settings design,
§7; the PI, 2026-11-16, "The task file names it"), and **declares a limit only where a value
cannot be, or where wl-xcon's checks need one**, each with its reason (§4; the PI, 2026-11-16,
"Hard limits only where impossible"): what crowds or overlaps at the values set is warned of
where they are set, not capped here. **Each setting carries its plain name and one sentence saying
what it is**, every count and share is a whole number, the bars and the distractors' brightness
fractions are percents (the PI, 2026-11-19), and the bars, the staircases and the special trials
read as four rules, each one box with one Apply (wl-xcon's console interface design,
goals 5, 6 and 8; the PI, 2026-11-19: "descriptions are too long ... what are pairings? for
necessary whole numbers (set size), there should not be a decimal option for entry", and "One box
after Timing").

Positions and sizes are degrees of visual angle at their place (the PI, 2026-10-19). Its event
codes are wl-xcon's `tasks/allocation.py`'s, until this repository publishes one.
"""

from pathlib import Path

from wl_xcon.photometry import ColorSet, ColorSetLight
from wl_xcon.task import (
    BACKGROUND,
    CLEAR_CUT,
    CRITERION,
    EASIER,
    EXPECTED,
    FRESH,
    HARDER,
    NEITHER,
    NOT_DIFFICULTY,
    SAME,
    SPENT,
    STIMULUS,
    After,
    Annulus,
    Array,
    Blank,
    Block,
    ByCriterion,
    Choice,
    Condition,
    Counting,
    Disc,
    Entered,
    Exited,
    FullTask,
    Group,
    Hide,
    Hold,
    Mark,
    Meaning,
    NonAging,
    ObjectWindows,
    On,
    Outcome,
    P,
    Param,
    Plan,
    Pool,
    ReactionTime,
    Reward,
    SaccadeOnset,
    SaccadeTo,
    Show,
    Special,
    Square,
    Staircase,
    State,
    Steps,
    Stimulus,
    Task,
    Tolerances,
    Trial,
    Uniform,
    Update,
    Window,
)

#: **The four colors** (§3.2), as plain data beside this repository's tasks: what each color is,
#: read by a path relative to this file; the rig computes each one's drive on its measured panel.
ISOHUE = ColorSet.load(Path(__file__).resolve().parents[1] / "stimuli" / "isohue.json")
#: Their names, in the file's order: blue, purple, red, green.
COLORS = tuple(ISOHUE.colors)

#: The odd one: a `disc_size` disc (1° to start) at the set's full luminance, `color_luminance`
#: (15 cd/m² to start, the file's own).
ODD = {
    color: Disc(size=P("disc_size"),
                color=ColorSetLight(ISOHUE, color, luminance=P("color_luminance")))
    for color in COLORS
}
#: A distractor: a disc as large at `distractor_fraction` of it, faint to full in Fade-in, full in
#: Crowd.
AMONG = {
    color: Disc(size=P("disc_size"),
                color=ColorSetLight(ISOHUE, color, fraction=P("distractor_fraction"),
                                    luminance=P("color_luminance")))
    for color in COLORS
}

#: **The twelve ordered pairings, the odd one's color first** (§3.2, "A pool of four"), in the
#: colors' order: blue among purple, red, green; purple among blue, red, green; red among blue,
#: purple, green; green among blue, purple, red. The pool's value is the sum of the numbers of
#: those it holds, 1, 2, 4 ... 2048 in this order (wl-xcon's `task.Pool`).
POOL = Pool(
    "pairings",
    tuple((ODD[odd], AMONG[among]) for odd in COLORS for among in COLORS if among != odd),
    odd="odd_color",
    distractor="distractor_color",
)
#: **The pool a run starts with where the trainer picks none**: blue among red and red among blue,
#: the two colors the PI first named ("the isoluminate bluish color and redish color"), so from the
#: first trial the odd one is not always the same color. The trainer picks at the run's start
#: (§3.6).
FIRST_PAIRINGS = POOL.number([(ODD["blue"], AMONG["red"]), (ODD["red"], AMONG["blue"])])
#: **Every pairing**, the full task's pool (the revision's §5: "every pairing").
EVERY_PAIRING = POOL.number(list(POOL.choices))


def _looks(size: str, hole: str, color: str) -> tuple:
    """**One look's three shapes** (the fixation rule: "changes color or shape or hollows out"): a
    disc `size` across, a ring as wide with a hole `hole` across, and a square `size` on a side,
    each lit by the look's own color, `color`."""
    return (
        Disc(size=P(size), color=P(color)),
        Annulus(inner=P(hole), outer=P(size), color=P(color)),
        Square(size=P(size), color=P(color)),
    )


def _hues(saturation: str, luminance: str) -> tuple:
    """**One look's hues**: each of the four colors as a light at the look's own `saturation`
    (0, the set's gray, to 1, the color as the set shows it, its macaque luminance held) and
    brightness `luminance`, cd/m²."""
    return tuple(ColorSetLight(ISOHUE, color, saturation=P(saturation), luminance=P(luminance))
                 for color in COLORS)


#: **The fixation point's two looks** (the revision's §2): its *hold* look until the go, a disc to
#: start, and its *act* look from the go, a ring to start ("Hollows out"), each built from its own
#: size, hole, hue, saturation and brightness.
HOLD_LOOKS = _looks("fix_size", "fix_hole", "fix_color")
ACT_LOOKS = _looks("fix_act_size", "fix_act_hole", "fix_act_color")
HOLD_HUES = _hues("fix_saturation", "fix_luminance")
ACT_HUES = _hues("fix_act_saturation", "fix_act_luminance")

# The fixation point, at the center: a fixed place, since the ring and every window are about it.
# It is drawn in its hold look; the go changes it to its act look, never hiding it.
FIX = Stimulus("fix", at=(0.0, 0.0), looks=P("fix_look"))


def _ring(*, n: object = P("set_size"), looks: object = P("odd_color"),
          among: object = P("distractor_color"), found_by: str = "look") -> Stimulus:
    """**The ring** (§3.1): discs `disc_size` across (1° to start) on a true circle `ring_radius`
    from fixation (8° to start), the odd one object 0 and the ring turned to a new direction every
    trial, so the odd one is anywhere on it. Every kind of trial's array is a stimulus named
    `search`, so the windows, the choice and the record read one name. **At the starts**, twelve
    discs on the 8° ring are 4.13° apart, so their 1.5° windows never overlap. **At other values
    they can**: on the 8° ring windows wider than 2.06° would, and on a 4° ring twelve discs are
    2.07° apart, which the 1.5° windows already overlap at (computed 2026-11-07). No range holds
    them apart: wl-xcon judges the layout at the values set, at load and as each changes, and
    warns where windows overlap (`crowded-array`), where discs touch (`objects-touch`) and where a
    disc's window is smaller than the disc (`window-inside-object`); the trainer keeps them apart.
    **The fixation window, whose exit starts the answer, must stay clear of the discs' windows
    too**: on a ring smaller than the two radii together a look to the odd one could land inside
    it, never leave it, and end as no response with no reward; wl-xcon warns of it as the values
    set make it so (`answer-window-reaches-objects`)."""
    return Stimulus(
        "search",
        # The array's center is the fixation point's, fixed with it.
        at=(0.0, 0.0),
        looks=Array(
            n=n,
            radius=P("ring_radius"),
            target=0,
            looks=looks,
            among=among,
            phase=P("array_rotation"),
            found_by=found_by,
        ),
    )


#: **The normal search's array**: the odd one among `set_size - 1` distractors.
ARRAY = _ring()
#: **The special kinds' arrays** (the revision's §4 table). **The lone kinds' `n=1` is fixed**:
#: each kind is defined as one disc ("Either, as two kinds"), so no number a trainer sets.
ABSENT = _ring(looks=P("distractor_color"), found_by="none")
EMPTY_PLACE = _ring(looks=Blank(), found_by="none")
DISTRACTOR_ALONE = _ring(n=1, looks=P("distractor_color"), found_by="none")
ODD_ALONE = _ring(n=1)

#: The event codes this task strobes, from wl-xcon's `tasks/allocation.py`.
FIX_ON, SACCADE_ONSET, TARGET_ACQUIRED, ABORT_NO_FIXATION = 4096, 4098, 4099, 4100
ABORT_FIXATION_BREAK, REWARD_COMMANDED, ARRAY_ON, DISTRACTOR_ACQUIRED = 4101, 4102, 4103, 4104
OUTCOME_CORRECT, OUTCOME_WRONG_TARGET, OUTCOME_NO_RESPONSE = 4110, 4113, 4117
OUTCOME_ABORT, OUTCOME_FIXATION_BREAK, OUTCOME_TARGET_BREAK = 4118, 4119, 4120
OUTCOME_CORRECT_REJECT, OUTCOME_FALSE_ALARM = 4123, 4124
TIMEOUT_ON = 4138
#: The revision's (its §7; wl-xcon's XC-543): the go, a catch's hold kept and broken, and each
#: special kind, strobed on its array's frame after `ARRAY_ON`.
GO_CUE, CATCH_FIXATION_HELD, CATCH_FIXATION_BREAK = 4139, 4140, 4141
SPECIAL_TARGET_ABSENT, SPECIAL_ODD_PLACE_EMPTY = 4142, 4143
SPECIAL_DISTRACTOR_ALONE, SPECIAL_ODD_ONE_ALONE = 4144, 4145


#: **Why the training plan's settings keep both ends** (the console settings plan's Task 11, as
#: `set_size` keeps its highest): wl-xcon's load checks read the whole range of each setting a
#: staircase or a bar reads (`bad-staircase`, `bad-plan`) and refuse one with an open side, and
#: the bars keep as many answers as a window's highest. The numbers were the builder's of
#: 2026-11-07, wide enough for a trainer; a side a standard reason covers takes that instead.
PLANNED = ("the training plan's load checks read its whole range, so it keeps both ends; "
           "the builder's")
#: Why each special kind's percentage is at most 100.
SHARE = "a share of trials is at most 100"
#: Why each fixation point brightness is at most 80 cd/m².
WHITE = "white on the default calibration, the published sRGB 80 cd/m² (COL-29)"


def _timeout(state: str, outcome: Outcome, reason: int) -> State:
    """**The blank screen after an error** (§3.1, "A short timeout"): nothing shown for `timeout`
    seconds, no reward, then the trial ends with the error's own `outcome`, its reason strobed
    just before the trial's end marker, which several outcomes share."""
    return State(state, go=[On(After(P("timeout")), outcome, do=[Mark(reason)])])


#: Each error's blank begins: the fixation point and the array off, on one frame.
BLANK = [Hide("fix"), Hide("search")]

params = [
    # **Timing**, by their unit (the console settings design's §7): the PI's starting values
    # (§3.1, "that looks good"), each a value the trainer may change. A time below 0 cannot
    # be; none has a highest: a hold its state's own bound always ends first, below, is a
    # trial that cannot finish, refused where it is set (`impossible-trial`). `fix_hold` is
    # drawn non-aging each trial (`TASK.draws`); its start, 0.5 s, is what its timing switch's
    # fixed side holds.
    Param("inter_trial", unit="s", low=0.0, start=1.0,
          label="Time between trials",
          help="The blank screen before each trial begins, in seconds."),
    Param("fix_acquisition", unit="s", low=0.0, start=2.0,
          label="Time to find the fixation point",
          help="How long the animal has to look at the fixation point once it comes on."),
    Param("fix_hold", unit="s", low=0.0, start=0.5,
          label="Fixation hold",
          help="How long the animal holds its gaze on the fixation point before the discs "
               "appear."),
    # The go's delay after the discs (the revision's §3 item 5): 0, the reaction-time version,
    # the discs and the go on one frame (wl-xcon's TSK-78: a zero wait lasts no frame).
    Param("go_delay", unit="s", low=0.0, start=0.0,
          label="Delay before the go",
          help="How long the discs are up before the fixation point changes its look to say "
               "go, in seconds."),
    Param("response_deadline", unit="s", low=0.0, start=1.0,
          label="Time to answer",
          help="How long the animal has, once the fixation point says go, to start its look "
               "away from the center."),
    Param("target_hold", unit="s", low=0.0, start=0.3,
          label="Hold on the odd disc",
          help="How long the animal keeps looking at the odd disc to earn its reward."),
    Param("timeout", unit="s", low=0.0, start=2.0,
          label="Timeout after an error",
          help="How long the screen stays blank after an error, with no reward."),
    # **The graces** (the PI, 2026-11-16, "Yes, a setting"), at the engine's own: a blink ends a
    # held fixation at once, and the tracker may stall 50 ms, the OpenIrisDPI paper's reported
    # stall maximum, a placeholder until a rig's tracker is measured (wl-xcon's S5, V3(a)).
    Param("blink_grace", unit="s", low=0.0, start=0.0,
          label="Blink allowance",
          help="How long a blink may hide the eye before the trial ends as a blink, in seconds."),
    Param("tracker_lost_grace", unit="s", low=0.0, start=0.05,
          label="Tracker dropout allowance",
          help="How long the eye tracker may lose the eye before the trial ends as tracker loss, "
               "in seconds."),
    # **The bounds on the engine's own waits** (the revision's §3; TSK-75: "bounds on the engine's
    # own waits"), settings since the revision, each at the number the task file fixed. Each is a
    # wait a hold or a landing cannot outlast: a hold its bound always ends first is a trial that
    # cannot finish, refused where it is set (`impossible-trial`), and one a drawn hold can
    # outlast is warned (`little-time-to-answer`).
    # The fixation hold's, the controller's (TSK-75): a hold the tracker's stalls keep from
    # completing ends there, as no fixation.
    Param("fix_hold_limit", unit="s", low=0.0, start=10.0, section="Timing/bounds",
          label="Fixation hold limit",
          help="How long the rig waits for a fixation hold to complete before ending the trial "
               "as no fixation."),
    # The landing's, the builder's (TSK-74 (d), "an engineering bound"), far longer than any
    # saccade lasts: an eye that stays put after leaving the fixation window ends there, astray.
    Param("landing_limit", unit="s", low=0.0, start=0.3, section="Timing/bounds",
          label="Saccade landing limit",
          help="How long the rig waits for the look away from the center to land before scoring "
               "it as empty space."),
    # The hold on the odd disc's, the controller's (TSK-75), likewise.
    Param("target_hold_limit", unit="s", low=0.0, start=3.0, section="Timing/bounds",
          label="Odd disc hold limit",
          help="How long the rig waits for a hold on the odd disc to complete before ending the "
               "trial as no response."),
    # A catch's hold's, as the odd disc's (the revision's plan).
    Param("catch_hold_limit", unit="s", low=0.0, start=3.0, section="Timing/bounds",
          label="Catch hold limit",
          help="How long the rig waits for a catch trial's hold to complete before ending the "
               "trial as no response."),
    # **Special trials** (the revision's §4; the PI, 2026-11-16, "A percentage per kind"): each
    # kind's percentage of trials, 0 to start, whole (the console interface design's goal 6);
    # past 100 together is warned where it is set (`specials-over-100`). And the catch's hold
    # after the go, 0.5 s (the revision's §6), a time a person may draw.
    Param("target_absent_percent", unit="percent", low=0, high=100, start=0, why=SHARE,
          section="Special trials",
          label="Target absent trials",
          help="The percent of trials with every disc in the distractor color, a catch trial.",
          whole=True),
    Param("odd_place_empty_percent", unit="percent", low=0, high=100, start=0, why=SHARE,
          section="Special trials",
          label="Odd place empty trials",
          help="The percent of trials with the distractors only, the odd disc's place left "
               "empty, a catch trial.",
          whole=True),
    Param("distractor_alone_percent", unit="percent", low=0, high=100, start=0, why=SHARE,
          section="Special trials",
          label="Distractor alone trials",
          help="The percent of trials with one disc alone in the distractor color, a catch "
               "trial.",
          whole=True),
    Param("odd_one_alone_percent", unit="percent", low=0, high=100, start=0, why=SHARE,
          section="Special trials",
          label="Odd disc alone trials",
          help="The percent of trials with the odd disc alone, scored as a search.",
          whole=True),
    Param("catch_hold", unit="s", low=0.0, start=0.5, section="Special trials",
          label="Catch hold",
          help="How long the animal keeps looking at the fixation point after the go on a catch "
               "trial to earn its reward."),
    # **Gaze windows** (§3.1): the fixation window's radius in degrees, 2°; the discs'
    # windows a multiple of each disc's radius, 3.0 -- the 1.5° about a 1° disc they were.
    # A size's lowest stays open (one of 0 is refused where it is set); a multiple below 0
    # cannot be. Windows that overlap, or one smaller than its disc, are warned of at the
    # values set (`crowded-array`, `window-inside-object`), as the fixation window reaching
    # the discs' is (`answer-window-reaches-objects`).
    Param("fix_window", unit="deg", start=2.0, section="Gaze windows",
          label="Fixation window",
          help="How far from the fixation point the eye may be and still count as on it, in "
               "degrees."),
    Param("object_window", unit="× disc radius", low=0.0, start=3.0,
          section="Gaze windows",
          label="Disc window",
          help="How far from a disc's center the eye counts as on that disc, in multiples of "
               "the disc's radius."),
    # **The fixation point's two looks** (the revision's §2, the PI's rule): each a shape, a
    # size (0.3° to start, as it was), a ring's hole (0.15°, half its width, the builder's), a
    # hue, a saturation and a brightness (40 cd/m², as it was), the act look the hold look
    # hollowed out to start. A size's lowest stays open, as the discs' does; a hole below 0
    # cannot be. Each brightness is bounded at the default calibration's white until a panel is
    # measured (wl-xcon's COL-29). Each saturation starts at 0, the set's gray at the point's
    # brightness -- D65, the lab's gray, as the point was (the PI, 2026-10-07) -- and each hue
    # at the set's first, which at 0 shows no hue.
    Param("fix_look", unit="appearance", choices=HOLD_LOOKS, start=HOLD_LOOKS[0],
          section="Stimuli/fixation point",
          label="Fixation point shape",
          help="The fixation point's shape while the animal holds it, before the go."),
    Param("fix_act_look", unit="appearance", choices=ACT_LOOKS, start=ACT_LOOKS[1],
          section="Stimuli/fixation point",
          label="Fixation shape at go",
          help="The fixation point's shape from the go on, which tells the animal to act."),
    Param("fix_size", unit="deg", start=0.3, section="Stimuli/fixation point",
          label="Fixation point size",
          help="How wide the fixation point is, in degrees."),
    Param("fix_act_size", unit="deg", start=0.3, section="Stimuli/fixation point",
          label="Fixation size at go",
          help="How wide the fixation point is from the go on, in degrees."),
    Param("fix_hole", unit="deg", low=0.0, start=0.15, section="Stimuli/fixation point",
          label="Fixation ring hole",
          help="How wide the hole is where the fixation point is a ring, in degrees."),
    Param("fix_act_hole", unit="deg", low=0.0, start=0.15, section="Stimuli/fixation point",
          label="Fixation ring hole at go",
          help="How wide the hole is where the fixation point is a ring from the go on, in "
               "degrees."),
    Param("fix_color", unit="appearance", choices=HOLD_HUES, start=HOLD_HUES[0],
          section="Stimuli/fixation point",
          label="Fixation point hue",
          help="The fixation point's hue, one of the four colors; with no saturation it is gray."),
    Param("fix_act_color", unit="appearance", choices=ACT_HUES, start=ACT_HUES[0],
          section="Stimuli/fixation point",
          label="Fixation hue at go",
          help="The fixation point's hue from the go on; with no saturation it is gray."),
    Param("fix_saturation", unit="fraction", low=0.0, high=1.0, start=0.0,
          section="Stimuli/fixation point",
          label="Fixation point saturation",
          help="How much of its hue the fixation point shows, as a percent, from gray to full.",
          percent=True),
    Param("fix_act_saturation", unit="fraction", low=0.0, high=1.0, start=0.0,
          section="Stimuli/fixation point",
          label="Fixation saturation at go",
          help="How much of its hue the fixation point shows from the go on, as a percent.",
          percent=True),
    Param("fix_luminance", unit="cd/m2", high=80.0, start=40.0, why=WHITE,
          section="Stimuli/fixation point",
          label="Fixation point brightness",
          help="How bright the fixation point is, in cd/m²."),
    Param("fix_act_luminance", unit="cd/m2", high=80.0, start=40.0, why=WHITE,
          section="Stimuli/fixation point",
          label="Fixation brightness at go",
          help="How bright the fixation point is from the go on, in cd/m²."),
    # **The array** (§3.1): the discs' size, its lowest open (a disc of 0° is refused where it
    # is set), and the ring's radius, a distance, which below 0 cannot be; how many discs, one
    # in Alone, four in Fade-in, Crowd's staircase from 4 to 12, up to 36 by hand, a highest
    # kept since a run builds every disc before its first frame (wl-xcon's `unbounded-set-size`
    # refuses a set size without one); and the ring's direction, turned anew every trial
    # (`TASK.draws`), written from 0 to 360.
    Param("disc_size", unit="deg", start=1.0, section="Stimuli/array",
          label="Disc size",
          help="How wide each disc is, in degrees."),
    Param("ring_radius", unit="deg", low=0.0, start=8.0, section="Stimuli/array",
          label="Ring distance from center",
          help="How far the ring of discs sits from the fixation point, in degrees."),
    Param("set_size", unit="objects", low=1, high=36, start=4,
          why="a run builds every disc before its first frame, so a set size needs a "
              "highest: 36, the PI's (2026-11-19)",
          section="Stimuli/array",
          label="Number of discs",
          help="How many discs are on the ring, the odd one included.",
          whole=True),
    Param("array_rotation", unit="deg", low=0.0, high=360.0, start=0.0,
          why="a direction, written from 0 to 360 (the PI, 2026-10-30)",
          section="Stimuli/array",
          label="Odd disc direction",
          help="Where around the ring the odd disc sits, in degrees; the rig picks it at "
               "random each trial."),
    # **The colors** (§3.2): the two looks each trial's pairing gives; their brightness at
    # full, cd/m² of macaque luminance ("15 cd/m² on every rig"), the color set file's own to
    # start, bounded as the fixation point's is (COL-29), its lowest open: at 0 or below a
    # color has no chromaticity, and a value a panel cannot show is refused where it is set
    # (`unrealizable-color`); and the distractors' luminance as a share of the odd one's,
    # Fade-in's staircase from faint, full in Crowd, its start the staircase's first level,
    # so Fade-in starts faint.
    Param("odd_color", unit="appearance", choices=tuple(ODD.values()), section="Colors",
          label="Odd disc color",
          help="The color of the one disc that differs, taken each trial from the pairings "
               "ticked."),
    Param("distractor_color", unit="appearance", choices=tuple(AMONG.values()),
          section="Colors",
          label="Distractor color",
          help="The color of the other discs, taken each trial from the pairings ticked."),
    Param("color_luminance", unit="cd/m2", high=80.0, start=ISOHUE.luminance_cd_m2, why=WHITE,
          section="Colors",
          label="Color brightness",
          help="How bright the colors are at full, in cd/m²; the odd disc is at full, the "
               "distractors a share of it."),
    Param("distractor_fraction", unit="fraction", low=0.0, high=1.0, start=0.1,
          section="Colors",
          label="Distractor brightness",
          help="How bright the distractors are, as a percent of the odd disc's brightness.",
          percent=True),
    # **The pairings pooled** (§3.2): a pool holds one at least; a value past its twelve
    # pairings the pool refuses itself, so it declares no highest. With the colors it pairs
    # (the console interface rework's Task 9).
    Param("pairings", unit="pairings", low=1, start=FIRST_PAIRINGS, section="Colors",
          label="Color pairings",
          help="Pairs of an odd disc color and a distractor color; each trial draws one of the "
               "pairs ticked.",
          whole=True),
    # **The bars** (§3.4), one pair for every stage: up at 80% right of the last 50 answers
    # at the stage's hardest step, back below 50% of the last 50 first answers ("80%
    # correct, last 50 trials"; "Below 50% of the last 50"), each read at every judgment.
    # **These and the staircases' settings keep both ends** (`PLANNED`): a bar is above 0, and
    # each window keeps as many answers as its highest.
    Param("move_up_bar", unit="fraction", low=0.5, high=1.0, start=0.8, why=PLANNED,
          section="Training/bars",
          label="Score to move up",
          help="The share of answers right at which the rig suggests moving up a stage.",
          percent=True),
    Param("move_up_window", unit="answers", low=1, high=200, start=50, why=PLANNED,
          section="Training/bars",
          label="Answers counted to move up",
          help="How many of the latest answers at the stage's hardest step the move-up score "
               "is taken over.",
          whole=True),
    Param("move_back_bar", unit="fraction", low=0.05, high=1.0, start=0.5, why=PLANNED,
          section="Training/bars",
          label="Score to move back",
          help="The share of answers right below which the rig suggests moving back a stage.",
          percent=True),
    Param("move_back_window", unit="answers", low=1, high=200, start=50, why=PLANNED,
          section="Training/bars",
          label="Answers counted to move back",
          help="How many of the latest answers the move-back score is taken over.",
          whole=True),
    # How far a suggestion's bar may be missed before it is withdrawn, in answers (the PI,
    # 2026-11-08: "Stay up until 3 below"): up at 40 of 50, it goes only below 37.
    Param("suggestion_margin", unit="answers", low=0, high=20, start=3, why=PLANNED,
          section="Training/suggestions",
          label="Suggestion margin",
          help="How many answers a score may fall short of its bar before the rig withdraws "
               "its suggestion.",
          whole=True),
    # **The staircases** (§3.4, "Automatic within a stage"): three right a level harder, one
    # wrong a level easier, in both stages [@levitt1971transformed]; and each stage's step,
    # the distractors by a tenth of full, the discs one at a time ("set size starts at 4, and
    # finer steps"), the builder's (§7); a step is above 0. A step set so fine it makes no
    # levels is warned of where it is set (`staircase-steps-unmade`).
    Param("staircase_down", unit="answers", low=1, high=10, start=3, why=PLANNED,
          section="Training/staircases",
          label="Right in a row to step harder",
          help="How many right answers in a row make the staircase one level harder.",
          whole=True),
    Param("staircase_up", unit="answers", low=1, high=10, start=1, why=PLANNED,
          section="Training/staircases",
          label="Wrong in a row to step easier",
          help="How many wrong answers in a row make the staircase one level easier.",
          whole=True),
    Param("fade_in_step", unit="fraction", low=0.05, high=1.0, start=0.1, why=PLANNED,
          section="Training/staircases",
          label="Fade-in brightness step",
          help="How much the distractors brighten or dim per Fade-in level, as a percent of "
               "full.",
          percent=True),
    Param("crowd_step", unit="objects", low=1, high=8, start=1, why=PLANNED,
          section="Training/staircases",
          label="Crowd disc step",
          help="How many discs Crowd adds or takes away per level.",
          whole=True),
    # Each staircase's easiest level, where its stage starts faintest or fewest: the
    # distractors at a tenth of full, four discs ("set size starts at 4"). Their hardest are
    # the stages' own definitions (full brightness, all 12 discs), so they stay fixed below.
    Param("fade_in_floor", unit="fraction", low=0.0, high=1.0, start=0.1,
          section="Training/staircases",
          label="Faintest distractors in Fade-in",
          help="How faint the distractors are at Fade-in's easiest level, as a percent of "
               "full.",
          percent=True),
    Param("crowd_floor", unit="objects", low=1, high=11, start=4, why=PLANNED,
          section="Training/staircases",
          label="Fewest discs in Crowd",
          help="How many discs Crowd's easiest level shows.",
          whole=True),
]


def _structure(array: Stimulus, answer: list[State], *, kind: int | None = None,
               windows: list | None = None) -> Trial:
    """**One kind of trial, from the normal search's states** (the revision's §3 and §4): the
    fixation point on in its hold look, held, `array` on with it staying, then after `go_delay`
    the go, its act look -- and then `answer`, the states that score it: the search's saccade, or
    a catch's hold. A special kind's array edge marks its `kind` too, after `ARRAY_ON`."""
    shown = [Show(array), Mark(ARRAY_ON)] + ([] if kind is None else [Mark(kind)])
    return Trial(
        start="between",
        # Direct view, with the lab's other search tasks.
        view="direct",
        # Black ("On black, faint to full"): the default bottom layer, `None`.
        background=None,
        # Its counting table: the array appears on entering the delay, the go after it. A break
        # after it -- a look to empty space, leaving the odd one before its hold -- is spent, used
        # up as a wrong disc's trial is: the PI's rule makes these and an early saccade one kind of
        # error, each with the timeout (§3.1), and the lab's other pop-out search spends them too
        # (wl-xcon's `tasks/visual_search.py`). **An early saccade in the delay is owed**, not
        # spent: it ends the trial a fixation break, which wl-xcon owes wherever it falls (its
        # `task.REPEATED`), as the first pop-out design owes a break before the go; and so is a
        # break before the array. Each stage is one condition worked on past its first trial, so
        # neither brings a trial back: the next is drawn afresh.
        counting=Counting(after_stimulus=SPENT, appears="delay"),
        # The fixation point's window scores it throughout: before the go a hold, after it the
        # answer's saccade starting as the eye leaves it, or on a catch the hold kept.
        windows=windows or [Window("fix", at=(0.0, 0.0), radius=P("fix_window"), on="fix")],
        tolerances=Tolerances(blink=P("blink_grace"), tracker_lost=P("tracker_lost_grace")),
        params=params,
        states=[
            # The time between trials, a blank screen.
            State("between", go=[On(After(P("inter_trial")), "await_fix")]),
            State(
                "await_fix",
                enter=[Show(FIX), Mark(FIX_ON)],
                go=[
                    On(Entered("fix"), "hold_fix"),
                    On(
                        After(P("fix_acquisition")),
                        Outcome.NO_FIXATION,
                        do=[Mark(ABORT_NO_FIXATION)],
                    ),
                ],
            ),
            State(
                "hold_fix",
                go=[
                    # The discs on, the fixation point staying in its hold look.
                    On(Hold("fix", P("fix_hold")), "delay", do=shown),
                    # An early saccade: leaving the fixation point before the discs.
                    On(
                        Exited("fix"),
                        "early",
                        do=[Hide("fix"), Mark(ABORT_FIXATION_BREAK), Mark(TIMEOUT_ON)],
                    ),
                    # A bound on a hold the engine runs (`fix_hold_limit`).
                    On(After(P("fix_hold_limit")), Outcome.NO_FIXATION),
                ],
            ),
            State(
                "delay",
                go=[
                    # **Leaving first**: an eye that leaves on the frame the delay ends is an
                    # early saccade, since an exit is an edge the go state would never see
                    # (wl-xcon's EYE-30); listed after the wait, it would wait out the deadline.
                    On(Exited("fix"), "early",
                       do=[*BLANK, Mark(ABORT_FIXATION_BREAK), Mark(TIMEOUT_ON)]),
                    # **The go**: the fixation point takes its act look. At 0 this passes on
                    # the frame the delay is entered, the discs' (wl-xcon's TSK-78).
                    On(After(P("go_delay")), "go",
                       do=[Update("fix", looks=P("fix_act_look")), Mark(GO_CUE)]),
                ],
            ),
            *answer,
            _timeout("early", Outcome.FIXATION_BREAK, OUTCOME_FIXATION_BREAK),
        ],
    )


#: **The search's answer** (§3.1): the next saccade from fixation, scored where it lands.
SEARCHED = [
    State(
        "go",
        go=[
            # The answer begins: the eye leaves the fixation window, and `flight` scores the
            # saccade where it lands.
            On(Exited("fix"), "flight", do=[Mark(SACCADE_ONSET)]),
            On(
                After(P("response_deadline")),
                Outcome.NO_RESPONSE,
                do=[Mark(OUTCOME_NO_RESPONSE)],
            ),
        ],
    ),
    State(
        "flight",
        go=[
            On(SaccadeTo("search.target"), "on_target", do=[Mark(TARGET_ACQUIRED)]),
            On(
                SaccadeTo("search.distractor"),
                "wrong",
                do=[*BLANK, Mark(DISTRACTOR_ACQUIRED), Mark(TIMEOUT_ON)],
            ),
            # Empty space: the saccade landed on no disc. The saccade in flight as this state
            # began counts here only where it lands; one that begins here is a second look,
            # an error, wherever it goes. An eye that stays put ends on its bound,
            # `landing_limit`.
            On(SaccadeOnset(), "astray", do=[*BLANK, Mark(TIMEOUT_ON)]),
            On(After(P("landing_limit")), "astray", do=[*BLANK, Mark(TIMEOUT_ON)]),
        ],
    ),
    State(
        "on_target",
        go=[
            On(
                Hold("search.target", P("target_hold")),
                Outcome.CORRECT,
                do=[Mark(OUTCOME_CORRECT), Mark(REWARD_COMMANDED), Reward("reward_correct")],
            ),
            On(Exited("search.target"), "broke", do=[*BLANK, Mark(TIMEOUT_ON)]),
            # A hold runs its own time, bounded (`target_hold_limit`).
            On(After(P("target_hold_limit")), Outcome.NO_RESPONSE,
               do=[Mark(OUTCOME_NO_RESPONSE)]),
        ],
    ),
    _timeout("wrong", Outcome.WRONG_TARGET, OUTCOME_WRONG_TARGET),
    _timeout("astray", Outcome.ABORT, OUTCOME_ABORT),
    _timeout("broke", Outcome.TARGET_BREAK, OUTCOME_TARGET_BREAK),
]
#: **A catch's answer** (the revision's §4): keep looking at the fixation point for `catch_hold`
#: after the go, paid with the task's own reward, its amount the animal's and bounded as every
#: reward is; looking away is a false alarm, an error with the timeout ("An error, counted"); a
#: hold its bound ends first is no response.
CAUGHT = [
    State(
        "go",
        go=[
            On(
                Hold("fix", P("catch_hold")),
                Outcome.CORRECT_REJECT,
                do=[Mark(CATCH_FIXATION_HELD), Mark(OUTCOME_CORRECT_REJECT),
                    Mark(REWARD_COMMANDED), Reward("reward_correct")],
            ),
            On(Exited("fix"), "false_alarm",
               do=[*BLANK, Mark(CATCH_FIXATION_BREAK), Mark(TIMEOUT_ON)]),
            On(After(P("catch_hold_limit")), Outcome.NO_RESPONSE,
               do=[Mark(OUTCOME_NO_RESPONSE)]),
        ],
    ),
    _timeout("false_alarm", Outcome.FALSE_ALARM, OUTCOME_FALSE_ALARM),
]
#: The search's windows: the fixation point's, and each disc's a multiple of its own radius,
#: `object_window` (the console settings design's §5; the PI, 2026-11-16, "Grows in proportion"),
#: so it follows its disc.
SEARCH_WINDOWS = [
    Window("fix", at=(0.0, 0.0), radius=P("fix_window"), on="fix"),
    ObjectWindows(of="search", scale=P("object_window")),
]

search = _structure(ARRAY, SEARCHED, windows=SEARCH_WINDOWS)
target_absent = _structure(ABSENT, CAUGHT, kind=SPECIAL_TARGET_ABSENT)
odd_place_empty = _structure(EMPTY_PLACE, CAUGHT, kind=SPECIAL_ODD_PLACE_EMPTY)
distractor_alone = _structure(DISTRACTOR_ALONE, CAUGHT, kind=SPECIAL_DISTRACTOR_ALONE)
odd_one_alone = _structure(ODD_ALONE, SEARCHED, kind=SPECIAL_ODD_ONE_ALONE,
                           windows=SEARCH_WINDOWS)

#: **The stages** (§3.3, "Alone, Fade-in, Crowd"), easiest first. Each is one condition, worked
#: until the trainer moves on; its own value -- one disc, four, the distractors at full -- a
#: condition's, which a person's live value overrides. Each stage's bar is `move_up_bar` right of
#: its last `move_up_window` answers at its hardest step ("80% correct, last 50 trials"; "Hardest
#: step reached, 80% there"). The staircases' floors are settings, faint and four discs to start
#: (`fade_in_floor`, `crowd_floor`), and so are their steps and counts; **their hardest ends stay
#: fixed, 1.0 and 12**, since each is the stage's own definition of its hardest step -- the
#: distractors at full, so the odd one differs by color alone; the ring at its twelve discs --
#: which the bar to move up is judged at. Neither declares where it starts, so each starts, the
#: first time the run enters its stage, at the level nearest the run's value of its setting, which
#: the trainer picks at the run's start; **a stage the run returns to resumes at the level its
#: staircase was at when the run left it** (the PI, 2026-11-08: "Pick up where it left"). Each
#: names its hardest step in the trainer's words, which the prompt to move up says (the PI's
#: sketch, §3.5). **Each condition's `target=1` is fixed**: a stage is one condition worked on
#: until a person moves the run, its targets a minimum met at its first trial, so the number
#: changes nothing a trainer could want.
UP = (P("move_up_bar"), P("move_up_window"))
STEPPED = {"down": P("staircase_down"), "up": P("staircase_up")}
TRAINING = Plan(
    [
        Block("Alone", [Condition("alone", {"set_size": 1}, target=1)], criterion=UP),
        Block(
            "Fade-in",
            [Condition("fade_in", {"set_size": 4}, target=1)],
            criterion=UP,
            staircase=Staircase(
                "distractor_fraction", Steps(P("fade_in_floor"), 1.0, P("fade_in_step")),
                **STEPPED,
                hardest="the distractors are at full brightness",
            ),
        ),
        Block(
            "Crowd",
            [Condition("crowd", {"distractor_fraction": 1.0}, target=1)],
            criterion=UP,
            staircase=Staircase("set_size", Steps(P("crowd_floor"), 12, P("crowd_step")),
                                **STEPPED,
                                hardest="the ring holds all 12 discs"),
        ),
    ],
    # "Rig suggests, trainer confirms"; back below `move_back_bar` of the last `move_back_window`
    # ("Below 50% of the last 50"); each suggestion standing until its bar is missed by more than
    # `suggestion_margin` answers ("Stay up until 3 below", the PI, 2026-11-08).
    order=ByCriterion(fall_back=(P("move_back_bar"), P("move_back_window")), confirm=True,
                      margin=P("suggestion_margin")),
    # **The full task** (the revision's §5, the controller's reading, which the PI checks): Crowd at
    # its hardest -- its staircase held at its last level, all 12 discs, and its condition's
    # distractors at full -- from every pairing.
    full=FullTask("Crowd", {"pairings": EVERY_PAIRING}),
)

TASK = Task(
    structures={
        "search": search,
        "target_absent": target_absent,
        "odd_place_empty": odd_place_empty,
        "distractor_alone": distractor_alone,
        "odd_one_alone": odd_one_alone,
    },
    default="search",
    reaction_time=ReactionTime(
        state="go",
        to=("flight",),
        note=(
            "from the go, the frame the fixation point takes its act look, to the eye leaving "
            "the fixation window"
        ),
    ),
    choice=Choice(objects=("search.target", "search.distractor"), by="saccade"),
    meanings={
        "inter_trial": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "the blank screen between trials: time, not a judgment")),
        "timeout": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "the blank screen after an error, a consequence: it costs the animal time, and makes "
            "no trial easier or harder")),
        "go_delay": Meaning(CLEAR_CUT, CRITERION, raising=HARDER, note=(
            "a longer delay is a longer hold on the fixation point with the discs up, which the "
            "animal must keep before it may answer")),
        "catch_hold": Meaning(CLEAR_CUT, CRITERION, raising=HARDER, note=(
            "a longer hold on a catch is longer to keep looking at the fixation point after the "
            "go")),
        "fix_hold_limit": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a later bound leaves more time for a fixation hold the tracker's stalls hold up")),
        "landing_limit": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a later bound leaves more time for the answer's saccade to land")),
        "target_hold_limit": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a later bound leaves more time for the hold on the odd disc to complete")),
        "catch_hold_limit": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a later bound leaves more time for a catch's hold to complete")),
        "blink_grace": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a longer grace lets a longer blink pass without ending a held fixation")),
        "tracker_lost_grace": Meaning(CLEAR_CUT, CRITERION, raising=EASIER, note=(
            "a longer grace lets a longer tracker dropout pass without ending the trial")),
        **{name: Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how often this kind of special trial is drawn, not what a trial asks"))
           for name in ("target_absent_percent", "odd_place_empty_percent",
                        "distractor_alone_percent", "odd_one_alone_percent")},
        **{name: Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "the fixation point's shape, which tells the animal to hold or to act; no shape is "
            "easier in general"))
           for name in ("fix_look", "fix_act_look")},
        **{name: Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "the ring's hole, where the fixation point is a ring"))
           for name in ("fix_hole", "fix_act_hole")},
        **{name: Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "the fixation point's hue, which at no saturation shows none"))
           for name in ("fix_color", "fix_act_color")},
        **{name: Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "how much hue the fixation point shows, its brightness held"))
           for name in ("fix_saturation", "fix_act_saturation")},
        "set_size": Meaning(EXPECTED, STIMULUS, raising=HARDER, note=(
            "more discs are more to look past while the animal learns the odd one; once it finds "
            "the odd one by color, a denser ring can make it stand out more, as in a trained "
            "pop-out search"), overrides=(
            "a training stage: Crowd adds discs as its harder steps (the PI, 2026-11-07)")),
        "distractor_fraction": Meaning(EXPECTED, STIMULUS, raising=HARDER, note=(
            "dimmer distractors let the odd one stand out by brightness; at full they match its "
            "luminance and it differs by color alone. An animal already using color may find "
            "bright distractors no harder")),
        "odd_color": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which of the four colors the odd one takes, drawn from the pool each trial; the four "
            "are equal in macaque luminance, so none is easier by brightness")),
        "distractor_color": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which of the four colors the distractors take, drawn from the pool each trial")),
        "pairings": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which pairings of odd color and distractor color are drawn; widening the pool adds "
            "pairings, not difficulty")),
        "disc_size": Meaning(EXPECTED, STIMULUS, raising=EASIER, note=(
            "larger discs are easier to see and to land a saccade on; the windows are their own "
            "settings")),
        "ring_radius": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "how far the ring sits from fixation, as the shared list's array_eccentricity: what "
            "moving it does depends on the search")),
        "fix_size": Meaning(EXPECTED, STIMULUS, raising=EASIER, note=(
            "a larger fixation point is easier to find")),
        "fix_act_size": Meaning(EXPECTED, STIMULUS, raising=EASIER, note=(
            "a larger fixation point is easier to find, as its hold look's size")),
        "fix_act_luminance": Meaning(EXPECTED, STIMULUS, raising=EASIER, relative_to=BACKGROUND,
                                     note=(
            "a point farther in luminance from the background is easier to find, as its hold "
            "look's brightness")),
        "color_luminance": Meaning(EXPECTED, STIMULUS, raising=EASIER, relative_to=BACKGROUND,
                                   note=(
            "brighter discs on black are easier to see, as a target's luminance is; every color "
            "and the distractors' share move together, so the odd one still differs by color "
            "alone at full")),
        "move_up_bar": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "when the rig suggests moving up or widening the pool, not what a trial asks")),
        "move_up_window": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many answers the bar to move up reads, not what a trial asks")),
        "move_back_bar": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "when the rig suggests moving back, not what a trial asks")),
        "suggestion_margin": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how long a suggestion stands once made, not what a trial asks")),
        "move_back_window": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many first answers the bar to move back reads, not what a trial asks")),
        "staircase_down": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many right in a row step the staircase harder, between trials; its level is "
            "the difficulty, not this")),
        "staircase_up": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many wrong in a row step the staircase easier, between trials")),
        "fade_in_step": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how far apart Fade-in's levels are; the level the staircase gives is the difficulty")),
        "crowd_step": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many discs apart Crowd's levels are; the level the staircase gives is the "
            "difficulty")),
        "fade_in_floor": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "where Fade-in's staircase starts at its faintest; the level the staircase gives is the "
            "difficulty")),
        "crowd_floor": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how few discs Crowd's staircase starts at; the level the staircase gives is the "
            "difficulty")),
    },
    # The rig fixes the head, as the lab's other rig tasks need it.
    needs_fixed_head=True,
    pool=POOL,
    plans={"training": TRAINING},
    draws={
        # The ring's direction, anywhere, each trial; a trial a drum brings back (should the
        # trainer switch drumming on) keeps its place, as it keeps its pairing. **Fixed, the whole
        # circle**: the odd one's place on the ring is random each trial, so the animal learns its
        # color, not a place; a narrower draw would teach a place.
        "array_rotation": Uniform(0.0, 360.0, repeat=SAME),
        # The fixation hold, non-aging from 0.75 to 1.25 s, the PI's published foreperiod "to
        # reduce expectancy" [@westerberg2020priming] (the revision's §6), drawn afresh on a trial
        # brought back, so a repeat teaches no wait.
        "fix_hold": NonAging.between(0.75, 1.25, repeat=FRESH),
    },
    # **The rules, each one box with one Apply** (wl-xcon's console interface design, goal 8; the
    # PI, 2026-11-19, "One box after Timing"), read as the trainer says them: each setting's field
    # stands in its place, the bars as percents.
    groups=(
        Group("Special trials", ("target_absent_percent", "odd_place_empty_percent",
                                 "distractor_alone_percent", "odd_one_alone_percent",
                                 "catch_hold"),
              "Of every 100 trials: {target_absent_percent} target absent, "
              "{odd_place_empty_percent} odd place empty, {distractor_alone_percent} a "
              "distractor alone, {odd_one_alone_percent} the odd one alone; a catch is held "
              "{catch_hold}"),
        Group("Move up", ("move_up_bar", "move_up_window"),
              "Move up when at least {move_up_bar} of the last {move_up_window} answers at the "
              "hardest step are right"),
        Group("Move back", ("move_back_bar", "move_back_window"),
              "Move back when fewer than {move_back_bar} of the last {move_back_window} answers "
              "are right"),
        Group("Staircase", ("staircase_down", "staircase_up"),
              "One level harder after {staircase_down} right in a row, one level easier after "
              "{staircase_up} wrong in a row"),
    ),
    # **The special trials** (the revision's §4), each kind's share cumulated in this order as
    # each trial is drawn; three catches and the probe.
    specials=(
        Special("target_absent", P("target_absent_percent"), "target_absent"),
        Special("odd_place_empty", P("odd_place_empty_percent"), "odd_place_empty"),
        Special("distractor_alone", P("distractor_alone_percent"), "distractor_alone"),
        Special("odd_one_alone", P("odd_one_alone_percent"), "odd_one_alone"),
    ),
)
