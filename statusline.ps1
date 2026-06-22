#!/usr/bin/env pwsh
# Claude Code statusLine script
# Reads JSON from stdin and outputs a compact status line

$input_data = $null
try {
    $raw = [Console]::In.ReadToEnd()
    $input_data = $raw | ConvertFrom-Json
} catch {
    exit 0
}

# --- Helper: ANSI color codes ---
$reset   = "`e[0m"
$dim     = "`e[2m"
$bold    = "`e[1m"
$cyan    = "`e[36m"
$yellow  = "`e[33m"
$green   = "`e[32m"
$blue    = "`e[34m"
$magenta = "`e[35m"
$red     = "`e[31m"
$white   = "`e[37m"

$sep = "${dim}|${reset}"

# --- Helper: compact time-remaining until a reset epoch (e.g. 2h13m, 3d4h, 9m) ---
function Format-Remaining($resetsAt) {
    if ($null -eq $resetsAt) { return $null }
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $d = [int]([double]$resetsAt - $now)
    if ($d -le 0) { return "0m" }
    $days  = [int][Math]::Floor($d / 86400)
    $hours = [int][Math]::Floor(($d % 86400) / 3600)
    $mins  = [int][Math]::Floor(($d % 3600) / 60)
    if ($days -ge 1)  { return "${days}d${hours}h" }
    elseif ($hours -ge 1) { return "${hours}h${mins}m" }
    else { return "${mins}m" }
}

$parts = [System.Collections.Generic.List[string]]::new()

# --- Time ---
$time = Get-Date -Format "HH:mm"
$parts.Add("${dim}${white}${time}${reset}")

# --- CWD (basename) ---
$cwd = $input_data.cwd
if ($cwd) {
    $cwdShort = Split-Path $cwd -Leaf
    if (-not $cwdShort) { $cwdShort = $cwd }  # root edge case
    $parts.Add("${cyan}${cwdShort}${reset}")
}

# --- Git repo name and branch ---
$repoName = $null
$branch   = $null

$repo = $input_data.workspace.repo
if ($repo -and $repo.name) {
    $repoName = $repo.name
}

# Try to get branch from git (skip optional locks, read-only)
try {
    $gitDir = $null
    if ($cwd -and (Test-Path $cwd)) {
        $gitDir = & git -C $cwd rev-parse --git-dir 2>$null
    }
    if ($gitDir) {
        $branch = & git -C $cwd symbolic-ref --short HEAD 2>$null
        if (-not $branch) {
            $branch = & git -C $cwd rev-parse --short HEAD 2>$null
        }
        # If we didn't get repo name from JSON, derive from remote
        if (-not $repoName) {
            $remote = & git -C $cwd remote get-url origin 2>$null
            if ($remote) {
                $repoName = [System.IO.Path]::GetFileNameWithoutExtension(($remote -split '[/:]')[-1])
            }
        }
    }
} catch {}

# Worktree branch override
$worktreeBranch = $input_data.worktree.branch
if ($worktreeBranch) { $branch = $worktreeBranch }

$gitPart = ""
if ($repoName -and $branch) {
    $gitPart = "${green}${repoName}${reset}${dim}:${reset}${yellow}${branch}${reset}"
} elseif ($repoName) {
    $gitPart = "${green}${repoName}${reset}"
} elseif ($branch) {
    $gitPart = "${yellow}${branch}${reset}"
}
if ($gitPart) { $parts.Add($gitPart) }

# --- Model name ---
$modelName = $input_data.model.display_name
if ($modelName) {
    # Shorten common names
    $modelShort = $modelName `
        -replace 'Claude ', 'C ' `
        -replace ' Sonnet', ' Son' `
        -replace ' Haiku', ' Hai' `
        -replace ' Opus', ' Ops'
    $parts.Add("${magenta}${modelShort}${reset}")
}

# --- Effort level ---
$effort = $input_data.effort.level
if ($effort) {
    $effortColor = switch ($effort) {
        'max'    { $red }
        'xhigh'  { $yellow }
        'high'   { $cyan }
        default  { $dim }
    }
    $parts.Add("${effortColor}${effort}${reset}")
}

