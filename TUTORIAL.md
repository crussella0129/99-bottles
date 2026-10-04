# 99 Bottles: A Code-Golf Tutorial in Seven Rounds

This repo holds four attempts at the [99 Bottles of Beer](https://code.golf/99-bottles-of-beer#python) hole on code.golf. This tutorial goes through them in order: what each round changed, what it taught, and the bug one of them introduced. Then it continues for three more rounds, from 730 bytes down to 241.

You can check every claim below yourself. Every byte count was measured with the included `check.py`, and every code block was run through it.

---

## Setup

```bash
git clone https://github.com/crussella0129/99-bottles
cd 99-bottles
python check.py wallbeers0.py wallbeers1.py wallbeers2.py wallbeers3.py
```

(Use `python3` if your system's `python` is Python 2. Any Python 3.7+ works.)

You should see:

```
PASS   730 bytes  wallbeers0.py
FAIL   527 bytes  wallbeers1.py
      trailing whitespace in source on line 3
      line 295 got:      '1 bottle of beer on the wall, 1 bottle.'
      line 295 expected: '1 bottle of beer on the wall, 1 bottle of beer.'
PASS   485 bytes  wallbeers2.py
      trailing whitespace in source on lines 3, 6
PASS   450 bytes  wallbeers3.py
      trailing whitespace in source on lines 2, 5
```

`check.py` does four jobs:

1. **Judges like code.golf.** It builds the expected song, runs your program, then strips trailing whitespace from every line and trailing newlines from the end. That is the rule code.golf's own judge applies (the `perLineTrimmer` regex in [`hole/play.go`](https://github.com/code-golf/code-golf/blob/master/hole/play.go)). Then it compares.
2. **Has a `--strict` mode.** `python check.py --strict ...` turns the trimming off and compares byte-for-byte. It will catch whitespace you can't see.
3. **Counts bytes the same way on every OS.** These files were saved on Windows, which ends each line with two bytes (`\r\n`). Linux ends lines with one (`\n`). A golf score shouldn't depend on your OS, so `check.py` counts `\r\n` as one byte and ignores the final newline.
4. **Flags free bytes.** Spaces or tabs at the end of a source line do nothing but still count toward your score. `check.py` lists the lines that have them.

> The expected text in `check.py` is the standard lyric. If code.golf ever disagrees with it, code.golf wins. Paste your solution there to confirm.

### Scoreboard

| Round | File | Bytes | Judge | `--strict` | Idea |
|---|---|---:|---|---|---|
| 0 | `wallbeers0.py` | 730 | PASS | FAIL | One `print` per case |
| 1 | `wallbeers1.py` | 527 | **FAIL** | FAIL | Words → variables |
| 2 | `wallbeers2.py` | 485 | PASS | FAIL | Phrases → variables |
| 3 | `wallbeers3.py` | 450 | PASS | **PASS** | Use the loop variable |
| 4 | below | 379 | PASS | PASS | One function for "N bottles" |
| 5 | below | 338 | PASS | FAIL | The song is a cycle: mod 100 |
| 6 | below | 241 | PASS | FAIL | Golf syntax |

---

## The spec: what actually varies?

Math first, then code. Every verse is the same template with one number, *n*, filled in.

**In words:**

> verse(n) = **count(n)** on the wall, **count(n)**.\
> **action(n)**, **count(next(n))** on the wall.

Only three things change with *n*:

- **count(n)** is "no more bottles of beer" at 0, "1 bottle of beer" at 1, and "*n* bottles of beer" otherwise.
- **action(n)** is "Take one down and pass it around" when *n* ≥ 1, and "Go to the store and buy some more" when *n* = 0.
- **next(n)** is *n* − 1, except that after 0 comes 99.

There is one more detail: "no more" is capitalized when it starts a line.

**In notation:**

```math
\text{count}(n) = \begin{cases} \text{no more bottles of beer} & n = 0 \\ \text{1 bottle of beer} & n = 1 \\ n\ \text{bottles of beer} & 2 \le n \le 99 \end{cases}
\qquad
\text{next}(n) = (n - 1) \bmod 100
```

Each round below gives a different answer to one question: **where in the code is each of these facts written, and how many times?** Rounds 0–3 compress the *text*. Rounds 4–6 compress the *logic*.

---

## Round 0: one branch per case (730 bytes)

```python
wallbeers=99
while wallbeers >=0:
	if wallbeers>2:
		print(f"{wallbeers} bottles of beer on the wall, {wallbeers} bottles of beer.\nTake one down and pass it around, {wallbeers-1} bottles of beer on the wall.\n")
	elif wallbeers==2:
		print(f"{wallbeers} bottles of beer on the wall, {wallbeers} bottles of beer. \nTake one down and pass it around, {wallbeers-1} bottle of beer on the wall.\n")
	elif wallbeers==1:
		print(f"{wallbeers} bottle of beer on the wall, {wallbeers} bottle of beer. \nTake one down and pass it around, no more bottles of beer on the wall.\n")
	else: print("No more bottles of beer on the wall, no more bottles of beer. \nGo to the store and buy some more, 99 bottles of beer on the wall.")
	wallbeers-=1
```

There are four branches: *n* > 2, *n* = 2, *n* = 1, and *n* = 0. Why does 2 need its own branch? Because the *next* count is 1, which is singular. The plural rule has leaked into the branch structure: the branch for *n* is really checking what count(*n* − 1) will look like.

**What's good:** the structure mirrors the spec, and every sentence can be read and proofread as English.

**What it costs:** "bottles of beer on the wall" is written out in full in every branch. That repetition is why it's 730 bytes.

**The hidden flaw is whitespace you can't see.** Look closely at the `== 2`, `== 1` and `else` branches: `beer. \nTake`. There's a space before the `\n`. It's invisible in a terminal. Make it visible:

```bash
python check.py --strict wallbeers0.py
```

```
FAIL   730 bytes  wallbeers0.py
      line 292 got:      '2 bottles of beer on the wall, 2 bottles of beer. '
      line 292 expected: '2 bottles of beer on the wall, 2 bottles of beer.'
```

code.golf forgives trailing spaces. `diff`, checksums, and most test suites don't. The lesson: whitespace is output too.

---

## Round 1: words into variables (527 bytes, −203)

```python
a=99
b=a
c="bottle" 
d="of beer"
e="on the wall"
f="Take one down and pass it around,"
g="more"
h="Go to the store and buy some more,"
for i in range(a, -1, -1):
    if i > 2:
       print(f"{b} {c}s {d} {e}, {b} {c}s {d}.\n{f} {b-1} {c}s {d} {e}.\n")
    elif i == 2:
       print(f"{b} {c}s {d} {e}, {b} {c}s {d}.\n{f} {b-1} {c} {d} {e}.\n")
    elif i == 1:
       print(f"{b} {c} {d} {e}, {b} {c}.\n{f} no {g} {c}s {d} {e}.\n")
    else:
       print(f"No {g} {c}s {d} {e}, no {g} {c}s {d}.\n{h} 99 {c}s {d} {e}.")
    b-=1
```

This round makes two changes:

1. **`for i in range(a, -1, -1)`** replaces the `while` loop. `range(start, stop, step)` never includes `stop`, so to count down *to 0* you stop at −1.
2. **Every repeated word gets a one-letter name.** The plural is built by appending an `s` to a name, as in `{c}s`.

That saves 203 bytes, but `check.py` says **FAIL**:

```
line 295 got:      '1 bottle of beer on the wall, 1 bottle.'
line 295 expected: '1 bottle of beer on the wall, 1 bottle of beer.'
```

In the `i == 1` branch, the second half is `{b} {c}.`, which is missing `{d}`.

### Why this bug is the most important lesson here

In Round 0 the template *was* the sentence, so you could proofread it. In Round 1, `{b} {c} {d} {e}, {b} {c}.` no longer looks like English. Your eye can't spot a missing word in a row of letters. **Compressing code destroys your ability to proofread it.**

The fix is not "be more careful." The fix is a mechanical check. Golfed code needs a test harness *more* than readable code does, because you can no longer act as the test harness yourself. That's why `check.py` exists.

**A second warning sign: two counters.** `i` is the loop variable and `b` is decremented by hand, but they always hold the same value. Redundant state is two things that must stay in sync, which is a bug waiting to happen. Round 3 removes it.

> **Try it:** fix line 15 of `wallbeers1.py` (one token is missing) and re-run `python check.py wallbeers1.py` until it passes.

---

## Round 2: phrases into variables (485 bytes, −42)

```python
a=99
b="bottle"
c=f"{b}s of beer" 
d=f"{c} on the wall"
e="Take one down and pass it around,"
f=f"{b} of beer" 
g=f"{f} on the wall"
h="o more"
i="Go to the store and buy some more,"
for j in range(a, -1, -1):
    if j > 2:
       print(f"{a} {d}, {a} {c}.\n{e} {a-1} {d}.\n")
    elif j == 2:
       print(f"{a} {d}, {a} {c}.\n{e} {a-1} {g}.\n")
    elif j == 1:
       print(f"{a} {g}, {a} {f}.\n{e} n{h} {d}.\n")
    else:
       print(f"N{h} {d}, n{h} {c}. \n{i} 99 {d}.")
    a-=1
```

The variables now hold bigger chunks. `d` is the whole phrase "bottles of beer on the wall", and `g` is its singular form. Bigger variables mean fewer `{}` references in each template, and that means fewer bytes. The Round 1 bug is gone too: verse 1 now uses `{f}`, a complete phrase that can't lose a word.

**The best trick in the repo is `h="o more"`.** The song needs both "No more" (at the start of a line) and "no more" (mid-line). They differ only in the first letter, so Round 2 stores the shared tail and writes `N{h}` or `n{h}`.

**Left over:** `. \n` in the last branch. That's one more invisible trailing space (`--strict` will show you line 298).

### When does a variable pay for itself? The break-even math

**In words:** a variable saves bytes when the text you delete is longer than the text you add.

- You delete the string *k* times, which is *k · L* bytes (*L* = the string's length).
- You add the definition once. `x="..."` plus its newline is *L* + 5 bytes.
- You add a reference each time. `{x}` is 3 bytes, so 3*k* in total.

**In notation:**

```math
\text{savings}(k, L) = kL - (L + 5) - 3k = (k-1)L - 3k - 5
\qquad\Longrightarrow\qquad
\text{savings} > 0 \iff L > \frac{3k + 5}{k - 1}
```

| Uses (*k*) | String must be at least (*L* ≥) |
|---:|---:|
| 2 | 12 |
| 3 | 8 |
| 4 | 6 |
| 10 | 4 |

**Tested against a real measurement:** in Round 6 below, moving `" on the wall"` into a variable (*L* = 12, *k* = 2) should save (1)(12) − 6 − 5 = **1 byte**. Measured result: 241 → 240, exactly 1 byte. The formula also tells you when a trick isn't worth making the code harder to read.

*(This formula assumes each reference sits inside an f-string. Outside one, `+x+` costs a different amount. Redo the arithmetic for your own case.)*

---

## Round 3: use the loop variable (450 bytes, −35)

```python
b=" bottle"
c=f"{b}s of beer" 
d=f"{c} on the wall"
e="Take one down and pass it around, "
f=f"{b} of beer" 
g=f"{f} on the wall"
h="o more"
i="Go to the store and buy some more, "
for j in range(99, -1, -1):
   if j > 2:
      print(f"{j}{d}, {j}{c}.\n{e}{j-1}{d}.\n")
   elif j == 2:
      print(f"{j}{d}, {j}{c}.\n{e}{j-1}{g}.\n")
   elif j == 1:
      print(f"{j}{g}, {j}{f}.\n{e}n{h}{d}.\n")
   else:
      print(f"N{h}{d}, n{h}{c}.\n{i}99{d}.")
```

- **The second counter is gone.** The loop variable `j` *is* the count, so `a` and `a-=1` are no longer needed. There is now one source of truth.
- **Spaces moved into the data.** With `b=" bottle"` and `e="...around, "`, the templates become `{j}{d}` instead of `{j} {d}`. A space stored inside a variable is paid for once instead of on every use.
- **The output is byte-for-byte exact.** This is the only one of the original four that passes `--strict`.

> **Free bytes hiding in the source.** Lines 2 and 5 end with an invisible space (`c=f"{b}s of beer" `). Round 0 had invisible spaces in its *output*; Rounds 1–3 have them in the *source*, where they count toward your score. There are five across the repo, and `check.py` lists them. Deleting Round 3's two brings it to 448 bytes.
>
> A Linux trap: `grep -n ' $' wallbeers*.py` finds **nothing**. These are Windows files, so every line really ends in `" \r"`, not `" "`. `grep -nP ' \r?$' wallbeers*.py` finds all five. Line endings are characters you can't see, too.

Total progress: 730 → 450, which is **38% smaller**.

**What's still redundant:** the singular/plural rule is still written down twice as data (`c`/`f` and `d`/`g`), and the four-way `if` is still there. Rounds 0–3 compressed the *text*. The branches are *logic*, and they exist for only three reasons: the three facts from the spec. Write each fact down once and the branches collapse.

---

## Round 4: one function for count(n) (379 bytes, −71)

> **Try it first:** write `bottles(n)` so it returns "no more bottles of beer", "1 bottle of beer", or "*n* bottles of beer". The song then becomes a loop plus a final verse.

<details>
<summary>Solution</summary>

```python
def bottles(n):
    return f"{n or 'no more'} bottle{'s' if n != 1 else ''} of beer"

for n in range(99, 0, -1):
    print(f"{bottles(n)} on the wall, {bottles(n)}.")
    print(f"Take one down and pass it around, {bottles(n - 1)} on the wall.\n")
print(f"No more bottles of beer on the wall, {bottles(0)}.")
print(f"Go to the store and buy some more, {bottles(99)} on the wall.")
```

</details>

Two Python facts do all the work:

- **`n or 'no more'`**: `or` returns its first *truthy* operand. `0` is falsy, so `bottles(0)` gets `'no more'`. Any other `n` is truthy and returns itself.
- **`'s' if n != 1 else ''`**: the plural rule, now written down **exactly once**.

The special case for *n* = 2 is gone. It only existed because Round 0 spelled out the *next* count by hand. Now `bottles(n - 1)` gets 1 right by itself. This round is longer to read than Round 3, but it's 71 bytes shorter and much easier to check.

---

## Round 5: the song is a cycle (338 bytes, −41)

The "99" in the last verse isn't a special case. It's what follows 0 when you count down on a 100-position clock:

```math
\text{next}(n) = (n - 1) \bmod 100 \quad\Rightarrow\quad \text{next}(0) = 99
```

In Python, `(0 - 1) % 100 == 99`, so the final verse becomes an ordinary loop iteration.

The capital "No" is handled by **`str.capitalize()`**, which uppercases the first character and lowercases the rest. It turns "no more bottles of beer" into "No more bottles of beer" and leaves "99 bottles of beer" unchanged, because `'9'` has no uppercase form. This is only safe because the rest of the string is already lowercase.

<details>
<summary>Solution</summary>

```python
def bottles(n):
    return f"{n or 'no more'} bottle{'s' if n != 1 else ''} of beer"

for n in range(99, -1, -1):
    action = "Take one down and pass it around" if n else "Go to the store and buy some more"
    print(f"{bottles(n).capitalize()} on the wall, {bottles(n)}.")
    print(f"{action}, {bottles((n - 1) % 100)} on the wall.\n")
```

</details>

Only one fact still needs an `if`: which action to sing.

**The cost:** the last verse now ends with an extra `\n`, which leaves one blank line at the end. code.golf's judge trims trailing newlines, so this passes there, but `--strict` fails (line 301). It's a real trade-off, and you should know you're making it.

### The Rust trap: two meanings of `%`

Integer division has two common conventions. Both satisfy *a* = *q*·*b* + *r*, but they round the quotient *q* differently:

| Convention | Rounds *q* toward | −1 ÷ 100 gives | Languages |
|---|---|---|---|
| Truncated | zero | *q* = 0, *r* = **−1** | Rust `%`, C, C++, Java, JavaScript, Go |
| Floored | −∞ | *q* = −1, *r* = **99** | Python `%`, Ruby |

If you port Round 5 to Rust, `(n - 1) % 100` gives −1 at *n* = 0 and prints "-1 bottles". Use `rem_euclid`, which always returns a non-negative remainder:

<details>
<summary>Rust port of Round 5 (compiled and checked against the reference)</summary>

```rust
fn bottles(n: i32) -> String {
    match n {
        0 => "no more bottles of beer".to_string(),
        1 => "1 bottle of beer".to_string(),
        _ => format!("{n} bottles of beer"),
    }
}

fn main() {
    assert_eq!(-1 % 100, -1); // Rust's % keeps the dividend's sign...
    assert_eq!((-1i32).rem_euclid(100), 99); // ...rem_euclid is Python's %.
    for n in (0..=99).rev() {
        let now = bottles(n);
        let action = if n > 0 { "Take one down and pass it around" } else { "Go to the store and buy some more" };
        let mut first = now.clone();
        first[..1].make_ascii_uppercase();
        println!("{first} on the wall, {now}.");
        println!("{action}, {} on the wall.\n", bottles((n - 1).rem_euclid(100)));
    }
}
```

</details>

---

## Round 6: golf syntax (241 bytes, −97)

This is the same algorithm as Round 5. Only the syntax changes.

```python
b=lambda n:f"{n or'no more'} bottle{'s'[n==1:]} of beer"
for n in range(99,-1,-1):print(f"{b(n).capitalize()} on the wall, {b(n)}.\n{n and'Take one down and pass it around'or'Go to the store and buy some more'}, {b(~-n%100)} on the wall.\n")
```

Each trick can be checked in a Python REPL:

| Trick | Replaces | Why it works |
|---|---|---|
| `'s'[n==1:]` | `'s' if n!=1 else ''` | `bool` is a subclass of `int`, so `True` acts as 1 in a slice: `'s'[1:] == ''` and `'s'[0:] == 's'` |
| `n and X or Y` | `X if n else Y` | This was the idiom before Python 2.5 added `if`/`else` expressions. It's only safe here because `X` is a non-empty string, which is truthy |
| `~-n` | `n-1` | In two's complement, `~x == -x-1`, so `~(-n) == n-1`. Unary operators bind tighter than `%`, so `~-n%100` needs no parentheses. That saves 2 bytes over `(n-1)%100` |
| `n or'no more'` | `n or 'no more'` | The tokenizer doesn't need a space before a string literal |
| `lambda` + one line | `def` + indented body | Removes `return`, the newline, and the indentation |

Total progress: 730 → 241, which is **67% smaller** with the same output.

---

## How good is 241 bytes? A benchmark you can measure

The song is **11,884 bytes**. Here is how that compares with general-purpose compressors on the same text:

| | Bytes |
|---|---:|
| The song itself | 11,884 |
| `zlib` level 9 | 864 |
| **Round 0** | **730** |
| `bz2` level 9 | 575 |
| `lzma` (raw LZMA2, extreme preset) | 489 |
| **Round 3** | **450** |
| **Round 6** | **241** |

Reproduce the compressor rows (from the repo folder):

```bash
python -c "import check,zlib,bz2,lzma; s=check.expected().rstrip().encode(); print(len(s), len(zlib.compress(s,9)), len(bz2.compress(s,9)), len(lzma.compress(s,format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA2,'preset':9|lzma.PRESET_EXTREME}])))"
```

Round 0 already beats zlib, and Round 3 beats lzma. The compressor sizes also leave out the decompressor, which your programs are effectively carrying inside themselves. A compressor can only find repeated byte strings. Your program knows *why* they repeat, because it knows the song is counting. The more of the song's reasoning your code captures, the less text it has to store.

That idea has a formal name: **Kolmogorov complexity**. *K*(*s*) is the length of the shortest program that prints the string *s*. Every golf solution is an upper bound on it: *K*<sub>Python</sub>(song) ≤ 241 bytes.

### Wild fact: you can never prove you've won

*K* is **uncomputable**. **Chaitin's incompleteness theorem** (1974) is a direct descendant of Gödel's. It says that any consistent formal system that has a computable set of axioms and is strong enough for arithmetic has some fixed bound *L*, and the system cannot prove *K*(*s*) > *L* for *any* specific string *s*. So once programs get long enough, no proof can ever show "no shorter Python program prints this song." Leaderboards are how people compete when the optimum can't be proven.

Further reading: Donald Knuth's joke paper *"The Complexity of Songs"* (SIGACT News, 1977; reprinted in Communications of the ACM, 1984) asks how the size of a song's lyrics grows with the length of the song.

---

## Your turn

1. **Fix Round 1.** One token is missing on line 15 of `wallbeers1.py`. Re-run `check.py` until it passes.
2. **Remove the invisible spaces.** Edit `wallbeers0.py` and `wallbeers2.py` until `python check.py --strict` passes both. Then delete the five trailing spaces in the *source* files and watch the byte counts drop.
3. **Make Round 5 pass `--strict`.** Two approaches work: `print`'s `end=` argument, or building a list of verses and joining them with `"\n\n"`. Which one costs fewer bytes?
4. **Beat 241 bytes.** Moving `" on the wall"` into a variable saves exactly 1 byte, as the formula above predicts. Other directions, **not yet measured**, so measure them yourself:
   - `%`-formatting instead of f-strings
   - a `while` loop that avoids `range(99,-1,-1)`
   - storing both action phrases in one string and slicing out the one you need
5. **Port to Rust.** Watch out for `%`. `check.py` only runs Python, so compare your Rust output against a Python solution that passes. Save the Round 5 solution as `round5.py`; then on Linux, `rustc bottles.rs && diff <(./bottles) <(python round5.py)` should print nothing.
6. **Keep the history.** Commit each new attempt as `wallbeers4.py`, `wallbeers5.py`, and so on, and add its row to the scoreboard. The git log becomes the tutorial's next chapter.
