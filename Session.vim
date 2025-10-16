let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
let Db_ui_buffer_name_generator =  0 
let Db_ui_table_name_sorter =  0 
silent only
silent tabonly
cd ~/jonathan/projects/wine_wiki/wine_wiki_site
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +2 ~/jonathan/personal/dailies/2025-10-08.md
badd +1 wine_wiki/table_match_autofill/wld_selfjoin.sql
badd +905 ~/jonathan/projects/wine_wiki/wine_wiki_log/log.md
badd +1 ~/jonathan/projects/wine_wiki/.python-version_hidden_message
badd +402 ~/jonathan/projects/wine_wiki/wine_data_mining/notes/devlog.md
badd +1 ~/jonathan/projects/wine_wiki/wine_data_mining/orc_airflow/logs/dbt.log
badd +1 ~/jonathan/projects/wine_wiki/README.md
badd +1 wine_wiki/README.rst
badd +0 /private/var/folders/mh/cknmc22s2zv5m4l777wwz1b00000gn/T/nvim.jonathan/bCcSI8/wine_wiki_site-query-2025-10-14-23-31-53
badd +321 wine_wiki/models.py
badd +340 wine_wiki/views.py
badd +1 wine_wiki/templates/wine_wiki/bennelong_wine_list.html
badd +48 wine_wiki/urls.py
badd +3 bennelong_wine_list.pdf
badd +40 wine_wiki/table_match_autofill/autofill.py
badd +65 wine_wiki/table_match_autofill/views.py
badd +13 wine_wiki/templates/table_match_autofill/autofill_review.html
badd +28 wine_wiki/table_match_autofill/models.py
badd +2 wine_wiki/templates/wine_wiki/add_wine.html
badd +0 wine_wiki/templates/fuzzy_match/fuzzy_match_list_wiki_results.html
badd +2 wine_wiki/fuzzy_match_wiki/views.py
badd +1 wine_wiki/fuzzy_match_wiki/models.py
argglobal
%argdel
$argadd .
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit wine_wiki/table_match_autofill/models.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
wincmd =
tcd ~/jonathan/projects/wine_wiki/wine_wiki_site
argglobal
balt ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/fuzzy_match_wiki/models.py
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
8
sil! normal! zo
17
sil! normal! zo
32
sil! normal! zo
let s:l = 1 - ((0 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 029|
wincmd w
argglobal
if bufexists(fnamemodify("~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/views.py", ":p")) | buffer ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/views.py | else | edit ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/views.py | endif
if &buftype ==# 'terminal'
  silent file ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/views.py
endif
balt ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/autofill.py
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
12
sil! normal! zo
17
sil! normal! zo
31
sil! normal! zo
39
sil! normal! zo
49
sil! normal! zc
64
sil! normal! zo
69
sil! normal! zo
let s:l = 51 - ((6 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 51
normal! 02|
wincmd w
wincmd =
tabnext
edit ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/wld_selfjoin.sql
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
wincmd =
tcd ~/jonathan/projects/wine_wiki/wine_wiki_site
argglobal
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 2 - ((1 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 2
normal! 06|
wincmd w
argglobal
if bufexists(fnamemodify("~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/wld_selfjoin.sql", ":p")) | buffer ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/wld_selfjoin.sql | else | edit ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/wld_selfjoin.sql | endif
if &buftype ==# 'terminal'
  silent file ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/table_match_autofill/wld_selfjoin.sql
endif
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 107 - ((36 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 107
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("/private/var/folders/mh/cknmc22s2zv5m4l777wwz1b00000gn/T/nvim.jonathan/bCcSI8/161.dbout", ":p")) | buffer /private/var/folders/mh/cknmc22s2zv5m4l777wwz1b00000gn/T/nvim.jonathan/bCcSI8/161.dbout | else | edit /private/var/folders/mh/cknmc22s2zv5m4l777wwz1b00000gn/T/nvim.jonathan/bCcSI8/161.dbout | endif
if &buftype ==# 'terminal'
  silent file /private/var/folders/mh/cknmc22s2zv5m4l777wwz1b00000gn/T/nvim.jonathan/bCcSI8/161.dbout
endif
setlocal foldmethod=expr
setlocal foldexpr=db_ui#dbout#foldexpr(v:lnum)
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 1 - ((0 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
wincmd =
tabnext
edit ~/jonathan/projects/wine_wiki/wine_wiki_log/log.md
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt ~/jonathan/projects/wine_wiki/wine_wiki_site/wine_wiki/README.rst
setlocal foldmethod=expr
setlocal foldexpr=v:lua.LazyVim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
1
sil! normal! zo
855
sil! normal! zo
let s:l = 905 - ((30 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 905
normal! 071|
tabnext
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
