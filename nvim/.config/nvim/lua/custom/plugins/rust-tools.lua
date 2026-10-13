return {
  'mrcjkb/rustaceanvim',
  version = '^5',
  lazy = false,
  ft = { 'rust', 'toml' },
  dependencies = {
    'hrsh7th/cmp-nvim-lsp',
  },
  config = function()
    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

    -- codelldb installed via mason (works on NixOS)
    local mason_codelldb = vim.fn.stdpath 'data' .. '/mason/packages/codelldb/extension'
    local codelldb_path = mason_codelldb .. '/adapter/codelldb'
    local liblldb_path = mason_codelldb .. '/lldb/lib/liblldb.so'
    local has_codelldb = vim.uv.fs_stat(codelldb_path) and vim.uv.fs_stat(liblldb_path)

    vim.g.rustaceanvim = {
      tools = {
        enable_clippy = true,
        float_win_config = {
          border = 'rounded',
        },
      },
      server = {
        capabilities = capabilities,
        on_attach = function(client, bufnr)
          -- Same keymaps as every other LSP buffer (gd, gr, K, <leader>rn, ...)
          require('user.lspmaps').attach(client, bufnr)

          -- Inlay hints on by default (<leader>lh toggles globally)
          vim.lsp.inlay_hint.enable(true, { bufnr = bufnr })

          -- Rust indentation: rustfmt uses 4 spaces
          vim.bo[bufnr].tabstop = 4
          vim.bo[bufnr].shiftwidth = 4
          vim.bo[bufnr].softtabstop = 4
          vim.bo[bufnr].expandtab = true

          local rmap = function(keys, rhs, desc, modes)
            vim.keymap.set(modes or 'n', keys, rhs,
              { buffer = bufnr, silent = true, desc = 'Rust: ' .. desc })
          end

          -- rustaceanvim commands
          rmap('<leader>rr', '<Cmd>RustLsp runnables<CR>', '[R]unnables')
          rmap('<leader>rd', '<Cmd>RustLsp debuggables<CR>', '[D]ebuggables')
          rmap('<leader>rt', '<Cmd>RustLsp testables<CR>', '[T]estables under cursor')
          rmap('<leader>re', '<Cmd>RustLsp explainError<CR>', '[E]xplain error under cursor')
          rmap('<leader>rD', '<Cmd>RustLsp renderDiagnostic<CR>', 'Render [D]iagnostic (markdown)')
          rmap('<leader>rm', '<Cmd>RustLsp expandMacro<CR>', 'Expand [M]acro under cursor')
          rmap('<leader>rc', '<Cmd>RustLsp openDocs<CR>', 'Open docs.rs for item under [c]ursor')
          rmap('<leader>rf', '<Cmd>RustLsp flyCheck run<CR>', 'Run clippy/[f]lycheck now')
          rmap('<leader>rh', '<Cmd>RustLsp hover actions<CR>', '[H]over actions (run, implement, ...)')
          rmap('<leader>rs', ':RustLsp ssr ', '[S]tructural search & replace (ssr)')
          rmap('<leader>ra', '<Cmd>RustLsp moveItem 1<CR>', 'Move item [a] down')
          rmap('<leader>rA', '<Cmd>RustLsp moveItem -1<CR>', 'Move item up')
          rmap('<leader>rJ', '<Cmd>RustLsp joinLines<CR>', '[J]oin selected lines', { 'n', 'v' })

          -- Debug adapter keymaps (buffer-local, rust only)
          local dap, dapui = require('dap'), require('dapui')
          rmap('<F5>', dap.continue, 'Debug: Start/Continue')
          rmap('<F10>', dap.step_over, 'Debug: Step Over')
          rmap('<F11>', dap.step_into, 'Debug: Step Into')
          rmap('<S-F11>', dap.step_out, 'Debug: Step Out')
          rmap('<leader>db', dap.toggle_breakpoint, 'Toggle [B]reakpoint')
          rmap('<leader>du', dapui.toggle, 'Toggle DAP [U]I')
        end,
        default_settings = {
          ['rust-analyzer'] = {
            cargo = {
              allFeatures = true,
              buildScripts = true,
            },
            procMacro = {
              enable = true,
            },
            -- Modern key (replaces deprecated checkOnSave): clippy on save
            check = {
              command = 'clippy',
            },
            inlayHints = {
              closureReturnTypeHints = { enable = true },
              lifetimeElisionHints = { enable = true, useParameterNames = true },
            },
            completion = {
              -- Complete private fields/items from workspace crates
              privateEditable = { enable = true },
            },
          },
        },
      },
      dap = has_codelldb and {
        adapter = require('rustaceanvim.config').get_codelldb_adapter(codelldb_path, liblldb_path),
      } or {},
    }

    -- Format with rust-analyzer (rustfmt) on save
    vim.api.nvim_create_autocmd('BufWritePre', {
      group = vim.api.nvim_create_augroup('RustFormat', { clear = true }),
      pattern = '*.rs',
      callback = function()
        vim.lsp.buf.format {
          async = false,
          filter = function(c)
            return c.name == 'rust-analyzer'
          end,
        }
      end,
    })
  end,
}
