return {
  'ojroques/nvim-osc52',
  config = function()
    require('osc52').setup {
      max_length = 0,           -- Maximum length of selection (0 = no limit)
      silent = false,           -- Disable messages on successful copy
      trim = false,             -- Trim text before copy
      tmux_passthrough = true,  -- Use tmux passthrough escape sequences
    }
    
    -- Setup clipboard integration
    vim.api.nvim_create_autocmd('TextYankPost', {
      callback = function()
        if vim.v.event.operator == 'y' and vim.v.event.regname == '' then
          require('osc52').copy_visual()
        end
      end,
    })
  end,
}