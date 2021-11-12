start=`date +%s.%N`

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

echo "Running A* on all files in ./inputs with weights [1.0, 1.2, 1.4]"
echo ""
echo "PROGRESS  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
# Run search of each file 3 times with different weight and write output to file
for file in $files
do
  echo "Running A* on $file"
  python main.py -f $file -w 1.0> $BEG$COUNTER$A$END
  echo "  -> Ran sucessfully with weight 1.0 and wrote output to $BEG$COUNTER$A$END"
  python main.py -f $file -w 1.2 > $BEG$COUNTER$B$END
  echo "  -> Ran sucessfully with weight 1.2 and wrote output to $BEG$COUNTER$B$END"
  python main.py -f $file -w 1.4 > $BEG$COUNTER$C$END
  echo "  -> Ran sucessfully with weight 1.4 and wrote output to $BEG$COUNTER$C$END"
  let COUNTER++
done

end=`date +%s.%N`

echo ""
echo "SUMMARY - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
runtime=$( echo "$end - $start" | bc -l )
files_created=$( echo "($COUNTER - 1) * 3" | bc -l)
echo "  Variations Ran: $files_created"
echo "  Runtime: $runtime seconds"
