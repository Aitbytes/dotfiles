set background=dark
if exists('g:colors_name')
hi clear
if exists('syntax_on')
syntax reset
endif
endif
let g:colors_name = 'lushwal'
highlight Normal guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight! link User Normal
highlight Bold guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=bold
highlight Boolean guifg=#797F76 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Character guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight ColorColumn guifg=#7EB6C8 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Comment guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight Conceal guifg=#749BAA guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight! link Whitespace Conceal
highlight Conditional guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Constant guifg=#797F76 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Cursor guifg=#161408 guibg=#AAE1F3 guisp=NONE blend=NONE gui=NONE
highlight CursorColumn guifg=#7EB6C8 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight CursorLine guifg=#749BAA guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight CursorLineNr guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Debug guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Define guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Delimiter guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticError guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticHint guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticInfo guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticUnderlineError guifg=#DF9320 guibg=NONE guisp=#DF9320 blend=NONE gui=underline
highlight DiagnosticUnderlineHint guifg=#55AAE7 guibg=NONE guisp=#55AAE7 blend=NONE gui=underline
highlight DiagnosticUnderlineInfo guifg=#3FB7DE guibg=NONE guisp=#3FB7DE blend=NONE gui=underline
highlight DiagnosticUnderlineWarn guifg=#2070C5 guibg=NONE guisp=#2070C5 blend=NONE gui=underline
highlight DiagnosticWarn guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiffAdd guifg=#C99C4F guibg=#749BAA guisp=NONE blend=NONE gui=bold
highlight! link DiffAdded DiffAdd
highlight DiffChange guifg=#8ECCE1 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight DiffDelete guifg=#DF9320 guibg=#749BAA guisp=NONE blend=NONE gui=bold
highlight! link DiffRemoved DiffDelete
highlight! link diffRemoved DiffDelete
highlight DiffFile guifg=#DF9320 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight DiffLine guifg=#3FB7DE guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight DiffNewFile guifg=#C99C4F guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight DiffText guifg=#3FB7DE guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight Directory guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight EndOfBuffer guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Error guifg=#DF9320 guibg=#AAE1F3 guisp=NONE blend=NONE gui=NONE
highlight ErrorMsg guifg=#DF9320 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Exception guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Float guifg=#797F76 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight FoldColumn guifg=#3FB7DE guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Folded guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=italic
highlight Function guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Identifier guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight IncSearch guifg=#749BAA guibg=#797F76 guisp=NONE blend=NONE gui=NONE
highlight Include guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Italic guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=italic
highlight Keyword guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Label guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight LineNr guifg=#8ECCE1 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Macro guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MatchParen guifg=#AAE1F3 guibg=#8ECCE1 guisp=NONE blend=NONE gui=NONE
highlight MiniCompletionActiveParameter guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniCursorword guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=underline
highlight! link MiniCursorwordCurrent MiniCursorword
highlight MiniIndentscopePrefix guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=nocombine
highlight MiniIndentscopeSymbol guifg=#749BAA guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight MiniJump guifg=#3FB7DE guibg=NONE guisp=#8ECCE1 blend=NONE gui=underline
highlight MiniJump2dSpot guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=undercurl
highlight MiniStarterCurrent guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterFooter guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniStarterHeader guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniStarterInactive guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight MiniStarterItem guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight MiniStarterItemBullet guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterItemPrefix guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterQuery guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterSection guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineDevinfo guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineFileinfo guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineFilename guifg=#2070C5 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineInactive guifg=#7EB6C8 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeCommand guifg=#161408 guibg=#55AAE7 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeInsert guifg=#161408 guibg=#3FB7DE guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeNormal guifg=#161408 guibg=#C99C4F guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeOther guifg=#161408 guibg=#B396ED guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeReplace guifg=#161408 guibg=#DF9320 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeVisual guifg=#161408 guibg=#797F76 guisp=NONE blend=NONE gui=NONE
highlight MiniSurround guifg=#749BAA guibg=#797F76 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineCurrent guifg=#8ECCE1 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTablineFill guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniTablineHidden guifg=#C99C4F guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedCurrent guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedHidden guifg=#7EB6C8 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedVisible guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTablineVisible guifg=#8ECCE1 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight MiniTestEmphasis guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTestFail guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTestPass guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTrailspace guifg=#DF9320 guibg=#AAE1F3 guisp=NONE blend=NONE gui=NONE
highlight ModeMsg guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MoreMsg guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight NonText guifg=#8ECCE1 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Number guifg=#797F76 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Operator guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PMenu guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight PMenuSel guifg=#AAE1F3 guibg=#3FB7DE guisp=NONE blend=NONE gui=NONE
highlight PmenuSbar guifg=#7EB6C8 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PmenuThumb guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PreProc guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Question guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Repeat guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Search guifg=#8ECCE1 guibg=#2070C5 guisp=NONE blend=NONE gui=NONE
highlight! link MiniTablineTabpagesection Search
highlight SignColumn guifg=#7EB6C8 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight Special guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpecialChar guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpecialKey guifg=#8ECCE1 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpellBad guifg=#DF9320 guibg=NONE guisp=#DF9320 blend=NONE gui=underline
highlight SpellCap guifg=#2070C5 guibg=NONE guisp=#2070C5 blend=NONE gui=underline
highlight SpellLocal guifg=#55AAE7 guibg=NONE guisp=#55AAE7 blend=NONE gui=underline
highlight SpellRare guifg=#B396ED guibg=NONE guisp=#B396ED blend=NONE gui=underline
highlight Statement guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight StatusLine guifg=#AAE1F3 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight StatusLineNC guifg=#7EB6C8 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight StatusLineTerm guifg=#C99C4F guibg=#C99C4F guisp=NONE blend=NONE gui=NONE
highlight StatusLineTermNC guifg=#2070C5 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight StorageClass guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight String guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Structure guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight TabLine guifg=#8ECCE1 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight TabLineFill guifg=#8ECCE1 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight TabLineSel guifg=#C99C4F guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight Tag guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Title guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight Todo guifg=#2070C5 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight TooLong guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Type guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Typedef guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Underlined guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight VertSplit guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight! link WinSeparator VertSplit
highlight Visual guifg=#161408 guibg=#7EB6C8 guisp=NONE blend=NONE gui=NONE
highlight VisualNOS guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight WarningMsg guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight WildMenu guifg=#AAE1F3 guibg=#3FB7DE guisp=NONE blend=NONE gui=NONE
highlight WinBar guifg=#AAE1F3 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight WinBarNC guifg=#7EB6C8 guibg=#161408 guisp=NONE blend=NONE gui=NONE
highlight gitCommitOverflow guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight gitCommitSummary guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight helpCommand guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight helpExample guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @attribute guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @boolean guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @character guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @character.special guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @comment guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight @conditional guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant.builtin guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant.macro guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constructor guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @debug guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @define guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @exception guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @field guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @float guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function.builtin guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function.macro guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @include guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword.function guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword.operator guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @label guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @method guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @namespace guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @none guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @number guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @operator guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @parameter guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @preproc guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @property guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.bracket guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.delimiter guifg=#AAE1F3 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.special guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @repeat guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @storageclass guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.escape guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.regex guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.special guifg=#C29542 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @symbol guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag.attribute guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag.delimiter guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.bold guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @text.danger guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.diff.add guifg=#C99C4F guibg=#749BAA guisp=NONE blend=NONE gui=bold
highlight @text.diff.delete guifg=#DF9320 guibg=#749BAA guisp=NONE blend=NONE gui=bold
highlight @text.emphasis guifg=#B396ED guibg=NONE guisp=NONE blend=NONE gui=italic
highlight @text.environment guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.environment.name guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.literal guifg=#C99C4F guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.math guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.note guifg=#55AAE7 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.reference guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.strike guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=strikethrough
highlight @text.title guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @text.todo guifg=#2070C5 guibg=#749BAA guisp=NONE blend=NONE gui=NONE
highlight @text.underline guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=underline
highlight @text.uri guifg=NONE guibg=#749BAA guisp=NONE blend=NONE gui=underline
highlight @type guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @type.builtin guifg=#3FB7DE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @type.definition guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @variable guifg=#2070C5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @variable.builtin guifg=#DF9320 guibg=NONE guisp=NONE blend=NONE gui=NONE