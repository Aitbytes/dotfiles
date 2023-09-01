
change_color(){
    destination_file=$HOME/.config/glava/radial.glsl
    color_file=$HOME/.cache/wal/colors
    color7=$(head -n 7 $color_file|tail -n 1) 
    color3=$(head -n 3 $color_file|tail -n 1) 
    echo $color
    # sed -i 's/OUTLINE.*^/OUTLINE $color/g' $destination_file 
    sed -i "s/\(OUTLINE\).*/\1 $color7/g" $destination_file
    sed -i "19,18s/(#....../($color3/g" $destination_file

} 

if test -e /tmp/glavad.pid; then
    echo already_there
    pid=$(cat /tmp/glavad.pid)
    kill $pid
    change_color
    glava -d &
    echo $! > /tmp/glavad.pid
else
    echo not_there
   # change_color
   # glava -d &
   # echo $! > /tmp/glavad.pid
fi

