set background=dark
if exists('g:colors_name')
hi clear
if exists('syntax_on')
syntax reset
endif
endif
let g:colors_name = 'lushwal'
highlight Normal guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight! link User Normal
highlight Bold guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=bold
highlight Boolean guifg=#AF5A5D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Character guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight ColorColumn guifg=#A4799D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Comment guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight Conceal guifg=#8D6D88 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight! link Whitespace Conceal
highlight Conditional guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Constant guifg=#AF5A5D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Cursor guifg=#080613 guibg=#CD9DC5 guisp=NONE blend=NONE gui=NONE
highlight CursorColumn guifg=#A4799D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight CursorLine guifg=#8D6D88 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight CursorLineNr guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Debug guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Define guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Delimiter guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticError guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticHint guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticInfo guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiagnosticUnderlineError guifg=#EBAA60 guibg=NONE guisp=#EBAA60 blend=NONE gui=underline
highlight DiagnosticUnderlineHint guifg=#67549C guibg=NONE guisp=#67549C blend=NONE gui=underline
highlight DiagnosticUnderlineInfo guifg=#36448C guibg=NONE guisp=#36448C blend=NONE gui=underline
highlight DiagnosticUnderlineWarn guifg=#67368C guibg=NONE guisp=#67368C blend=NONE gui=underline
highlight DiagnosticWarn guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight DiffAdd guifg=#2E3E85 guibg=#8D6D88 guisp=NONE blend=NONE gui=bold
highlight! link DiffAdded DiffAdd
highlight DiffChange guifg=#B889B0 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight DiffDelete guifg=#EBAA60 guibg=#8D6D88 guisp=NONE blend=NONE gui=bold
highlight! link DiffRemoved DiffDelete
highlight! link diffRemoved DiffDelete
highlight DiffFile guifg=#EBAA60 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight DiffLine guifg=#36448C guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight DiffNewFile guifg=#2E3E85 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight DiffText guifg=#36448C guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight Directory guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight EndOfBuffer guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Error guifg=#EBAA60 guibg=#CD9DC5 guisp=NONE blend=NONE gui=NONE
highlight ErrorMsg guifg=#EBAA60 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Exception guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Float guifg=#AF5A5D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight FoldColumn guifg=#36448C guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Folded guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=italic
highlight Function guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Identifier guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight IncSearch guifg=#8D6D88 guibg=#AF5A5D guisp=NONE blend=NONE gui=NONE
highlight Include guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Italic guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=italic
highlight Keyword guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Label guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight LineNr guifg=#B889B0 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Macro guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MatchParen guifg=#CD9DC5 guibg=#B889B0 guisp=NONE blend=NONE gui=NONE
highlight MiniCompletionActiveParameter guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniCursorword guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=underline
highlight! link MiniCursorwordCurrent MiniCursorword
highlight MiniIndentscopePrefix guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=nocombine
highlight MiniIndentscopeSymbol guifg=#8D6D88 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight MiniJump guifg=#36448C guibg=NONE guisp=#B889B0 blend=NONE gui=underline
highlight MiniJump2dSpot guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=undercurl
highlight MiniStarterCurrent guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterFooter guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniStarterHeader guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniStarterInactive guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight MiniStarterItem guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight MiniStarterItemBullet guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterItemPrefix guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterQuery guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStarterSection guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineDevinfo guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineFileinfo guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineFilename guifg=#67368C guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineInactive guifg=#A4799D guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeCommand guifg=#080613 guibg=#67549C guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeInsert guifg=#080613 guibg=#36448C guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeNormal guifg=#080613 guibg=#2E3E85 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeOther guifg=#080613 guibg=#C882CE guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeReplace guifg=#080613 guibg=#EBAA60 guisp=NONE blend=NONE gui=NONE
highlight MiniStatuslineModeVisual guifg=#080613 guibg=#AF5A5D guisp=NONE blend=NONE gui=NONE
highlight MiniSurround guifg=#8D6D88 guibg=#AF5A5D guisp=NONE blend=NONE gui=NONE
highlight MiniTablineCurrent guifg=#B889B0 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineFill guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MiniTablineHidden guifg=#2E3E85 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedCurrent guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedHidden guifg=#A4799D guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineModifiedVisible guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTablineVisible guifg=#B889B0 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight MiniTestEmphasis guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTestFail guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTestPass guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=bold
highlight MiniTrailspace guifg=#EBAA60 guibg=#CD9DC5 guisp=NONE blend=NONE gui=NONE
highlight ModeMsg guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight MoreMsg guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight NonText guifg=#B889B0 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Number guifg=#AF5A5D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Operator guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PMenu guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight PMenuSel guifg=#CD9DC5 guibg=#36448C guisp=NONE blend=NONE gui=NONE
highlight PmenuSbar guifg=#A4799D guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PmenuThumb guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight PreProc guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Question guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Repeat guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Search guifg=#B889B0 guibg=#67368C guisp=NONE blend=NONE gui=NONE
highlight! link MiniTablineTabpagesection Search
highlight SignColumn guifg=#A4799D guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight Special guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpecialChar guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpecialKey guifg=#B889B0 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight SpellBad guifg=#EBAA60 guibg=NONE guisp=#EBAA60 blend=NONE gui=underline
highlight SpellCap guifg=#67368C guibg=NONE guisp=#67368C blend=NONE gui=underline
highlight SpellLocal guifg=#67549C guibg=NONE guisp=#67549C blend=NONE gui=underline
highlight SpellRare guifg=#C882CE guibg=NONE guisp=#C882CE blend=NONE gui=underline
highlight Statement guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight StatusLine guifg=#CD9DC5 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight StatusLineNC guifg=#A4799D guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight StatusLineTerm guifg=#2E3E85 guibg=#2E3E85 guisp=NONE blend=NONE gui=NONE
highlight StatusLineTermNC guifg=#67368C guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight StorageClass guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight String guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Structure guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight TabLine guifg=#B889B0 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight TabLineFill guifg=#B889B0 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight TabLineSel guifg=#2E3E85 guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight Tag guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Title guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight Todo guifg=#67368C guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight TooLong guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Type guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Typedef guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight Underlined guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight VertSplit guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight! link WinSeparator VertSplit
highlight Visual guifg=#080613 guibg=#A4799D guisp=NONE blend=NONE gui=NONE
highlight VisualNOS guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight WarningMsg guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight WildMenu guifg=#CD9DC5 guibg=#36448C guisp=NONE blend=NONE gui=NONE
highlight WinBar guifg=#CD9DC5 guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight WinBarNC guifg=#A4799D guibg=#080613 guisp=NONE blend=NONE gui=NONE
highlight gitCommitOverflow guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight gitCommitSummary guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight helpCommand guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight helpExample guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @attribute guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @boolean guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @character guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @character.special guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @comment guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=italic
highlight @conditional guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant.builtin guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constant.macro guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @constructor guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @debug guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @define guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @exception guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @field guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @float guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function.builtin guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @function.macro guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @include guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword.function guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @keyword.operator guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @label guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @method guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @namespace guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @none guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @number guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @operator guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @parameter guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @preproc guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @property guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.bracket guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.delimiter guifg=#CD9DC5 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @punctuation.special guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @repeat guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @storageclass guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.escape guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.regex guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @string.special guifg=#DA9E62 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @symbol guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag.attribute guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @tag.delimiter guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.bold guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @text.danger guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.diff.add guifg=#2E3E85 guibg=#8D6D88 guisp=NONE blend=NONE gui=bold
highlight @text.diff.delete guifg=#EBAA60 guibg=#8D6D88 guisp=NONE blend=NONE gui=bold
highlight @text.emphasis guifg=#C882CE guibg=NONE guisp=NONE blend=NONE gui=italic
highlight @text.environment guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.environment.name guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.literal guifg=#2E3E85 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.math guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.note guifg=#67549C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.reference guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @text.strike guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=strikethrough
highlight @text.title guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=bold
highlight @text.todo guifg=#67368C guibg=#8D6D88 guisp=NONE blend=NONE gui=NONE
highlight @text.underline guifg=NONE guibg=NONE guisp=NONE blend=NONE gui=underline
highlight @text.uri guifg=NONE guibg=#8D6D88 guisp=NONE blend=NONE gui=underline
highlight @type guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @type.builtin guifg=#36448C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @type.definition guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @variable guifg=#67368C guibg=NONE guisp=NONE blend=NONE gui=NONE
highlight @variable.builtin guifg=#EBAA60 guibg=NONE guisp=NONE blend=NONE gui=NONE
