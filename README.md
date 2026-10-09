# pyfx

**Terminal visual effects for Python.** Create animated fire, Matrix rain, stars, rainfall, confetti and particle explosions with one function call. Includes a tiny ASCII drawing canvas.

## Quick start

``` python
import pyfx

pyfx.fire()
pyfx.matrix()
pyfx.stars()
pyfx.rain()
pyfx.confetti()
pyfx.explosion()
```
Press Ctrl+C to stop looping effects. Effects use ANSI terminal colours when stdout is an interactive terminal and the ```NO_COLOR``` environment variable is not set.

## Control the animation
``` python 
import pyfx

pyfx.matrix(fps=30, density=0.07)
pyfx.stars(count=180, fps=24)
pyfx.fire(intensity=0.8, frames=200)
pyfx.explosion(frames=30)
```
```frames=None``` means loop until interrupted. ```frames=100``` renders 100 frames and exits.

## Choose an effect by name

``` python 
import pyfx

pyfx.run("confetti", count=150)
```
Available names: ```fire```, ```matrix```, ```stars```, ```rain```, ```confetti```, ```explosion```.

## Draw your own ASCII art

``` python
from pyfx import Canvas

screen = Canvas(40, 12)
screen.rectangle(1, 1, 38, 10)
screen.text(4, 3, "Hello from pyfx!")
screen.line(3, 7, 35, 7, "=")
screen.show()
```
Canvas methods can be chained. Coordinates start at the top-left corner.

## Examples

``` bash 
python examples/drawing.py
```
## Notes
- Best experienced in a modern terminal with ANSI escape support.
- The terminal is cleared while an animation runs.
- This first version uses text-based rendering, so no external dependencies are required.