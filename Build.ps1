# ChatGPT Exporter Personal local build (PowerShell 5.1+).
# This file does NOT delete, overwrite or reset the upstream directory.
$ErrorActionPreference = 'Stop'
# Resolve all paths relative to the checked-out project.
$RunnerDir = $PSScriptRoot
$ProjectRoot = $PSScriptRoot
$Required = @('patches\apply.py','patches\finalize.py','patches\beijing.ts','patches\mdReferences.ts','tests\features.test.mjs')
$Missing = @($Required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $ProjectRoot $_)) })
Set-Location -LiteralPath $ProjectRoot
$LogFile = Join-Path $ProjectRoot 'build.log'
$Step = 'initialize'
[System.IO.File]::WriteAllText($LogFile, "ChatGPT Exporter Personal build`r`n", (New-Object System.Text.UTF8Encoding($false)))

function Log([string]$Message) {
    Write-Host $Message
    Add-Content -LiteralPath $LogFile -Value $Message -Encoding UTF8
}

function Fail([string]$Message) {
    throw "$Step : $Message"
}

function Run([string]$Executable, [string[]]$Arguments) {
    Log ("$> " + $Executable + ' ' + ($Arguments -join ' '))
    # Console and file logging. Stderr from native processes is not a
    # PowerShell terminating error: verify process exit codes explicitly.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $Executable @Arguments 2>&1 | ForEach-Object {
            $line = $_.ToString()
            Write-Host $line
            Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
        }
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previous
    }
    if ($null -eq $code -or $code -ne 0) {
        Fail ("Command exited with code " + $code + ' : ' + $Executable)
    }
}

function Need([string]$CommandName) {
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        Fail ("Missing command: " + $CommandName)
    }
}

try {
    Log ('Runner directory: ' + $RunnerDir)
    Log ('Project directory: ' + $ProjectRoot)
    if ($Missing.Count -gt 0) {
        Fail ('Incomplete project folder. Missing: ' + ($Missing -join ', ') + '. Extract the WHOLE ZIP first and run Build.cmd inside its own folder.')
    }
    $Step = 'dependency check'
    Log '[0/6] Checking Git, Python, Node and Corepack...'
    foreach ($name in @('git','python','node','corepack')) { Need $name }
    Run 'git' @('--version')
    Run 'python' @('--version')
    Run 'node' @('--version')
    Run 'corepack' @('--version')
    # Check the installed version in PowerShell, avoiding node -e quoting rules.
    $NodeVersionText = (& node -p 'process.versions.node' | Select-Object -First 1).Trim()
    if ($LASTEXITCODE -ne 0) { Fail 'Could not read Node version' }
    try { $NodeVersion = [Version]$NodeVersionText }
    catch { Fail ('Unrecognized Node version: ' + $NodeVersionText) }
    if ($NodeVersion -lt [Version]'22.16.0') { Fail ('Node 22.16+ required; found ' + $NodeVersionText) }
    Log ('Accepted Node version: ' + $NodeVersionText)

    $Step = 'official source check'
    Log '[1/6] Checking official source...'
    $Upstream = Join-Path $ProjectRoot 'upstream'
    if (-not (Test-Path -LiteralPath $Upstream)) {
        Log 'No upstream directory found; downloading official source into this folder.'
        Run 'git' @('clone', '--depth', '1', 'https://github.com/pionxzh/chatgpt-exporter.git', 'upstream')
    }
    if (-not (Test-Path -LiteralPath (Join-Path $Upstream 'src/exporter/markdown.ts')) -or
        -not (Test-Path -LiteralPath (Join-Path $Upstream 'package.json'))) {
        Fail 'upstream exists but is incomplete. Keep it and send build.log; do not delete it yet.'
    }

    $Step = 'personal source patch'
    Log '[2/6] Checking personal patches...'
    $BeijingPath = Join-Path $Upstream 'src/personal/beijing.ts'
    $ReferencePath = Join-Path $Upstream 'src/personal/mdReferences.ts'
    $Pkg = Get-Content -Raw -LiteralPath (Join-Path $Upstream 'package.json') -Encoding UTF8 | ConvertFrom-Json
    $Patched = ($Pkg.title -eq 'ChatGPT Exporter Personal')
    if ($Patched -and (Test-Path -LiteralPath $BeijingPath) -and (Test-Path -LiteralPath $ReferencePath)) {
        Log 'Personal patches found. Reusing existing patched source.'
    }
    elseif (-not $Patched -and -not (Test-Path -LiteralPath $BeijingPath) -and -not (Test-Path -LiteralPath $ReferencePath)) {
        Run 'python' @('patches/apply.py', 'upstream')
    }
    else {
        Fail 'Partial or inconsistent patch detected. Do not re-patch; send build.log for recovery.'
    }

    $Step = 'dependency installation'
    Log '[3/6] Installing project dependencies...'
    Push-Location -LiteralPath $Upstream
    try {
        Run 'corepack' @('pnpm', 'install', '--frozen-lockfile')
        $Step = 'vite build'
        Log '[4/6] Building userscript...'
        Run 'corepack' @('pnpm', 'build')
        $Step = 'official tests'
        Log '[5/6] Running upstream tests...'
        Run 'corepack' @('pnpm', 'test')
    }
    finally {
        Pop-Location
    }

    $Step = 'personal feature tests'
    Log '[6/6] Checking personal functions and creating userscript...'
    Run 'node' @('--experimental-strip-types', 'tests/features.test.mjs')
    $Step = 'userscript finalize'
    Run 'python' @('patches/finalize.py', 'upstream/dist/chatgpt.user.js', 'dist/ChatGPT_Exporter_Personal.user.js', '--revision', '1')
    $Step = 'JavaScript syntax check'
    Run 'node' @('--check', 'dist/ChatGPT_Exporter_Personal.user.js')
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot 'dist/ChatGPT_Exporter_Personal.user.js'))) {
        Fail 'Build finished but the output .user.js file is missing.'
    }
    Log 'SUCCESS: dist/ChatGPT_Exporter_Personal.user.js'
    Log 'Note: GitHub auto-update requires a published repo URL; not configured for local build.'
    exit 0
}
catch {
    Log ('FAILED at: ' + $Step)
    Log $_.Exception.Message
    Log 'Keep upstream intact. Please share the end of build.log.'
    exit 1
}
