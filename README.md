# uhk-learn-layout
Tool to enable an UltimateHackingKeyboard (uhk) to learn the keyboard layout of the host system

## Command options

```
C:\dev\uhk-learn-layout>python uhk-learn-layout.py --help
usage: uhk-learn-layout.py [-h] [--debug] [--generate-macro] [--use-altgr] [--macrodelay] [--print-canonical]
                           [--canonical] [--showmap] [--compact] [--input INPUTFILE]

determine the host layout from the output of the "learn_layout" macro run on a UHK

options:
  -h, --help         show this help message and exit
  --debug            show debugging information for developers
  --generate-macro   generate learn_hostmap macro for UHK Agent. Paste the generated macro code into a macro command,
                     and bind it to a key. Execute the macro (by tapping the key), and feed the output into this
                     script to learn the host keymap.
  --use-altgr        use AltGr combinations in macro (in addition to standard keypress and shift-keypress)
  --macrodelay       insert delays into the macro (so it runs a bit slower)
  --print-canonical  print the canoncial string(s) for this keymap
  --canonical        show the canonical name for this keymap
  --showmap          show the keyboard layout
  --compact          show a compact version of the keyboard layout
  --fourlevels       show up to four levels for each key (base, shift, altgr, shift-altgr)
  --input INPUTFILE  read input from this file
```

## Brief instructions

First, generate a macro that you will need to copy/paste into Agent. 
Use --generate-macro to create the macro command. The plain version will test all keys in unshifted
and shifted state. You can also add the --use-altgr or --fourlevels options, and the generated macro 
will test all keys in unshifted, shifted, AltGr, and AltGr+Shift state.

```
C:\dev\uhk-learn-layout>python uhk-learn-layout.py --generate-macro --use-altgr > macro.txt
```

Now paste the generated text into a macro command, and bind that macro to a key on a mod, mouse or fn layer (for example, `Fn-=`).

To learn your host keymap, run the tool and then type your key (`Fn-=`). The macro will produce quite a bit of output,
and the tool will build an internal representation of the UHK keys and what characters they generate on the host.
The result will be displayed as a keymap, and if the keymap is known (i.e. its _canonical_ representation has been
added to the tool), it will also show a _canonical keymap name_ (e.g. "UK-International").

```
C:\dev\uhk-learn-layout>python uhk-learn-layout.py --canonical --showmap --compact
... (hit your macro key, see lots of output here) ...
Canonical keymap name: US-Colemak-International
R1:  [ `~~ ]  [ 1!¡ ]  [ 2@º ]  [ 3#ª ]  [ 4$¢ ]  [ 5%€ ]  [ 6^ħ ]  [ 7&ð ]  [ 8*þ ]  [ 9(‘ ]  [ 0)’ ]  [ -_– ]  [ =+× ]
R2:           [ qQä ]  [ wWå ]  [ fFã ]  [ pPø ]  [ gG˛ ]  [ jJđ ]  [ lLł ]  [ uUú ]  [ yYü ]  [ ;:ö ]  [ [{« ]  [ ]}» ]  [ \|* ]
R3:           [ aAá ]  [ rR` ]  [ sSß ]  [ tT´ ]  [ dD¨ ]  [ hHˇ ]  [ nNñ ]  [ eEé ]  [ iIí ]  [ oOó ]  [ '"õ ]
R4:  [ -_– ]  [ zZæ ]  [ xX^ ]  [ cCç ]  [ vVœ ]  [ bB˘ ]  [ kK˚ ]  [ mM¯ ]  [ ,<¸ ]  [ .>˙ ]  [ /?¿ ]
```

If you want to add new known keymaps, you can display their _canonical_ representation using the `--print-canonical` option, then copy/paste it
as a new entry into the `canonicalstrings` dictionary in the python code.

