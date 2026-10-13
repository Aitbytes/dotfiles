return {
  'Saecki/crates.nvim',
  tag = 'stable',
  event = { 'BufRead Cargo.toml', 'BufNewFile Cargo.toml' },
  dependencies = { 'hrsh7th/nvim-cmp' },
  config = function()
    require('crates').setup({
      completion = {
        cmp = {
          enabled = true,
        },
      },
    })

    -- crates.io completion when editing Cargo.toml
    require('cmp').setup.filetype('toml', {
      sources = {
        { name = 'crates' },
        { name = 'path' },
        { name = 'buffer' },
      },
    })

    -- Buffer-local keymaps for Cargo.toml files
    vim.api.nvim_create_autocmd('FileType', {
      group = vim.api.nvim_create_augroup('CratesKeymaps', { clear = true }),
      pattern = 'toml',
      callback = function(event)
        local map = function(lhs, rhs, desc)
          vim.keymap.set('n', lhs, rhs, { buffer = event.buf, silent = true, desc = 'Crates: ' .. desc })
        end
        map('<leader>ct', require('crates').toggle, 'Toggle')
        map('<leader>cv', require('crates').show_versions_popup, 'Show [v]ersions')
        map('<leader>cf', require('crates').show_features_popup, 'Show [f]eatures')
        map('<leader>cd', require('crates').show_dependencies_popup, 'Show [d]ependencies')
        map('<leader>cu', require('crates').update_crate, '[u]pdate crate under cursor')
        map('<leader>cU', require('crates').upgrade_crate, '[U]pgrade crate under cursor')
        map('<leader>cA', function()
          require('crates').update_all_crates()
        end, 'Update [A]ll crates')
      end,
    })
  end,
}
