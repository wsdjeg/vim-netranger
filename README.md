vim-netranger
=============
![Screenshot](https://user-images.githubusercontent.com/1246394/33575494-da0dbff4-d90a-11e7-8b26-f839493b48cc.png)

Vim-netranger is a ranger-like system/cloud storage explorer for Vim. It brings together the best of Vim, [ranger](https://github.com/ranger/ranger), and [rclone](https://rclone.org/):

1. Against Vim (netrw):
    - Better rendering
    - Open files with extern programs (see [Rifle](#rifle))
    - Supports various cloud storages (via rclone)
2. Against ranger:
    - No `sudo` required
    - Native Vim key-binding rather than just mimicking Vim
3. Against rclone
    - Display/modify remote content without typing commands in terminal

## Installation
------------

Using vim-plug

```viml
if has('nvim')
  Plug 'ipod825/vim-netranger', { 'do': ':UpdateRemotePlugins' }
endif
```
__Note__: Other explorer plugins (e.g. [NERDTree](https://github.com/scrooloose/nerdtree)) might prohibit `vim-netranger`. You must disable them to make `vim-netranger` work.

## Requirements

vim-netranger requires Neovim. You should install neovim's Python3 api with pip:

```bash
    pip3 install neovim
```

`rclone` is needed if you use the remote editing feature. However, it will be installed automatically on the first time running `NETRListRemotes` command.


## Usage

### Opening a `vim-netranger` buffer
1. vim a directory
2. Inside vim, use edit commands (e.g. `vsplit`, `edit`, `tabedit`) to edit a directory. Just like `netrw`.

### Help
1. Press `?` to see current key bindings

### Navigation
1. Press `l` to change directory/open file for the current directory/file under the cursor.
2. Press `h` to jump to the parent directory.
3. Press `<Space>` to toggle expand current directory under cursor.
4. Press `<Cr>` to set vim's cwd to the directory of the file under cursor. This is very useful if you've expanded a directory and want to open an nvim terminal to run a script in the subdirectory. 

### File Rename
1. Press `i` to enter edit mode. You can freely modify any file/directory name in this mode.
2. Note that in this mode, you can't delete file by deleting lines (you can't add file either).
3. After you are done, back into normal mode (i.e. press `<Esc>` or whatever mapping you prefer), then press `<Esc>` again. All files will be renamed as you've modified.

### File Selection/Copy/Cut/Paste/Deletion
1. Press `v` or `V` to select a file for further processing. You can select multiple files and then do one of the following
    * Press `y` to copy all selected files
    * Press `x` or `d` to cut all selected files
    * Press `D` to delete (`rm -r`) all selected files
    * Press `X` to force delete (i.e. `rm -rf`) all selected files

2. Note that if you leave the directory before pressing any aforementioned keys, your selection will be lost.
3. For `y`, `x`, `d`, go to the target directory, press `p` to paste all cut/copied files/directories.
4. If only one file is to be cut/copy, you can simply press `yy` (copy) or `dd` (cut). The current file will be marked. You can then continue `yy`,  `dd` other lines. I personally think this is more convenient then using `v`.
5. Similarly, if only one file is to be (force) deleted, you can simply press `DD` or `XX`.

### Bookmark
1. Press `m` to open the bookmark UI. You'll see the current bookmarks you have. Press [azAZ] (any letters) to bookmark the current directory.
2. Press `'` to open the bookmark UI again. You'll see that previous entered character appears there. Press the correct character to navigate to the directory you want to go.
3. Press `em` to edit the bookmark with vim. On saving (e.g. `:x`)the file, your bookmarks will be updated automatically.
4. Note that you can use `:q` to quit the bookmark ui to abort the aforementioned operation. 

### Rifle
1. Rifle is a config file ranger used to open files with external program. vim-netranger mimics its syntax and behavior.
2. If you don't have a `rifle.config` file in `g:NETRRootDir` (default to `$HOME/.netranger/`), vim-netranger will copy a default one to that directory. You can simply modify the default `rifle.config` to serve your need.


### Sort
In progress

### Misc
1. Press `zp` to (toggle) pin current directory as the project root, which means you can't use `h` to jump to the parent directory. I think it might be useful when developing a project.
2. Press `zh` to (toggle) show hidden files.

### Remote storage
1. Run `NETRListRemotes` command to open a `vim-netranger` buffer showing all configured remote storage.
2. If `rclone` is not in your `PATH`, on first time running `NETRListRemotes`. It will be automatically downloaded and installed.
3. Remote files are downloaded on demand and cached in `g:NETRRootDir/cache`. Other than that, it's just like browsing local files.
__Note__ Remote reading is done now. Writing is still in progress.

## Customization
### Key mappings:
1. Assign a list to each of the variables to provide extra key mappings. For maintaining issue, please press `?` in a vim-ranger buffer to check variables and their key bindings.
2. Assign a list to `g:NETRDefaultMapSkip` to ignore default mappings. For example, if you want to switch the mappings for `g:NETRBookmarkSet`, `g:NETRBookmarkGo`, you'll put the following in your `.vimrc`:
```vim
let g:NETRDefaultMapSkip = ['m',"'"]
let g:NETRBookmarkSet = ["'"]
let g:NETRBookmarkGo = ["m"]
```

### Variables
| Variable             | Description                                               | Default               |
| :------------        | :--------------                                           | :----------------     |
| g:NETRIgnore         | File patterns (bash wild card) to ignore (not displaying) | []                    |
| g:NETRRootDir        | Directory for storing remote cache and bookmark file      | ['$HOME/.netranger/'] |
| g:NETRTabAutoToFirst | Automatically move new netranger tab to the first tab     | v:false               |
| g:NETROpenInBUffer   | Open files in current buffer instead of a new tab         | v:false               |

