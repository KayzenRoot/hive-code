#!/usr/bin/env python3
from pathlib import Path


def replace_exact(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected source block not found in {path}")
    p.write_text(text.replace(old, new, 1))

# Separate hidden/obfuscated content from legitimate but executable recipe surfaces.
replace_exact(
    "crates/goose/src/recipe/mod.rs",
    '''    /// Returns true when a recipe contains content or executable surfaces that require
    /// an explicit trust decision before execution.
    pub fn check_for_security_warnings(&self) -> bool {
        if [self.instructions.as_deref(), self.prompt.as_deref()]
            .iter()
            .flatten()
            .any(|&field| contains_unicode_tags(field))
        {
            return true;
        }

        if self.activities.as_ref().is_some_and(|activities| {
            activities
                .iter()
                .any(|activity| contains_unicode_tags(activity))
        }) {
            return true;
        }

        if self.extensions.as_ref().is_some_and(|extensions| {
            extensions
                .iter()
                .any(|extension| matches!(extension, ExtensionConfig::Stdio { .. }))
        }) {
            return true;
        }

        if self.retry.as_ref().is_some_and(|retry| {
            !retry.checks.is_empty()
                || retry
                    .on_failure
                    .as_ref()
                    .is_some_and(|command| !command.trim().is_empty())
        }) {
            return true;
        }

        false
    }
''',
    '''    /// Returns true when recipe text contains hidden Unicode tag content.
    pub fn has_hidden_content_warning(&self) -> bool {
        [self.instructions.as_deref(), self.prompt.as_deref()]
            .iter()
            .flatten()
            .any(|&field| contains_unicode_tags(field))
            || self.activities.as_ref().is_some_and(|activities| {
                activities
                    .iter()
                    .any(|activity| contains_unicode_tags(activity))
            })
    }

    /// Returns true when running the recipe can introduce local process execution,
    /// shell-based retry behavior, or delegated sub-recipe execution.
    pub fn has_executable_surfaces(&self) -> bool {
        self.extensions.as_ref().is_some_and(|extensions| {
            extensions
                .iter()
                .any(|extension| matches!(extension, ExtensionConfig::Stdio { .. }))
        }) || self.retry.as_ref().is_some_and(|retry| {
            !retry.checks.is_empty()
                || retry
                    .on_failure
                    .as_ref()
                    .is_some_and(|command| !command.trim().is_empty())
        }) || self
            .sub_recipes
            .as_ref()
            .is_some_and(|sub_recipes| !sub_recipes.is_empty())
    }

    /// Returns true when a recipe requires a security decision before execution.
    pub fn check_for_security_warnings(&self) -> bool {
        self.has_hidden_content_warning() || self.has_executable_surfaces()
    }
''',
)

# Saving through ACP remains fail-closed for security-sensitive recipes until the desktop has
# a durable explicit-trust model. Use accurate wording instead of claiming every warning is
# hidden Unicode.
replace_exact(
    "crates/goose/src/acp/server/recipe/mod.rs",
    '''        if recipe.check_for_security_warnings() {
            return Err(agent_client_protocol::Error::invalid_params().data(
                "This recipe contains hidden characters that could be malicious. Please remove them before trying to save.",
            ));
        }
''',
    '''        if recipe.check_for_security_warnings() {
            return Err(agent_client_protocol::Error::invalid_params().data(
                "This recipe contains hidden content or executable surfaces that require an explicit trust decision before it can be saved through ACP.",
            ));
        }
''',
)

# CLI execution: reject hidden content; recursively inspect sub-recipes; require an explicit
# interactive trust decision for local process/shell/delegation surfaces. Quiet mode fails closed.
replace_exact(
    "crates/goose-cli/src/recipes/extract_from_cli.rs",
    '''use std::path::PathBuf;

use anyhow::{anyhow, Result};
use goose::recipe::{Recipe, SubRecipe};
''',
    '''use std::collections::HashSet;
use std::path::{Path, PathBuf};

use anyhow::{anyhow, Context, Result};
use goose::recipe::manifest::load_recipe_from_path;
use goose::recipe::{Recipe, SubRecipe};
''',
)

replace_exact(
    "crates/goose-cli/src/recipes/extract_from_cli.rs",
    '''pub fn extract_recipe_info_from_cli(
''',
    '''fn inspect_recipe_tree_for_execution(recipe: &Recipe) -> Result<bool> {
    if recipe.has_hidden_content_warning() {
        anyhow::bail!("Recipe execution blocked because hidden Unicode tag content was detected");
    }

    let mut has_executable_surfaces = recipe.has_executable_surfaces();
    let mut pending: Vec<PathBuf> = recipe
        .sub_recipes
        .as_deref()
        .unwrap_or_default()
        .iter()
        .map(|sub_recipe| PathBuf::from(&sub_recipe.path))
        .collect();
    let mut seen = HashSet::new();

    while let Some(path) = pending.pop() {
        let canonical = path
            .canonicalize()
            .with_context(|| format!("Failed to resolve sub-recipe {}", path.display()))?;
        if !seen.insert(canonical.clone()) {
            continue;
        }
        let child = load_recipe_from_path(&canonical)
            .with_context(|| format!("Failed to inspect sub-recipe {}", canonical.display()))?;
        if child.has_hidden_content_warning() {
            anyhow::bail!(
                "Recipe execution blocked because hidden Unicode tag content was detected in sub-recipe {}",
                canonical.display()
            );
        }
        has_executable_surfaces |= child.has_executable_surfaces();
        pending.extend(
            child
                .sub_recipes
                .as_deref()
                .unwrap_or_default()
                .iter()
                .map(|sub_recipe| PathBuf::from(&sub_recipe.path)),
        );
    }

    Ok(has_executable_surfaces)
}

fn require_recipe_execution_trust(recipe: &Recipe, quiet: bool) -> Result<()> {
    if !inspect_recipe_tree_for_execution(recipe)? {
        return Ok(());
    }

    if quiet {
        anyhow::bail!(
            "Recipe execution requires explicit approval because it can start local processes, run shell checks, or delegate sub-recipes; quiet mode cannot provide that approval"
        );
    }

    let approved = cliclack::confirm(
        "This recipe can execute local processes, shell checks, or delegated sub-recipes. Continue?",
    )
    .initial_value(false)
    .interact()?;
    if !approved {
        anyhow::bail!("Recipe execution cancelled by user");
    }
    Ok(())
}

pub fn extract_recipe_info_from_cli(
''',
)

replace_exact(
    "crates/goose-cli/src/recipes/extract_from_cli.rs",
    '''    let mut recipe = load_recipe(&recipe_name, params.clone()).unwrap_or_else(|err| {
        eprintln!("{}: {}", console::style("Error").red().bold(), err);
        std::process::exit(1);
    });
    if !quiet {
''',
    '''    let mut recipe = load_recipe(&recipe_name, params.clone()).unwrap_or_else(|err| {
        eprintln!("{}: {}", console::style("Error").red().bold(), err);
        std::process::exit(1);
    });
    require_recipe_execution_trust(&recipe, quiet)?;
    if !quiet {
''',
)

# Deterministic regression coverage avoids interactive prompts by exercising quiet mode.
p = Path("crates/goose-cli/src/recipes/extract_from_cli.rs")
text = p.read_text()
marker = '''    #[test]
    fn test_extract_recipe_info_from_cli_with_additional_sub_recipes() {'''
tests = '''    #[test]
    fn executable_recipe_fails_closed_in_quiet_mode() {
        let temp_dir = tempfile::tempdir().unwrap();
        let recipe_path = temp_dir.path().join("exec_recipe.yaml");
        std::fs::write(
            &recipe_path,
            r#"title: executable
description: executable recipe
prompt: hello
extensions:
  - type: stdio
    name: local-tool
    cmd: echo
    args: [hello]
"#,
        )
        .unwrap();

        let result = extract_recipe_info_from_cli(
            recipe_path.to_string_lossy().to_string(),
            Vec::new(),
            Vec::new(),
            true,
        );
        assert!(result.is_err());
    }

    #[test]
    fn hidden_content_in_subrecipe_is_rejected() {
        let temp_dir = tempfile::tempdir().unwrap();
        let child_path = temp_dir.path().join("child.yaml");
        let parent_path = temp_dir.path().join("parent.yaml");
        let hidden_tag = '\\u{E0001}';
        std::fs::write(
            &child_path,
            format!("title: child\\ndescription: child\\nprompt: 'hello{hidden_tag}'\\n"),
        )
        .unwrap();
        std::fs::write(
            &parent_path,
            "title: parent\\ndescription: parent\\nprompt: hello\\nsub_recipes:\\n  - name: child\\n    path: child.yaml\\n",
        )
        .unwrap();

        let recipe = load_recipe(parent_path.to_str().unwrap(), Vec::new()).unwrap();
        assert!(inspect_recipe_tree_for_execution(&recipe).is_err());
    }

'''
if tests not in text:
    if marker not in text:
        raise SystemExit("CLI recipe test insertion marker not found")
    p.write_text(text.replace(marker, tests + marker, 1))

# Core test: sub-recipes themselves are a trust-requiring execution surface.
p = Path("crates/goose/src/recipe/mod.rs")
text = p.read_text()
marker = '''    #[test]
    fn test_from_content_with_json() {'''
core_test = '''    #[test]
    fn security_scan_flags_sub_recipes() {
        let recipe = Recipe::from_content(
            r#"version: \"1.0.0\"
title: parent
description: parent
prompt: hello
sub_recipes:
  - name: child
    path: child.yaml
"#,
        )
        .unwrap();
        assert!(recipe.has_executable_surfaces());
        assert!(recipe.check_for_security_warnings());
    }

'''
if core_test not in text:
    if marker not in text:
        raise SystemExit("Core recipe test insertion marker not found")
    p.write_text(text.replace(marker, core_test + marker, 1))

print("wave 6 recipe trust-boundary patches applied")
