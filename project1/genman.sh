start=`date +%s.%N`

# Clear old outputs
rm -rf ./outputs/master.txt

# get all txt files in ./inputs dir
files=`ls ./inputs/*.txt`

# some vars
COUNTER=1

echo "Running A* on all files in ./inputs with weights [1.0, 1.2, 1.4]"
echo ""
echo "PROGRESS  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
# Run search of each file 3 times with different weight and write output to file
for file in $files
do
  echo "Generating Master File"
  echo " " >>  './outputs/master.txt'
  echo "# $file with weight = 1.0: " >> './outputs/master.txt'
  python main.py -f $file -w 1.0 >> './outputs/master.txt'
  echo "   " >> "./outputs/master.txt"
  echo "   " >> "./outputs/master.txt" 
  echo " " >> './outputs/master.txt'
  echo "# $file with weight = 1.2: " >> './outputs/master.txt'
  python main.py -f $file -w 1.2 >> './outputs/master.txt'
  echo " " >> './outputs/master.txt'
  echo "   " >> "./outputs/master.txt"
  echo "   " >> "./outputs/master.txt"
  echo "# $file with weight = 1.4: " >> './outputs/master.txt'
  python main.py -f $file -w 1.4 >> './outputs/master.txt'
  echo "   " >> "./outputs/master.txt"
  echo "   " >> "./outputs/master.txt"
  let COUNTER++
done

end=`date +%s.%N`

