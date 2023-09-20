# Get general system information
$systemInfo = Get-CimInstance -ClassName Win32_ComputerSystem

# Get processor information
$processorInfo = Get-CimInstance -ClassName Win32_Processor

# Get memory (RAM) information
$memoryInfo = Get-CimInstance -ClassName Win32_PhysicalMemory

# Get disk drive information
$diskInfo = Get-CimInstance -ClassName Win32_DiskDrive

# Get laptop serial number from Win32_BIOS
$serialNumber = (Get-CimInstance -ClassName Win32_BIOS).SerialNumber

# Get network adapter information
$networkInfo = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration | Where-Object { $_.IPAddress -ne $null }

# Calculate the total memory capacity
$totalMemoryCapacity = ($memoryInfo | Measure-Object -Property Capacity -Sum).Sum

# Display the collected information
Write-Host "System Information"
Write-Host "------------------"
Write-Host "Manufacturer: $($systemInfo.Manufacturer)"
Write-Host "Model: $($systemInfo.Model)"
Write-Host "Processor: $($processorInfo.Name)"
Write-Host "Serial Number: $serialNumber"
Write-Host "Memory: $($totalMemoryCapacity / 1GB) GB"
Write-Host "Disk Drive:"
foreach ($drive in $diskInfo) {
    Write-Host "  - Model: $($drive.Model)"
    Write-Host "  - Size: $($drive.Size / 1GB) GB"
}
Write-Host "Network Adapter:"
foreach ($adapter in $networkInfo) {
    Write-Host "  - Description: $($adapter.Description)"
    Write-Host "  - IP Address: $($adapter.IPAddress)"
}