# --- Context usage ---
$usedPct = $input_data.context_window.used_percentage
if ($null -ne $usedPct) {
    $pctInt = [int][Math]::Round($usedPct)
    $ctxColor = $green
    if ($pctInt -ge 75) { $ctxColor = $red }
    elseif ($pctInt -ge 50) { $ctxColor = $yellow }
    $parts.Add("${dim}ctx:${reset}${ctxColor}${pctInt}%${reset}")
}

# --- Token count (input tokens used in context window) ---
$totalIn = $input_data.context_window.total_input_tokens
if ($null -ne $totalIn -and $totalIn -gt 0) {
    if ($totalIn -ge 1000) {
        $tokShort = "{0:F1}k" -f ($totalIn / 1000)
    } else {
        $tokShort = "$totalIn"
    }
    $parts.Add("${dim}tok:${reset}${white}${tokShort}${reset}")
}

# --- Rate limits (Claude.ai subscribers) ---
$fiveHour = $input_data.rate_limits.five_hour.used_percentage
if ($null -ne $fiveHour) {
    $fh = [int][Math]::Round($fiveHour)
    $rlColor = if ($fh -ge 80) { $red } elseif ($fh -ge 50) { $yellow } else { $green }
    $fhRem = Format-Remaining $input_data.rate_limits.five_hour.resets_at
    $fhTime = if ($fhRem) { "${dim}(${fhRem})${reset}" } else { "" }
    $parts.Add("${dim}5h:${reset}${rlColor}${fh}%${reset}${fhTime}")
}

# --- Weekly rate limit (7-day) ---
$sevenDay = $input_data.rate_limits.seven_day.used_percentage
if ($null -ne $sevenDay) {
    $wk = [int][Math]::Round($sevenDay)
    $wkColor = if ($wk -ge 80) { $red } elseif ($wk -ge 50) { $yellow } else { $green }
    $wkRem = Format-Remaining $input_data.rate_limits.seven_day.resets_at
    $wkTime = if ($wkRem) { "${dim}(${wkRem})${reset}" } else { "" }
    $parts.Add("${dim}7d:${reset}${wkColor}${wk}%${reset}${wkTime}")
}

# --- Vim mode ---
$vimMode = $input_data.vim.mode
if ($vimMode) {
    $vmColor = switch ($vimMode) {
        'INSERT'      { $green }
        'VISUAL'      { $yellow }
        'VISUAL LINE' { $yellow }
        default       { $blue }
    }
    $parts.Add("${vmColor}${vimMode}${reset}")
}

# --- PR badge ---
$prNum = $input_data.pr.number
if ($null -ne $prNum) {
    $prState = $input_data.pr.review_state
    $prColor = switch ($prState) {
        'approved'          { $green }
        'changes_requested' { $red }
        'draft'             { $dim }
        default             { $cyan }
    }
    $prLabel = if ($prState) { "PR#${prNum}(${prState})" } else { "PR#${prNum}" }
    $parts.Add("${prColor}${prLabel}${reset}")
}

# --- Dotfiles drift (cached ~10min; silent no-op if python/repo missing) ---
try {
    $syncPy = Join-Path $HOME "dotfiles\sync.py"
    if (Test-Path $syncPy) {
        $cacheFile = Join-Path $env:TEMP "dotfiles-audit-count.txt"
        $fresh = (Test-Path $cacheFile) -and `
                 (((Get-Date) - (Get-Item $cacheFile).LastWriteTime).TotalSeconds -lt 600)
        $count = $null
        if ($fresh) {
            $count = (Get-Content $cacheFile -Raw -ErrorAction SilentlyContinue).Trim()
        } else {
            $out = (& python $syncPy audit --quiet 2>$null | Out-String).Trim()
            if ($out -match '^\d+$') {
                $count = $out
                Set-Content -Path $cacheFile -Value $count -ErrorAction SilentlyContinue
            }
        }
        $n = 0
        if ([int]::TryParse($count, [ref]$n) -and $n -gt 0) {
            $parts.Add("${red}dotfiles:${n}!${reset}")
        }
    }
} catch {}

# --- Output ---
$line = $parts -join " ${sep} "
Write-Host $line
