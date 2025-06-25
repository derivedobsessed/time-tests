In this exercise, you will be given a few lines of code that perform a certain task (that you will have to understand) and then write an automated test that checks whether that task is performed correctly.

## Step 0

If you haven't already, fork this repository and clone it on your computer, and use `uv` to create a new environment for it (with `pytest`):

```bash
uv init
uv add --dev pytest
```

> [!TIP]
> You can find useful information on the following chapters of our notes on [Testing basics](https://github-pages.arc.ucl.ac.uk/rsd-summerschool/ch02testsandsmells/01testingbasics.html), [The Fields of Saskatchewan](https://github-pages.arc.ucl.ac.uk/rsd-engineeringcourse/ch03tests/02SaskatchewanFields.html) and [Test frameworks](https://github-pages.arc.ucl.ac.uk/rsd-summerschool/ch02testsandsmells/03pytest.html).

## Step 1: Understanding the existing code
- Spend some time reading the code, try to run it and see whether you understand what's going on.
- Have you seen [`datetime`](https://docs.python.org/3.7/library/datetime.html) before?
- Play using your favourite tool (notebook, terminal, scripts) with the functions and objects used in `times.py`.

> [!TIP]
> Imagine we have two instruments. The first one takes measurements for 5 minutes, stops for 1, and takes measurements again for another 5 minutes. The other one measures for 1 minute, and has a gap of 2 minutes between intervals. If we start our measurments with the first one at `t=0` and the second one starts at `t=2`, then we would have a pattern of observations like:
> ```mermaid
> block-beta
>   columns 13
>   a["obs 1 [5min]"]:5 space:1 c["obs 1 [5min]"]:5 space:2
>   space:2 d["obs 2 [1min]"]:1 space:2 e["obs 2 [1min]"]:1 space:2 f["obs 2 [1min]"]:1 space:2 g["obs 2 [1min]"]:1 space:1
>   h["00:00"]:1 j["01:00"]:1 k["02:00"]:1 l["03:00"]:1 m["04:00"]:1 n["05:00"]:1 o["06:00"]:1 p["07:00"]:1 q["08:00"]:1 r["09:00"]:1 s["10:00"]:1 t["11:00"]:1 u["12:00"]:1
> ```
>
> The `time_range` function generates the observation blocks for a given start and end time, a number of intervals and a duration for the gaps.  For the first row above, this would be:
> `"2025-06-01 00:00:00", "2025-06-01 00:11:00", 2, 60`
> and for the second:
> `"2025-01-01 00:02:00", "2025-01-01 00:12:00", 4, 120`.  
> And the `compute_overlap_time` should provide:
> ```python
> [('2020-01-01 00:02:00', '2020-01-01 00:03:00'),  # first interval
>  ('2020-01-01 00:08:00', '2020-01-01 00:09:00')]  # second interval 
> ```

## Step 2: Writing a unit test

- Create a new file called `test_times.py` in the same directory where `times.py` is.
- Make the `overlap_time` function accessible to that file. (*Hint*: You need to `import` the file).
- Move the content from the `if __name__ ...` block from `times.py` to a function called `test_given_input` into `test_times.py`
  and fill the gaps for `result` and `expected`. (For now, you can copy the output of the program as the expected value, as if being a regression test)
```python
def test_given_input():
    ... 
    result = ... 
    expected = ...
    assert result == expected
```

## Step 3: Running the tests
- run `pytest` on that directory and see whether the test is picked up by `pytest` and whether it passes. If the test doesn't pass, see if you can find what is going wrong.

> [!NOTE]
> If you have created the environment using `uv` and installed `pytest` with it then you need to run `uv run pytest` or use the VS Code testing menu.

## Step 4: Push to GitHub
- When you are happy with your solution (or want some feedback!):
    - Push your new code to your own fork.
    - On GitHub, open a pull request from your fork to the original repository.
    - In the description, include the text as required in the issue for this exercise. This will link your PR to this issue.
    - On the PR text, comment on what you found difficult or interesting, or something you learned.
- Continue with the remaining steps (7. - 9.) on the following issue in the Classwork repository.
