#!/usr/bin/env bash

pkl_dir=/home/jiangyy/projects/rib_20181212/medical-rib/cache
output_dir=/home/jiangyy/projects/rib_20181214/medical-rib/temp_output
#python3 main.py --pkl_path "/home/jiangyy/projects/rib_20181212/medical-rib/cache/135402000550272.pkl" --output_prefix $output_dir/"hello_123"

#exit
files=$(ls $pkl_dir)
array=("135402000565843.pkl" "135402000572309.pkl" "A1076955.pkl" "A1076956.pkl")
# array=("A1076956.pkl")
for f in ${array[@]};
do
    file_path=$pkl_dir/$f
    if [[ "$file_path" == *.pkl ]]
    then
        prefix=${f%%".pkl"}
        echo "cut $prefix data"
        folder=$output_dir/$prefix
        if [[ -d "$folder" ]]; then
            rm -r "$folder"
        fi
        echo "$folder"
        mkdir "$folder"

        python3 main.py --pkl_path "$file_path" --output_prefix "$folder"/ > $output_dir/$prefix".log"
    fi
done