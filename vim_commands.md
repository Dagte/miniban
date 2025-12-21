# Basic Vim Commands

## Starting and Exiting Vim
- `vim filename`: Open a file in Vim.
- `:q`: Quit Vim.
- `:q!`: Quit Vim without saving changes.
- `:w`: Save the file.
- `:wq` or `:x`: Save and quit.
- `ZZ`: Save and quit (shortcut).

## Navigation
- `h`, `j`, `k`, `l`: Move left, down, up, and right respectively.
- `gg`: Go to the beginning of the file.
- `G`: Go to the end of the file.
- `:num`: Go to line number `num`.
- `w`: Move to the beginning of the next word.
- `b`: Move to the beginning of the previous word.
- `e`: Move to the end of the current word.

## Editing
- `i`: Enter insert mode at the cursor.
- `a`: Enter insert mode after the cursor.
- `I`: Enter insert mode at the beginning of the line.
- `A`: Enter insert mode at the end of the line.
- `o`: Insert a new line below the current line and enter insert mode.
- `O`: Insert a new line above the current line and enter insert mode.
- `x`: Delete the character under the cursor.
- `dd`: Delete the current line.
- `yy`: Yank (copy) the current line.
- `p`: Paste the yanked text after the cursor.
- `P`: Paste the yanked text before the cursor.

