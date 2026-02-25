return {
  'mrcjkb/rustaceanvim',
  version = '^5',
  lazy = false,
  ft = { 'rust' },
  dependencies = {
    'hrsh7th/cmp-nvim-lsp',
  },
  config = function()
    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

    vim.g.rustaceanvim = {
      tools = {
        enable_clippy = true,
      },
      server = {
        capabilities = capabilities,
        on_attach = function(client, bufnr)
          vim.lsp.inlay_hint.enable(true, { bufnr = bufnr })
        end,
        default_settings = {
          ['rust-analyzer'] = {
            cargo = {
              allFeatures = true,
            },
            checkOnSave = {
              command = "clippy",
            },
            inlayHints = {
              enable = true,
            },
          },
        },
      },
    }
  end
}
