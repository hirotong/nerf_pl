###
 # @Author: hiro.tong
### 
python train.py \
   --dataset_name llff \
   --root_dir /home/hiro/dataset/jiahao \
   --N_importance 64 --img_wh 272 640 \
   --num_epochs 30 --batch_size 2048 \
   --optimizer adam --lr 5e-4 \
   --lr_scheduler steplr --decay_step 10 20 --decay_gamma 0.5 \
   --exp_name cup_video \
   --spheric_poses