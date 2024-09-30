# functions_sandbox
Azure functions Sanbox


## Rosetta設定を追加する。
`.zshrc`に以下を追加する。
```
if [ "$(arch)" = "arm64" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    eval "$(/usr/local/bin/brew shellenv)"
fi
```
これで、homebrewをrosettaとarm64で分けることができる。

azure func-core toolsは、rosettaを使用しないと使えないため、rosettaでインストールする。

```
brew tap azure/functions
brew install azure-functions-core-tools@4
```

vscodeからrosettaを使える様にするために、以下を`settings.json`に追加する。
これを追加すると、rosettaというターミナル名で、ターミナルを起動することができる。ターミナル+ボタンから選択できる。
```
"terminal.integrated.profiles.osx": {
    "rosetta": {
        "path": "arch",
        "args": [
            "-x86_64",
            "zsh",
            "-l"
        ],
        "overrideName": true
    }
},
"terminal.integrated.defaultProfile.osx": "rosetta"
```