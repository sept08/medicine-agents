[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repositoryRoot = (& git rev-parse --show-toplevel).Trim()
if (-not $repositoryRoot) {
    throw 'Unable to resolve the Git repository root.'
}

$denyListPath = Join-Path $repositoryRoot '.local\sensitive_terms.txt'
if (-not (Test-Path -LiteralPath $denyListPath)) {
    Write-Error 'Missing .local/sensitive_terms.txt. Create the local, ignored denylist before committing.'
    exit 1
}

$sensitiveTerms = @(
    Get-Content -LiteralPath $denyListPath -Encoding UTF8 |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -and -not $_.StartsWith('#') }
)

if ($sensitiveTerms.Count -eq 0) {
    Write-Error 'The local sensitive-term denylist is empty; refusing to commit.'
    exit 1
}

$stagedPaths = @(& git diff --cached --name-only --diff-filter=ACMR)
$violations = [System.Collections.Generic.List[string]]::new()
$textExtensions = @(
    '.md', '.txt', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.ini', '.cfg',
    '.py', '.pyi', '.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html',
    '.sh', '.ps1', '.bat', '.cmd', '.sql', '.xml', '.csv', '.env', ''
)

foreach ($path in $stagedPaths) {
    $normalizedPath = $path.Replace('\', '/')
    if ($normalizedPath -eq 'wiki' -or $normalizedPath.StartsWith('wiki/')) {
        $violations.Add("Forbidden staged path: $path")
        continue
    }

    $extension = [System.IO.Path]::GetExtension($path).ToLowerInvariant()
    if ($textExtensions -notcontains $extension) {
        continue
    }

    $content = (& git show ":$path" 2>$null) -join "`n"
    if ($LASTEXITCODE -ne 0) {
        $violations.Add("Unable to inspect staged file: $path")
        continue
    }

    foreach ($term in $sensitiveTerms) {
        if ($content.IndexOf($term, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $violations.Add("Local sensitive term detected in: $path")
            break
        }
    }

    $genericPatterns = @(
        '(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])',
        '(?<!\d)1[3-9]\d{9}(?!\d)',
        '(?<!\d)\d{17}[0-9Xx](?!\d)'
    )
    foreach ($pattern in $genericPatterns) {
        if ($content -match $pattern) {
            $violations.Add("Possible email, mobile number, or identity number detected in: $path")
            break
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host 'Commit blocked by repository privacy policy:' -ForegroundColor Red
    $violations | Sort-Object -Unique | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

Write-Host 'Sensitive-content pre-commit check passed.' -ForegroundColor Green

