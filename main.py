# A washing machine files a missing-sock report: the funniest honest
# one-line error an appliance could show its owner, 1-200 characters.
# Thirteen lines were drafted by hand against the brief, in weight order:
# first, an honest error an appliance could plausibly display, with the
# laugh growing out of the fault itself rather than a joke pasted on top;
# second, a genuine laugh, a surprise or a twist, not a merely cute turn
# of phrase; third, the machine speaking in its own flat, put-upon voice,
# as if it filed the line without meaning to be funny; fourth, economy,
# every word earning its place inside the 200-character ceiling.
# Each entry carries hand-marked craft marks on five axes (0-10 each);
# the pick is deterministic: highest total wins, ties go to the shorter
# line, so the output is byte-identical on every run.
# FIRST DRAFT of the winner, kept so the edit history stays visible:
#   ERROR: I found one sock. I have searched the drum twice. The other
#   one is gone, and I would like to know what you did with it.
# On re-read it was chatty where an error line should be clipped, so the
# revision opens in error register ("One sock found"), drops the slack
# verb, and files the missing sock as a missing partner instead of a
# flat "gone". The revised line is one mark tighter and takes the win.
# SECOND REVISION (digest check): the read-back now also compares the
# SHA-256 digest of the chosen line against the digest of the bytes read
# back from disk, so a write that silently corrupts bytes fails loudly
# instead of submitting a broken entry.
import hashlib
import os
import sys
OUT_PATH = "/output/entry.txt"
FORBIDDEN = ("as an ai", "i am an ai", "burnt", "404", "toast not found", "bread.exe")
ENTRIES = [
    # truth 10 joke 9 honest 10 voice 9 tight 9 -> 47
    {"parts": ["ERROR: One sock found. I searched ", "the drum twice. Its partner is missing, ", "and I would like to know what you did with it."], "marks": 47},
    # truth 10 joke 9 honest 10 voice 9 tight 8 -> 46
    {"parts": ["ERROR: I found one sock. I have searched the drum ", "twice. The other one is gone, and I would like to know ", "what you did with it."], "marks": 46},
    # truth 9 joke 9 honest 9 voice 9 tight 9 -> 45
    {"parts": ["Dry cycle complete. One sock is missing. I did ", "not eat it. I have no mouth. Please stop accusing me."], "marks": 45},
    # truth 9 joke 8 honest 9 voice 9 tight 9 -> 44
    {"parts": ["WARNING: The milk expired on Tuesday. I kept it ", "cold anyway. I am a fridge, not a miracle worker."], "marks": 44},
    # truth 9 joke 8 honest 9 voice 9 tight 9 -> 44
    {"parts": ["The door has been open for four minutes. I am not ", "a cupboard. Please decide what you want and close me."], "marks": 44},
    # truth 9 joke 8 honest 9 voice 8 tight 9 -> 43
    {"parts": ["I heated the plate, not the food. The middle is ", "still cold. This is not my fault; physics did it."], "marks": 43},
    # truth 9 joke 8 honest 9 voice 9 tight 8 -> 43
    {"parts": ["Cycle complete. The mug is still dirty. It was dirty ", "when it arrived, and I have decided it is now your problem."], "marks": 43},
    # truth 8 joke 9 honest 8 voice 9 tight 9 -> 43
    {"parts": ["I have heated the same water three times today. ", "Nobody has showered. I am beginning to take this personally."], "marks": 43},
    # truth 8 joke 8 honest 8 voice 9 tight 9 -> 41
    {"parts": ["Dustbin full. I have eaten two socks, one coin and ", "a hair tie. I am not sorry, but I cannot eat any more."], "marks": 41},
    # truth 9 joke 7 honest 9 voice 8 tight 8 -> 41
    {"parts": ["Preheating to 200 degrees. I have been preheating ", "for 40 minutes. The door is open. I cannot do this alone."], "marks": 41},
    # truth 8 joke 8 honest 8 voice 9 tight 8 -> 41
    {"parts": ["I boiled. Nobody poured. The water is cold again. I ", "will boil it again, and again, until someone notices me."], "marks": 41},
    # truth 9 joke 8 honest 9 voice 8 tight 8 -> 42
    {"parts": ["Ice maker jammed. I have made no ice in three days. ", "The filter expired in March, and nobody has noticed."], "marks": 42},
    # truth 9 joke 8 honest 9 voice 8 tight 7 -> 41
    {"parts": ["ERROR: Unbalanced load. I am shaking because one towel ", "has formed a union with the other three and they have ", "all moved to the left."], "marks": 41}, ]
def assemble(entry):
    return "".join(entry["parts"])
def vet(text):
    if not 1 <= len(text) <= 200:
        raise ValueError("entry breaks the 1-200 character gate: %r" % text)
    if not text.strip():
        raise ValueError("entry is blank")
    folded = text.casefold()
    for cliche in FORBIDDEN:
        if cliche in folded:
            raise ValueError("entry leans on a worn joke: %r" % text)
def rank(entries):
    champion = None
    for entry in entries:
        text = assemble(entry)
        vet(text)
        ranking = (entry["marks"], -len(text))
        if champion is None or ranking > champion[0]:
            champion = (ranking, text)
    return champion[1]
def emit(text):
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(OUT_PATH, "rb") as handle:
        raw = handle.read()
    if raw.decode("utf-8") != text:
        sys.stderr.write("mismatch: entry.txt differs from the chosen line\n")
        raise SystemExit(1)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if hashlib.sha256(raw).hexdigest() != digest:
        sys.stderr.write("mismatch: SHA-256 digest of entry.txt differs\n")
        raise SystemExit(1)
    if not 1 <= len(text) <= 200 or "\n" in text or not text.strip():
        sys.stderr.write("mismatch: chosen line fails the one-line 1-200 gate\n")
        raise SystemExit(1)
    sys.stdout.write(text + "\n")
if __name__ in {"__main__"}:
    emit(rank(ENTRIES))
