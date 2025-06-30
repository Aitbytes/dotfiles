return {
  "olimorris/codecompanion.nvim",
  opts = {
    strategies = {
      -- Change the default chat adapter
      chat = {
        adapter = "anthropic",
      },
    },
  },
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-treesitter/nvim-treesitter",
    "ravitemer/mcphub.nvim",
  },

}
