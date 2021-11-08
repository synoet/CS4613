rm -rf ./outputs

mkdir outputs

files=`ls ./inputs/*.txt`

COUNTER=1
BEG='./outputs/output'
END='.txt'
A='a'
B='b'
C='c'

for file in $files
do
  python main.py -f $file -w 1.0 > $BEG$COUNTER$A$END
  python main.py -f $file -w 1.2 > $BEG$COUNTER$B$END
  python main.py -f $file -w 1.4 > $BEG$COUNTER$C$END
  let COUNTER++
done


