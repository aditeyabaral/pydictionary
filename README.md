# PyDictionary

PyDictioanry is an offline English dictionary made using Python along with the Wordnet Lexical Database and Enchant Spell Dictionary. The project is a very simple one made to understand the complete functionality of Wordnet and to test the extent of its resources. It also includes a spell checker, and the option to add in custom words to the dictionary. The application returns any query with a list of results - the various word forms and their meanings along with a sample sentence using the given word.

PyDictionary is a complete project, and can be used as a full fledged offline English dictionary. Although limited, it does the same job Google search does when searched with a word.

# How to execute

1. Create a virtualenv

```
python -m venv env
```

1. Activate virtualenv

```
source env/bin/activate
```

1. Install dependencies

```
pip install -r requirements.txt
```

1. Install dev dependencies (needed for code linting)

```
pip install -r requirements-dev.txt
```

1. Run the dictionary with any world

```
python PyDictionary.py hello
```


# How to run flask app

```
flask run
```
