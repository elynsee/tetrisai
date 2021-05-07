# tetrisai
An artificial intelligence (AI) model built to automatically play Tetris!

## Running the code
To run the code, you have to use a recent version of Python 3. This can be downloaded from https://python.org/.

Once you are in the code directory, you can start the interface by running:
```python
python visual.py
```

To get a feeling for the game, you can also run any of the interfaces in manual mode by adding the ag -m:
```python
python visual.py -m
````

If that interface does not work, there are two alternative interfaces available:
1. A command-line interface; run python cmdline.py to use it. If you are using Windows, you may need to
install the windows-curses package rst; try running pip --user install windows-curses.
2. A Pygame-based interface; run python visual-pygame.py to use it. For this, you need to have a working
copy of Pygame; run pip --user install pygame to install it.

If you get an interface running, you should see the default player in action.
