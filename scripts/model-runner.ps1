# Run this script from powershell as:
# powershell.exe -executionpolicy bypass ./model-runner.ps1 modelfilename <arg1>....<argn>


param(
    [string]$model,
    [string]$arg1,
    [string]$arg2,
    [string]$arg3
)

function create_config_file {
    param(
        [string]$path
    )
    $JSON_OBJECT = @{
        parentUrl = ""
    }
    $json = $JSON_OBJECT | ConvertTo-Json
    $json | Set-Content -Path $path
}

$SCRIPTS_DIRECTORY = $PSScriptRoot
$JSON_CONFIG_PATH = $SCRIPTS_DIRECTORY + "\\config.json"
Write-Output $JSON_CONFIG_PATH

if (!(Test-Path $JSON_CONFIG_PATH)) {
    create_config_file($JSON_CONFIG_PATH)
}

$JSON = Get-Content -Path $JSON_CONFIG_PATH -Raw | ConvertFrom-JSON
switch($model) {
    "model1" {
        Write-Output "Running model1";
        $PARENT_URL = $JSON.parentUrl
        if ($PARENT_URL.Length -gt 0) {
            Write-Output "parentUrl is defined as [$PARENT_URL] in config.json"
        } else {
            Write-Output "parentUtl is empty. Correct the config.json. Exiting."
            exit 1
        }
        $URL = $arg1
        $CHANNEL_NAME = $arg2
        $FEED_FILE_NAME = $arg3
        python $SCRIPTS_DIRECTORY\$model".py" $URL $CHANNEL_NAME $JSON.parentUrl "MULTI_FILE" $FEED_FILE_NAME
    }
    "model2" {
        $PARENT_URL = $JSON.parentUrl
        Write-Output "PARENT URL = $PARENT_URL"
        if ($PARENT_URL.Length -gt 0) {
            Write-Output "parentUrl is defined as [$PARENT_URL] in config.json"
        } else {
            Write-Output "parentUrl is empty. Correct the config.json. Exiting."
            exit 1
        }
        Write-Output "Running model2";
        $URL = $arg1
        $CHANNEL_NAME = $arg2
        python $SCRIPTS_DIRECTORY\$model".py" $CHANNEL_NAME $JSON.parentUrl $URL
    }
    "model3" {
        Write-Output "Running model3";
        $FILEPATH = $arg1
        python $SCRIPTS_DIRECTORY\$model".py" $FILEPATH
    }
    "model4" {
        Write-Output "Running model4";
        $DOMAIN_NAME = $arg1
        $QUERY = $arg2
        $FEED_FILE_NAME = $arg3
        python $SCRIPTS_DIRECTORY\$model".py" $DOMAIN_NAME $QUERY "SINGLE_FILE" $FEED_FILE_NAME
    }
    "--help" {
        Write-Output "Commands : "
        Write-Output "model1 <url> <channel-name> <feed-file-name>"
        Write-Output "model2 <url> <channel-name>"
        Write-Output "model3 <-- Requires the existence of input.txt to contain entries for media resolution"
        Write-Output "model4 <domain_name> <query_string> <feed_file_name>"
    }
    default {
        Write-Output "Unknown model: $model"
        Write-Output ""
        Write-Output "Commands : "
        Write-Output "model1 <url> <channel-name> <feed-file-name>"
        Write-Output "model2 <url> <channel-name>"
        Write-Output "model3 <-- Requires the existence of input.txt to contain entries for media resolution"
        Write-Output "model4 <domain_name> <query_string> <feed_file_name>"
    }
}

