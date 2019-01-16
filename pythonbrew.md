```bash
curl -kL http://xrl.us/pythonbrewinstall | bash
echo '[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc' | ~/.zshrc
pythonbrew list
pythonbrew list -k
pythonbrew install 3.5.4
pythonbrew use 3.5.4
pythonbrew switch 3.5.4
```