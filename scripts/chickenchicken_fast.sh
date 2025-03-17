start_time=$(date +%s)

for level in 'large'; do
    echo $level

    auto_mask_start_time=$(date +%s)
    CUDA_VISIBLE_DEVICES=2 python auto-mask-fast.py \
        --video_path videos/chickenchicken \
        --output_dir output/chickenchicken \
        --batch_size 40 \
        --detect_stride 20 \
        --level ${level}
    auto_mask_end_time=$(date +%s)
    auto_mask_elapsed_time=$((auto_mask_end_time - auto_mask_start_time))

    visulization_start_time=$(date +%s)
    CUDA_VISIBLE_DEVICES=2 python visulization.py \
        --video_path videos/chickenchicken \
        --output_dir output/chickenchicken \
        --level ${level}
    visulization_end_time=$(date +%s)
    visulization_elapsed_time=$((visulization_end_time - visulization_start_time))

    echo "auto-mask-batch.py execution time: ${auto_mask_elapsed_time} seconds"
    echo "visulization.py execution time: ${visulization_elapsed_time} seconds"

done

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Total execution time: ${elapsed_time} seconds"