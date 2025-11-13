#   textgrid_explorer - A TextGrid editing tool with a spreadsheet interface
#   Copyright (C) 2025 Rolando Muñoz <rolando.muar@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License version 3, as published
#   by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranties of
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
form: "Open file"
    infile: "Textgrid path", ""
    infile: "Sound path", ""
    boolean: "Maximize audibility", "1"
    integer: "Tier position", "0"
    real: "Start selection", "0.0"
    real: "End selection", "0.1"
endform

tg = Read from file: textgrid_path$
objects# = {tg}
if fileReadable(sound_path$)
    if maximize_audibility == 1
        sd = Read from file: sound_path$
        Scale peak: 0.99
    else
        sd = Open long sound file: sound_path$
    endif
    objects# = {tg, sd}
endif

selectObject: objects#
View & Edit

editor: tg
# Select tier position
for i to tier_position - 1
    Select next tier
endfor
Zoom: start_selection-0.1, end_selection+0.1
Select: start_selection, end_selection

beginPause: "TextGrid Explorer"
clicked = endPause: "Save", "Quit", 2, 2

if clicked == 1
    Save whole TextGrid as text file: textgrid_path$
endif

endeditor
Quit
