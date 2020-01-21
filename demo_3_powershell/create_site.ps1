param(
    [string] $namesJson
)

Install-Module -Name Az -AllowClobber -Scope CurrentUser -Force


$namesJson | ConvertFrom-Json | ConvertTo-Json -depth 100 | Out-File "web-files/file.json"

$ServicePrincipalUsername=""
$ServicePrincipalPassword=""
$SubscriptionId=""
$StorageAccountName=""
$ResourceGroup=""
$tenantId=""

$password = ConvertTo-SecureString $ServicePrincipalPassword -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential ($ServicePrincipalUsername, $password)
$pscredential = $Cred
Connect-AzAccount -ServicePrincipal -Credential $pscredential -Tenant $tenantId

New-AzStorageAccount -ResourceGroupName $ResourceGroup `
    -Name $StorageAccountName `
    -Location "eastus" `
    -SkuName "Standard_LRS" `
    -Kind "StorageV2"

$storageAccount = Get-AzStorageAccount -ResourceGroupName $ResourceGroup -AccountName $StorageAccountName
$ctx = $storageAccount.Context

Enable-AzStorageStaticWebsite -Context $ctx -IndexDocument index.html -ErrorDocument404Path 404.html

Set-AzStorageBlobContent -File "./web-files/index.html" `
  -Container "`$web" `
  -Blob "index.html" `
  -Properties @{"ContentType" = "text/html"} `
  -Context $ctx 

Set-AzStorageBlobContent -File "./web-files/file.json" `
  -Container "`$web" `
  -Blob "file.json" `
  -Context $ctx 

$WebEndpoint = (Get-AzStorageAccount -ResourceGroupName <RESOURCEGROUPNAME> -Name <STORAGEACCOUNTNAME>|select PrimaryEndpoints).PrimaryEndpoints.Web)

Write-Host "Website is hosted at: $WebEndpoint" 

