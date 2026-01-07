{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "dotfiles-env";
  buildInputs = with pkgs; [
    # Window Managers & Compositors
    hyprland

    # Terminal
    alacritty

    # Shells
    bash
    zsh

    # Editors
    neovim
    vim

    # Application Launcher
    rofi

    # Vibe coding
    gemini-cli
    opencode

    pulumi


    # Other Tools
    stow
    rclone
    pywal
    zellij
    lazygit
    ltex-ls
    languagetool
    nodemon
    pandoc
    opentofu

    # Neovim Dependencies (LSPs, etc.)
    clang-tools # for clangd
    gopls
    pyright
    rust-analyzer
    nodejs # for typescript-language-server
    nodePackages.typescript-language-server
    nodePackages.vscode-langservers-extracted # for html, css, json, etc.
    lua53Packages.luarocks-nix
    lua51Packages.lua
    python312Packages.hvac

    lua-language-server
    uv
    pulumiPackages.pulumi-python
    # texlive.combined.scheme-full # for vimtex. This is a large package and can be commented out to speed up shell activation.

    # Build dependencies for plugins
    gnumake
    gcc
    ripgrep
    fd
    unzip # for nvim-dap
  ];
  

  shellHook = ''
    echo "Entered dotfiles development environment."
    export PS1="[dotfiles-env] $PS1"
    exec zsh
  '';
}
