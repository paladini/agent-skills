[CmdletBinding()]
param(
    [ValidateSet('codex', 'claude', 'agents', 'all')]
    [string]$Agent = 'codex',
    [string[]]$TargetRoot,
    [string[]]$SkillName
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$skillRoot = Join-Path $repoRoot 'skills'
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$legacyCodexRoot = [System.IO.Path]::GetFullPath((Join-Path $codexHome 'skills'))
$sharedAgentsRoot = [System.IO.Path]::GetFullPath((Join-Path $HOME '.agents\skills'))

function Get-LinkTargetPath {
    param(
        [System.IO.FileSystemInfo]$Item,
        [string]$Path
    )

    $linkTarget = $Item.LinkTarget
    if (-not $linkTarget) {
        $fsutil = Join-Path $env:SystemRoot 'System32\fsutil.exe'
        $query = @(& $fsutil reparsepoint query $Path 2>$null)
        $text = $query -join "`n"
        $match = [regex]::Match($text, '(?im)^\s*Substitute Name:\s*(.+?)\s*$')
        if ($match.Success) {
            $linkTarget = $match.Groups[1].Value.Trim()
            if ($linkTarget.StartsWith('\??\UNC\', [System.StringComparison]::OrdinalIgnoreCase)) {
                $linkTarget = '\\' + $linkTarget.Substring(8)
            } elseif ($linkTarget.StartsWith('\??\', [System.StringComparison]::OrdinalIgnoreCase)) {
                $linkTarget = $linkTarget.Substring(4)
            }
        }
    }

    if (-not $linkTarget) {
        return $null
    }
    if ([System.IO.Path]::IsPathRooted($linkTarget)) {
        return [System.IO.Path]::GetFullPath($linkTarget)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Split-Path -Parent $Path) $linkTarget))
}

if (-not $TargetRoot -or $TargetRoot.Count -eq 0) {
    $agents = if ($Agent -eq 'all') { @('codex', 'claude', 'agents') } else { @($Agent) }
    $TargetRoot = foreach ($targetAgent in $agents) {
        switch ($targetAgent) {
            { $_ -in 'codex', 'agents' } { Join-Path $HOME '.agents\skills' }
            'claude' { Join-Path $HOME '.claude\skills' }
        }
    }
    $TargetRoot = @($TargetRoot | Select-Object -Unique)
}

$skills = @(Get-ChildItem -LiteralPath $skillRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
})
if ($skills.Count -eq 0) {
    throw "No skills containing SKILL.md were found in $skillRoot"
}
if ($SkillName -and $SkillName.Count -gt 0) {
    $missingSkills = @($SkillName | Where-Object { $_ -notin $skills.Name })
    if ($missingSkills.Count -gt 0) {
        throw "Unknown skill name(s): $($missingSkills -join ', ')"
    }
    $skills = @($skills | Where-Object { $_.Name -in $SkillName })
}

$conflicts = [System.Collections.Generic.List[string]]::new()
foreach ($root in $TargetRoot) {
    $targetPath = [System.IO.Path]::GetFullPath($root)
    if (-not (Test-Path -LiteralPath $targetPath)) {
        New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
    }

    foreach ($skill in $skills) {
        $destination = Join-Path $targetPath $skill.Name
        $source = [System.IO.Path]::GetFullPath($skill.FullName)
        if ($targetPath.TrimEnd('\') -ieq $sharedAgentsRoot.TrimEnd('\')) {
            $legacyDestination = Join-Path $legacyCodexRoot $skill.Name
            $legacyExisting = Get-Item -LiteralPath $legacyDestination -Force -ErrorAction SilentlyContinue
            if ($legacyExisting) {
                $legacyLink = $null
                if (($legacyExisting.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                    $legacyLink = Get-LinkTargetPath -Item $legacyExisting -Path $legacyDestination
                }
                if ($legacyLink -and $legacyLink.TrimEnd('\') -ieq $source.TrimEnd('\')) {
                    Write-Output "Already linked in legacy Codex root: $legacyDestination"
                    continue
                }
                $conflicts.Add($legacyDestination)
                Write-Warning "Preserved legacy Codex skill to avoid a duplicate: $legacyDestination"
                continue
            }
        }
        $existing = Get-Item -LiteralPath $destination -Force -ErrorAction SilentlyContinue
        if ($existing) {
            if (($existing.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                $resolvedLink = Get-LinkTargetPath -Item $existing -Path $destination
                if ($resolvedLink -and $resolvedLink.TrimEnd('\') -ieq $source.TrimEnd('\')) {
                    Write-Output "Already linked: $destination"
                    continue
                }
            }
            $conflicts.Add($destination)
            Write-Warning "Preserved existing destination: $destination"
            continue
        }

        New-Item -ItemType Junction -Path $destination -Target $source | Out-Null
        Write-Output "Linked: $destination -> $source"
    }
}

if ($conflicts.Count -gt 0) {
    Write-Error ("{0} existing destination(s) were preserved. Inspect and move them manually, then rerun: {1}" -f $conflicts.Count, ($conflicts -join ', '))
    exit 1
}
