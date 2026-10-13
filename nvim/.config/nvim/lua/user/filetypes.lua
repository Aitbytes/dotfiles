-- Filetype detection for the Docker / Jinja / SQL workflow
-- NOTE nvim 0.12: user patterns are matched against the file's tail (basename)
-- and are implicitly anchored (^pat$) -- so use .* prefixes, no $ anchors.

vim.filetype.add({
  pattern = {
    -- Docker Compose -> dedicated compose LSP (docker_compose_language_service)
    ['docker%-compose%.ya?ml'] = 'yaml.docker-compose',
    ['compose%.ya?ml'] = 'yaml.docker-compose',
    -- Jinja templates
    ['.*%.j2'] = 'jinja',
    ['.*%.jinja2?'] = 'jinja',
  },
})
