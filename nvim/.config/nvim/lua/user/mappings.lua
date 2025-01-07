-- [[ Basic Keymaps ]]

-- Keymaps for better default experience
-- See `:help vim.keymap.set()`
vim.keymap.set({ 'n', 'v' }, '<Space>', '<Nop>', { silent = true })

-- Remap for dealing with word wrap
vim.keymap.set('n', 'k', "v:count == 0 ? 'gk' : 'k'", { expr = true, silent = true })
vim.keymap.set('n', 'j', "v:count == 0 ? 'gj' : 'j'", { expr = true, silent = true })

--Remap moving between windows
vim.api.nvim_set_keymap('n', '<C-k>', "<C-w>k", {  silent = true })
vim.api.nvim_set_keymap('n', '<C-l>', "<C-w>l", {  silent = true })
vim.api.nvim_set_keymap('n', '<C-j>', "<C-w>j", {  silent = true })
vim.api.nvim_set_keymap('n', '<C-h>', "<C-w>h", {  silent = true })

--Neo tree mappings
vim.keymap.set('n', '<Space>ee', ":Neotree toggle<CR>", { silent = true, desc = "toogle Neo-tree"})
vim.keymap.set('n', '<Space>eb', ":Neotree toggle show buffers right<CR>", { silent = true, desc = "Toggle Neo-tree buffers"})
vim.keymap.set('n', '<Space>es', ":Neotree toggle float git-status", { silent = true, desc = "Toggle Neo-tree git"})
vim.keymap.set('n', '<Space>eE', ":Neotree position=current<CR>", { silent = true, desc = "Toggle Neo-tree netrw style"})

--Split screen with terminal at the right
vim.keymap.set({"n", "v"}, "<leader>et",":vsplit<CR><C-w>l:terminal<CR>a" , {silent = true, desc="Split screen with terminal at the right "})
vim.keymap.set({"n", "v"}, "<leader>eg",":LazyGit<CR>" , {silent = true, desc="Open Lazygit"})


-- Navigate buffers
vim.keymap.set("n", "<S-l>", ":bnext<CR>", {silent = true, desc=" "})
vim.keymap.set("n", "<S-h>", ":bprevious<CR>", {silent = true, desc=" "})

-- Insert --
-- Press jk fast to enter
vim.keymap.set("i", "jk", "<ESC>", {silent = true, desc="jk to exit insert mode "})

-- Visual --

-- Move text up and down
vim.keymap.set("v", "<A-j>", ":m .+1<CR>==", {silent = true, desc="Move down "})
vim.keymap.set("v", "<A-k>", ":m .-2<CR>==", {silent = true, desc=" "})

-- Visual Block --
-- Move text up and down
vim.keymap.set("x", "J", ":move '>+1<CR>gv-gv", {silent = true, desc="mystery "})
vim.keymap.set("x", "K", ":move '<-2<CR>gv-gv", {silent = true, desc="mystery "})
vim.keymap.set("x", "<A-j>", ":move '>+1<CR>gv-gv", {silent = true, desc="Move down "})
vim.keymap.set("x", "<A-k>", ":move '<-2<CR>gv-gv", {silent = true, desc="Move up"})
-- Terminal --
-- Better terminal navigation
vim.keymap.set("t", "<C-h>", "<C-\\><C-N><C-w>h", {silent = true, desc="Go left "})
vim.keymap.set("t", "<C-j>", "<C-\\><C-N><C-w>j", {silent = true, desc="Go down "})
vim.keymap.set("t", "<C-k>", "<C-\\><C-N><C-w>k", {silent = true, desc="Go up"})
vim.keymap.set("t", "<C-l>", "<C-\\><C-N><C-w>l", {silent = true, desc="Go right "})

-- Set theme from wall
vim.keymap.set({"n", "v"}, "<leader><C-w>", ":colorscheme pywal<CR>", {silent = true, desc="Get the colortheme from lushwal "})
--

--Autoformat
vim.keymap.set({"n", "v"}, "<leader>lf", vim.lsp.buf.format, {silent = true, desc="Format the file "})


-- Open LazyGit
vim.keymap.set({"n", "v"}, "<leader>lg", ":LazyGit<CR>", {silent = true, desc="Open LazyGit "})
--


--Specific to harpoon

local harpoon = require("harpoon")

-- REQUIRED
harpoon:setup()
-- REQUIRED

vim.keymap.set("n", "<leader>ha", function() harpoon:list():append() end, {silent = true, desc="Add to harpoon"})
vim.keymap.set("n", "<leader>eh", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end, {silent = true, desc="toggle harpoon menu"})

-- Float Terminal
-- vim.keymap.set("n","<leader>tt", ":FloatermNew<CR>", {silent = true, desc="Open floaterm"})
-- vim.keymap.set("n","<leader>tf", ":FloatermToggle<CR>", {silent = true, desc="Toggle floaterm"})
-- vim.keymap.set("n","<leader>tn", ":FloatermNext<CR>", {silent = true, desc="Next floaterm"})
-- vim.keymap.set("n","<leader>tp", ":FloatermPrevious<CR>", {silent = true, desc="Previous floaterm"})
--
--
-- vim.keymap.set("t","<leader>tf", "<C-\\><C-N>:FloatermToggle<CR>", {silent = true, desc="Toggle floaterm"})
-- vim.keymap.set("t","<leader>tn", "<C-\\><C-N>:FloatermNext<CR>", {silent = true, desc="Next floaterm"})
-- vim.keymap.set("t","<leader>tp", "<C-\\><C-N>:FloatermPrevious<CR>", {silent = true, desc="Previous floaterm"})
--
-- Toogle Terminal

vim.keymap.set("n", "<leader>tt", ":ToggleTerm<CR>", {silent = true, desc="Toggle terminal"})
-- vim.keymap.set("", "<leader>tt", ":ToggleTerm<CR>", {silent = true, desc="Toggle terminal"})

require"toggleterm".setup {
  size = 55,
  direction = "vertical"
}


