@echo off

git add .
git commit -m "Add push script!"
git pull
git push

echo Done!
pause>nul