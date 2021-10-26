# Writing Alfred copy/paste scripts in Python

This repository shows how to create [Alfred](https://www.alfredapp.com) scripts in Python. The examples below assume that you have Python 3 installed via Homebrew.

Our working example will be a script that will convert text in the Mac clipboard to small caps, that is, for example, it will take "Hello World!" and replace it with "ʜᴇʟʟᴏ ᴡᴏʀʟᴅ!"

## Set up

1. Create a directory in which you want to place your Python-based Alfred scripts. I created mine in `$HOME/projects/alfred-scripts`

## Writing and testing a script locally

First you need to decide what your text transformation will do. Let's start with something simple: converting text to upper case:

```python
def convert(text):
    return text.upper()
```

By my own convention, I write this scripts to run in three ways: in test mode, from the command line, and in clipboard mode (which is what we will use for Alfred). So I have a driver that looks like this:

```python
if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv.pop(1)
        if action == "--test":
            unittest.main()
        elif action == "--clipboard":
            clipboard_main()
        else:
            print("Unknown action: {}".format(action))
        sys.exit(1)
    else:
        main()
```

You can use your own conventions, but this allow me to test the script out from the command line.

The main function is easy enough:

```python
def main():
    sys.stdout.write(convert(sys.stdin.read()))
```

You can embed unit tests in the script and invoke them using the `--test` flag as given above:

```python
import unittest

class TestConvert(unittest.TestCase):
    def test_convert(self):
        text = "Hello World!"
        match = "HELLO WORLD!"
        self.assertEqual(convert(text), match)
```

Once you are satisfied that your conversion routine is working, you can write the simple clipboard main:

```python
def clipboard_main():
    to_convert = clipboard.paste()
    clipboard.copy(convert(to_convert.lower()))
```

(Note that you are _pasting_ into your program, and _copying_ back into the clipboard).

## Creating a Alfred Workflow

Creating the Alfred workflow is relatively simple. Create a new worklfow and name it. Typically, it will have four steps:

1. A trigger command
2. Executing ⌘C to copy text into the clipboard
3. Running your script
4. Executing ⌘V to paste text

The script should look like this (I use [zsh](https://www.zsh.org), your script might vary). Note that
we install the `clipboard` package; if there are other packages you need, you'll want to do the same thing.

```zsh
export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
export SCRIPTDIR=$HOME/projects/alfred-scripts
export PYTHONPATH=$SCRIPTDIR/dist
python3 -m pip install --target $PYTHONPATH clipboard --exists-action a
python3 $SCRIPTDIR/upper.py --clipboard

```

This is what the workflow looks like:

<img width="839" alt="Workflow" src="https://user-images.githubusercontent.com/37049/138725865-26e7b952-7b64-45c1-a849-ac84d7326223.png">

I find myself often needing to debug the Alfred script, so it's useful to learn [how to use the debugger](https://www.alfredapp.com/help/workflows/advanced/debugger/).

Note: many thanks to [@deanishe](https://github.com/deanishe) for improvements to what I'm doing. Any
foolishness remaining I claim for my own. See also his [https://github.com/deanishe/alfred-workflow](alfred-workflow) package.
