# nel-lo
## Requirements
https://github.com/isawnyu/pleiades_search_api (requires python 3.10.2)

If not using python 3.10.2, it will still work, but the requirement in setup.py has to be changed
```
install_requires=[
        "feedparser",
        "textnorm",
        "webiquette",
#        "webiquette @ git+https://github.com/paregorios/webiquette.git",
    ],
#    python_requires=">=3.10.2",
)


and also, https://github.com/isawnyu/webiquette needs to be installed manually and also modified in setup.py to not require python 3.10.2

spacy version TODO
