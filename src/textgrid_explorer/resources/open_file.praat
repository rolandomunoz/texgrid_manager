form: "Open file"
    infile: "Textgrid path", ""
    infile: "Sound path", ""
    real: "Start_selection", "0.0"
    real: "End_selection", "0.1"
endform

tg = Read from file: textgrid_path$
objects# = {tg}
if fileReadable(sound_path$)
    sd = Read from file: sound_path$
    Scale peak: 0.99
    objects# = {tg, sd}
endif

selectObject: objects#
View & Edit

editor: tg
Zoom: start_selection-0.1, end_selection+0.1
Select: start_selection, end_selection


beginPause: "TGManager"
clicked = endPause: "Save", "Quit", 2, 2

if clicked == 1
    Save whole TextGrid as text file: textgrid_path$
endif

endeditor
Quit