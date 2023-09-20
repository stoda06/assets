# Get the OS information
$osInfo = uname -a

# Get the CPU information
$cpuInfo = lscpu

# Output the gathered data
"OS Info: $osInfo"
"CPU Info: $cpuInfo"
