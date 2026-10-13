-- Formatting (conform.nvim) and linting (nvim-lint) via CLI tools installed
-- by Mason: sqlfluff (SQL), hadolint (Dockerfiles).
-- SQL has no working LSP (sqls/sqlls are abandoned, sqlfluff never had one),
-- so linting/formatting is done through these CLI wrappers instead.

return {
  {
    'stevearc/conform.nvim',
    event = { 'BufWritePre' },
    cmd = { 'ConformInfo' },
    keys = {
      {
        '<leader>lf',
        function()
          require('conform').format({ lsp_format = 'fallback' })
        end,
        mode = { 'n', 'v' },
        desc = 'Format buffer (conform, LSP fallback)',
      },
    },
    opts = {
      formatters_by_ft = {
        sql = { 'sqlfluff' },
      },
      format_on_save = false,
      formatters = {
        sqlfluff = {
          -- conform requires a project config root by default; relax it so
          -- standalone .sql files use the global ~/.config/sqlfluff/.sqlfluff
          -- (projects with their own .sqlfluff still take precedence).
          require_cwd = false,
        },
      },
    },
  },
  {
    'mfussenegger/nvim-lint',
    event = { 'BufReadPost', 'BufNewFile' },
    config = function()
      require('lint').linters_by_ft = {
        sql = { 'sqlfluff' },
        dockerfile = { 'hadolint' },
      }
      vim.api.nvim_create_autocmd({ 'BufWritePost', 'InsertLeave' }, {
        group = vim.api.nvim_create_augroup('nvim-lint-run', { clear = true }),
        callback = function()
          require('lint').try_lint()
        end,
      })
    end,
  },
}
