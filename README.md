# PyProgressTerm

## Description

This package implement a customizable progress bar and rotating animation.
 - timed progress bar
 - colored progress bar
 - rotating animation in progress bar

## Requirements
This package require:
 - python3
 - python3 Standard Library

## Installation
```bash
pip install PyProgressTerm
```

## Usages

### Command line
```bash
ProgressTerm -h                                # Help message
ProgressTerm -r                                # Rotating animation
ProgressTerm -m rotating                       # Progress bar with rotating animation
ProgressTerm -m timed                          # Timed progress bar
ProgressTerm -m colored -C magenta             # Colored progress bar (background magenta)
ProgressTerm -m colored -c blue                # Colored progress bar (foreground blue)
ProgressTerm -s 75                             # The progress bar size is 75 characters
ProgressTerm -p "#"                            # The progress characters of the progress bar
ProgressTerm -e " "                            # Empty characters of the progress bar
ProgressTerm -l "|"                            # Last delimiter of the progress bar
ProgressTerm -f "|"                            # First delimiter of the progress bar
ProgressTerm -i 0.2                            # Step time is 0.2 seconds
ProgressTerm -T "Progress bar"                 # Text (action description)
ProgressTerm -L 10                             # Text max length
ProgressTerm -P "..."                          # Text placeholder
ProgressTerm -t 50                             # Number of steps

ProgressTerm                                   # Basic progress bar
python3 -m PyProgressTerm                      # Basic progress bar
python3 PyProgressTerm.pyz                     # Basic progress bar
```

### Python script

```python
from PyProgressTerm import Progress

progress = Progress()
progress.thread_infinity_run()
```

```python
import PyProgressTerm
import asyncio

progress = PyProgressTerm.Progress()
asyncio.run(progress.async_infinity_run())
```

```python
from PyProgressTerm import Progress
from time import sleep

progress = Progress()

for step in range(256):
    progress.colored_progress_bar(
        step, 
        total=255, 
        first_delimiter="Progress... |", 
        function_name="timed_progress_bar", 
        background="default", 
        foreground="green",
    )
    sleep(0.2)

print()
progress.colored_progress_bar(
    50, 
    function_name="timed_progress_bar", 
    background="green", 
    foreground="default",
)

for step in range(51):
    progress.colored_progress_bar(
        step, 
        total=50, 
        function_name="rotating_progress_bar", 
        background="default", 
        foreground="green",
    )
    sleep(0.2)

progress.thread_infinity_run(function_name="rotating_animation")
```

## Links
 - [Pypi](https://pypi.org/project/PyProgressTerm)
 - [Github](https://github.com/mauricelambert/PyProgressTerm)
 - [Documentation](https://mauricelambert.github.io/info/python/code/PyProgressTerm.html)
 - [Python executable](https://mauricelambert.github.io/info/python/code/PyProgressTerm.pyz)

## Pictures

![Basic progress bar](https://mauricelambert.github.io/info/python/code/ProgressBar.PNG "Basic progress bar")
![Timed progress bar](https://mauricelambert.github.io/info/python/code/ProgressBarTimed.PNG "Timed progress bar")
![Colored progress bar](https://mauricelambert.github.io/info/python/code/ProgressBarColored.PNG "Colored progress bar")

## License
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).