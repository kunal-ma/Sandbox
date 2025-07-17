# Task: Create Git commits with custom date and time
# Description: This script allows the developer to specify a custom date and time for a Git commit. It is particularly useful for correcting missed commits in a coding streak.

# Permissions: None
# Dependencies: Git installed and available in PATH

# Usage: .\TimeMachine.ps1 -Day 1 -Month 12 -Year 2025 -Hour 14 -Minute 1 -Second 12

# WARNING: No error checking is implemented, hence verify all parameters are valid beforehand. 

# WARNING: Not recommended for use in repositories with CI/CD pipelines, as it may interfere with automated processes.

# --------------------------------------------------

# Variables for user provided date and time parameters
param(
    [int]$Day,
    [int]$Month,
    [int]$Year,
    [int]$Hour,
    [int]$Minute = -1,      # Optional, random if not specified
    [int]$Second = -1       # Optional, random if not specified
)

# Format the day and hour as two-digit strings for consistency
$DayStr   = $Day.ToString("00")
$MonthStr = $Month
$YearStr  = $Year
$HourStr  = $Hour.ToString("00")

# If Minute not specified, generate and assign a random value
if ($Minute -eq -1) {
    $Minute = Get-Random -Minimum 0 -Maximum 60
}

# If Second not specified, generate and assign a random value
if ($Second -eq -1) {
    $Second = Get-Random -Minimum 0 -Maximum 60
}

# Format the minute and second as two-digit strings
$MinuteStr = $Minute.ToString("00")
$SecondStr = $Second.ToString("00")

# Convert month from numeric value to string
$Months = @("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
$MonthAbbr = $Months[$Month - 1]

# Create the full date string in the format YYYY-MM-DD
$DateStr = "$Year-$MonthStr-$DayStr"
# Get the weekday abbreviation (Mon, Tue, etc.) for the given date
$Weekday = (Get-Date $DateStr).ToString("ddd")

# Combine the components into the final commit date string
$FinalDate = "$Weekday, $DayStr $MonthAbbr $YearStr $HourStr`:$MinuteStr`:$SecondStr +0530"

# Set Git environment variables to calculated value
$env:GIT_AUTHOR_DATE = $FinalDate
$env:GIT_COMMITTER_DATE = $FinalDate

# Show Git environment variables' values for verification
Write-Host "GIT_AUTHOR_DATE set to: $env:GIT_AUTHOR_DATE"
Write-Host "GIT_COMMITTER_DATE set to: $env:GIT_COMMITTER_DATE"

# Stage all changes, commit them, and push commit to Github
git add .
git commit
git push

# Clear Git environment variables after completion
Remove-Item Env:GIT_AUTHOR_DATE
Remove-Item Env:GIT_COMMITTER_DATE
