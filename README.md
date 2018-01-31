# Introduction


Trying to show the very bottom lines of machine learning.
Where in each knowledge-based system, a given agent starts with
basic grammar rules and empty databases.
It will simultaneously conversate and gain knowledge by what is told
to him.


# Installing
You can install MyBot with:
```sh
$ git clone https://github.com/FilippoL/mybot.git
```

In order to run the python files ou will need the following modules to be imported as well as your own telegram token

```sh
    $ pip install python-telegram-bot --upgrade
    $ pip install nltk
    $ pip install uuid4
    $ python
```
And then in the python shell you should run:

```sh
    import nltk
    nltk.download()
    #from the interface install nltk_data package
```

# Chat commands
To start the conversation:
 ```sh 
 /start 
 ```
To interrupt at during answer or question:
  ```sh 
 /cancel 
 ```

# Known issues
Doesn't always handle more than answer per question, although it will still store it in the database.

# Credits
A really big thanks to the creators of the "python-telegram-bot" library, which can be found [here]

# License

You may copy, distribute and modify the software provided that modifications are described and licensed for free under [LGPL-3] . Derivatives works (including modifications or anything statically linked to the library) can only be redistributed under LGPL-3, but applications that use the library don't have to be.


   [here]: <https://github.com/python-telegram-bot/python-telegram-bot/blob/master/README.rst>
   [LGPL-3]: <https://www.gnu.org/licenses/lgpl-3.0.html>
