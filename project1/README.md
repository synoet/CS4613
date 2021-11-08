# A* Search

## How to Run
### Batch File Run & Write
The `run.sh` script will run main.py on all files within the ./inputs directory with different weights.
It will also write a seperate output file for each variation of weight for each input file.

***Before running this you should add whatever input files you want to the `./inputs/` folder***

```
chmod +x && ./run.sh
```
Example output: 
![](https://raw.githubusercontent.com/nysteo/CS4613/master/project1/example.png?token=ACQQFUYWZMOAJLJCTIYQAUDBRGP2U)

### Individual Files (without file writing)

**Running on individual filles with specified weights.**
```
python main.py -f ./inputs.input1.txt -w 1.0
```
*Note: running `main.py` directly will not write out to a file, only display the output*

pass the `-f` flag followed by the file name to run a specific file.
```
python main.py -f ./inputs/input3.txt
```
pass the `-w` flag followed by a weight to run with a specific weight
```
python main.py -w 2.3
```

**Running with debug turned on**
```
python main.py -f ./inputs/input1.txt --debug
```

Running with debug flag will output a graphical representation of the state at each step.
