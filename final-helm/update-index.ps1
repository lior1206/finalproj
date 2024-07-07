# Define variables
$repoUrl = "https://your-repo-url/charts/"
$indexFile = "./index.yaml"
$helmChartDir = "."  # Update this to your Helm chart directory path

# Change directory to the Helm chart directory
Set-Location -Path $helmChartDir

# Generate or update index.yaml
helm repo index . --url $repoUrl --merge $indexFile