

InTrD="../../"
DName="full2024-fusion"
OutDir="../../"

SubDir="ncod81_efficientnet_b3_efficientnet_b3"

strings=("train_body.csv" "test_body.csv")
outstr=("train.csv" "test.csv")

ipynb-py-convert create_dataset.ipynb create_dataset.py

for ((i=0; i<${#strings[@]}; i++)); do
    CsvFile="${strings[i]}"
    CsvOutFile="${outstr[i]}"
    python3 create_dataset.py   --model-type-body 'efficientnet_b3' \
                                --model-type-face 'efficientnet_b3' \
                                --model-type-skel 81 \
                                --dataset-dir $InTrD \
                                --dataset-file $CsvFile \
                                --dataset-out-file $CsvOutFile \
                                --dataset-name $DName \
                                --sub-dir $SubDir \
                                --output-dir $OutDir
done




rm -f create_dataset.py
