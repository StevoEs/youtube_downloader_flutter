# Automatisch Tag mit Datum erstellen und pushen
$tag = "v" + (Get-Date -Format "yyyy-MM-dd")
Write-Output "Erstelle Tag: $tag"

git add .
git commit -m "Update on $tag"
git push origin main

git tag $tag
git push origin $tag
