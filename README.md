# Cache-Simulator
Cache Simulator

## Python
### dependencies
* [Termtables](https://github.com/nschloe/termtables)

### manual
before using this code, you must install dependencies. to do that you can use python package managers like `pip` to install them:
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```
then you can run this program on your machine:
```bash
python3 main.py
```
**note :** you can pass your requests in Hexadecimal system. to do that you must enter `y` in first query when the program ask you "`Your input is in Hex(Y/n)`".
## Cache Structure in Output
|   #   | way 0 | way 1 | ... | way k-1 |
|:-----:|:-----:|:-----:|:---:|:-------:|
| set 0 | \<block_number\> [ word_list ] | \<block_number\> [ word_list ] | ... | \<block_number\> [ word_list ] |
| set 1 | \<block_number\> [ word_list ] | \<block_number\> [ word_list ] | ... | \<block_number\> [ word_list ] |
|  ...  | ... | ... | ... | ... |
| set b-1 | \<block_number\> [ word_list ] | \<block_number\> [ word_list ] | ... | \<block_number\> [ word_list ] |
 
## Contributors
* [Ali Asad](https://github.com/aliasad059)
* [AmirMohammad Babaei](https://github.com/AmirMohamadbabaee)