for level in  'large' 'middle' 'small' 'default';do
echo $level
python auto-mask-batch.py \
    --video_path videos/chickenchicken \
    --output_dir output/chickenchicken \
    --batch_size 40 \
    --detect_stride 10 \
    --level ${level}
python visulization.py \
    --video_path videos/chickenchicken \
    --output_dir output/chickenchicken \
    --level ${level}
done