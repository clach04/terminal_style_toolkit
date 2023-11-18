#!/bin/bash

# based on script from

# from https://bbs.archlinux.org/viewtopic.php?id=51818&p=1%29
# also see http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html

# shows color/colour names. NOTE needs 86 columns (and regular 24 lines)

#
#   This file echoes a bunch of color codes to the 
#   terminal to demonstrate what's available.  Each 
#   line is the color code of one forground color,
#   out of 17 (default + 16 escapes), followed by a 
#   test use of that color on all nine background 
#   colors (default + 8 escapes).
#

T='gYw'   # The test text

# declare -A color_map=( ['    m']='    m' ['   1m']='   1m'
# ['1;37m']='TESTx')

# standard ansi mappings, generated this by reviewing https://bluesock.org/~willkg/dev/ansi.html
declare -A color_map=(
    ['    m']="normal" ['   1m']="bold" ['  30m']="black" ['1;30m']="blackB" ['  31m']="red"
    ['1;31m']="redB" ['  32m']="green" ['1;32m']="greenB" ['  33m']="yellow"
    ['1;33m']="yellowB" ['  34m']="blue" ['1;34m']="blueB" ['  35m']="magenta"
    ['1;35m']="magentaB" ['  36m']="cyan" ['1;36m']="cyanB" ['  37m']="white"
    ['1;37m']="whiteB"

    ['40m']="black" ['41m']="red" ['42m']="green" ['43m']="yellow"
    ['44m']="blue"    ['45m']="magenta" ['46m']="cyan" ['47m']="white"

)


echo -en "                      ";
for BG in 40m 41m 42m 43m 44m 45m 46m 47m;
do
    bgcolor_name=${color_map[$BG]}
    bgcolor_name=`printf "%8s" ${bgcolor_name}`

    echo -en "${bgcolor_name}";
done


#echo -e "\n                 40m     41m     42m     43m\
#     44m     45m     46m     47m";

echo -e "\n                         40m     41m     42m     43m\
     44m     45m     46m     47m";

for FGs in '    m' '   1m' '  30m' '1;30m' '  31m' '1;31m' '  32m' \
           '1;32m' '  33m' '1;33m' '  34m' '1;34m' '  35m' '1;35m' \
           '  36m' '1;36m' '  37m' '1;37m';
  do FG=${FGs// /}
  # echo [\'$FG\']=\"$FG\"  # generate hash table mapping
  fgcolor_name=${color_map[$FGs]}
  fgcolor_name=`printf "%8s" ${fgcolor_name}`
  echo -en "${fgcolor_name} $FGs \033[$FG  $T  "
  for BG in 40m 41m 42m 43m 44m 45m 46m 47m;
    do echo -en "$EINS \033[$FG\033[$BG  $T  \033[0m";
  done
  #echo -en ${color_name};
  #printf "%8s" ${color_name}
  echo;

done
echo

infocmp|grep colors
env TERM=xterm-256color infocmp | grep colors
