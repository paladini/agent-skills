#!/usr/bin/env bash
set -euo pipefail

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "Use scripts/link-global-skills.ps1 on Windows so directory links are created natively." >&2
    exit 2
    ;;
esac

agent="codex"
target_roots=()
requested_skills=()

while (($#)); do
  case "$1" in
    --agent)
      (($# >= 2)) || { echo "Missing value for --agent" >&2; exit 2; }
      agent="$2"
      shift 2
      ;;
    --target-root)
      (($# >= 2)) || { echo "Missing value for --target-root" >&2; exit 2; }
      target_roots+=("$2")
      shift 2
      ;;
    --skill)
      (($# >= 2)) || { echo "Missing value for --skill" >&2; exit 2; }
      requested_skills+=("$2")
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Usage: link-global-skills.sh [--agent codex|claude|agents|all] [--target-root PATH ...] [--skill NAME ...]

Link skills from this repository into a user's global skill directory.
Existing destinations are preserved and reported as conflicts.
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

repo_root="$(cd -- "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
skill_root="$repo_root/skills"
home_root="$(cd -- "$HOME" && pwd -P)"
codex_home="${CODEX_HOME:-$home_root/.codex}"
if [[ "$codex_home" != /* ]]; then
  codex_home="$PWD/$codex_home"
fi
legacy_codex_root="$codex_home/skills"
shared_agents_root="$home_root/.agents/skills"
if ((${#target_roots[@]} == 0)); then
  case "$agent" in
    codex|agents) target_roots=("$HOME/.agents/skills") ;;
    claude) target_roots=("$HOME/.claude/skills") ;;
    all) target_roots=("$HOME/.agents/skills" "$HOME/.claude/skills") ;;
    *) echo "Invalid --agent: $agent" >&2; exit 2 ;;
  esac
fi

shopt -s nullglob
skills=()
for candidate in "$skill_root"/*/; do
  [[ -f "$candidate/SKILL.md" ]] && skills+=("${candidate%/}")
done
if ((${#requested_skills[@]} > 0)); then
  selected_skills=()
  for requested in "${requested_skills[@]}"; do
    found=false
    for skill in "${skills[@]}"; do
      if [[ "$(basename "$skill")" == "$requested" ]]; then
        selected_skills+=("$skill")
        found=true
        break
      fi
    done
    if [[ "$found" != true ]]; then
      echo "Unknown skill name: $requested" >&2
      exit 2
    fi
  done
  skills=("${selected_skills[@]}")
fi
if ((${#skills[@]} == 0)); then
  echo "No skills containing SKILL.md were found in $skill_root" >&2
  exit 1
fi

conflicts=()
for target_root in "${target_roots[@]}"; do
  if [[ "$target_root" != /* ]]; then
    target_root="$PWD/$target_root"
  fi
  mkdir -p "$target_root"
  target_root="$(cd -- "$target_root" && pwd -P)"
  for source in "${skills[@]}"; do
    source="$(cd -- "$source" && pwd -P)"
    name="$(basename "$source")"
    destination="$target_root/$name"
    if [[ "$target_root" == "$shared_agents_root" ]]; then
      legacy_destination="$legacy_codex_root/$name"
      if [[ -L "$legacy_destination" ]]; then
        legacy_target="$(readlink "$legacy_destination")"
        if [[ "$legacy_target" != /* ]]; then
          legacy_target="$(dirname "$legacy_destination")/$legacy_target"
        fi
        if [[ -d "$legacy_target" ]]; then
          legacy_target="$(cd -- "$legacy_target" && pwd -P)"
        fi
        if [[ "$legacy_target" == "$source" ]]; then
          echo "Already linked in legacy Codex root: $legacy_destination"
          continue
        fi
      elif [[ -e "$legacy_destination" ]]; then
        conflicts+=("$legacy_destination")
        echo "Preserved legacy Codex skill to avoid a duplicate: $legacy_destination" >&2
        continue
      fi
    fi
    if [[ -L "$destination" ]]; then
      link_target="$(readlink "$destination")"
      if [[ "$link_target" != /* ]]; then
        link_target="$(dirname "$destination")/$link_target"
      fi
      if [[ -d "$link_target" ]]; then
        link_target="$(cd -- "$link_target" && pwd -P)"
      fi
      if [[ "$link_target" == "$source" ]]; then
        echo "Already linked: $destination"
        continue
      fi
    elif [[ -e "$destination" ]]; then
      conflicts+=("$destination")
      echo "Preserved existing destination: $destination" >&2
      continue
    fi

    ln -s "$source" "$destination"
    echo "Linked: $destination -> $source"
  done
done

if ((${#conflicts[@]} > 0)); then
  echo "${#conflicts[@]} existing destination(s) were preserved. Inspect and move them manually, then rerun:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  exit 1
fi
