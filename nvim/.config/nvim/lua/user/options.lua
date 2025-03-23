-- [[ Setting options ]]
-- See `:help vim.o`
-- NOTE: You can change these options as you wish!

-- Set highlight on search
vim.o.hlsearch = false

-- Make line numbers default
vim.o.number = false

-- Enable mouse mode
vim.o.mouse = 'a'

-- Sync clipboard between OS and Neovim.
--  Remove this option if you want your OS clipboard to remain independent.
--  See `:help 'clipboard'`
vim.o.clipboard = 'unnamedplus'

-- Enable break indent
vim.o.breakindent = true

-- Save undo history
vim.o.undofile = true

-- Case-insensitive searching UNLESS \C or capital in search
vim.o.ignorecase = true
vim.o.smartcase = true

-- Make ident smart again
-- vim.o.smartindent = true

-- Show tabline
-- vim.o.showtabline = 2

-- Keep signcolumn on by default
vim.wo.signcolumn = 'yes'

-- Decrease update time
vim.o.updatetime = 250
vim.o.timeoutlen = 300

-- Set completeopt to have a better completion experience
vim.o.completeopt = 'menuone,noselect'

-- NOTE: You should make sure your terminal supports this
vim.o.termguicolors = true

--relative line numbers
vim.o.relativenumber = true

--Leave so space when scrolling
vim.o.scrolloff = 8

--Expand tabs to spaces
vim.o.expandtab = true
--
--Enable line wraping
-- vim.o.wrap = true
-- vim.o.textwidth = 80


--Set the number of spaces for a tabs
vim.o.tabstop = 2
vim.o.shiftwidth = 2

vim.o.foldmethod = "expr"
vim.o.foldexpr = "nvim_treesitter#foldexpr()"

--Set the default shell for the terminal
vim.o.shell = 'zsh'

vim.g.terminal_emulator = "zsh"
-- Options for float term
--vim.go.floaterm_shell = "/bin/zsh"
--vim.cmd([[ let g:floaterm_shell = "zsh" ]])




