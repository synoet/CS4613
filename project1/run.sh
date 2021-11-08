# Clear old outputs
rm -rf ./outputs

# make new outputs folder
mkdir outputs

# get all txt files in ./inputs dir
files=`ls ./inputs/*.txt`

# some vars
COUNTER=1
BEG='./outputs/output'
END='.txt'
A='a'
B='b'
C='c'

# Run search of each file 3 times with different weight and write output to file
for file in $files
do
  python main.py -f $file -w 1.0 > $BEG$COUNTER$A$END
  python main.py -f $file -w 1.2 > $BEG$COUNTER$B$END
  python main.py -f $file -w 1.4 > $BEG$COUNTER$C$END
  let COUNTER++
done


