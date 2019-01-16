```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PATH=${HOME}/.pyenv/bin:$PATH' >> ~/.zshenv
echo 'export PYENV_ROOT=${HOME}/.pyenv' >> ~/.zshenv
echo 'eval "$(pyenv init -)"' >> ~/.zshenv
source ~/.zshenv

pyenv install --list
pyenv install <version>
pyenv install -v <version> # 若发生错误，显示错误详情
pyenv versions             # 显示当前 python 版本
pyenv which python         # 显示当前 python 路径
pyenv global <version>     # 设置全局默认 python 版本(~/.pyenv/version)
pyenv local <version>      # 设置当前路径默认 python 版本(./.python-version)
pyenv shell <version>      # 设置当前 shell session 默认 python 版本(优先级高于 global 及 local)

pyenv install -v 3.6.0
pyenv global 3.6.0
```