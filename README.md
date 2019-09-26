# CIRNO
**C**IRNO:  
**I**ntelligence for  
**R**ecognizing,  
**N**avigating and  
**O**perating ingame.   

Yes, You heard it right, Let's make Cirno be a intellectual being!  

## Supported Platforms
 * Micro$oft Window$ Platforms
 * Linux Systems whose Desktop Manager has GTK3 Support

 Yes, bad news here. macOS didn't make it. But Tim Cook is deprecating x86 support so whatever! TH17 was also distributed in x86 binary. not x86_64.

## Thesis
Brief idea:  
Process the Image:  
Raw Pixel Data as matrices:  
implement reinforcement learning idea from [Google I/O 2018: Reinforcement Learning without a PhD.](https://www.youtube.com/watch?v=t1A3NTttvBA) ~~(well i can ask my professor, but this project is somehow embarrassing to show him)~~ (No, I can just ask Chris about it LOLOLOLOLOL)  

Using Reinforcement Learning in FIFA 18 to perfect the art of free-kicks:
[Youtube](https://www.youtube.com/watch?time_continue=1&v=MasxAN-xZIU)
  
Since controlling is much like a categorization,  
we are going to use ConvNet with reLU (if possible, leaky reLU) and will use softmax for final decision.  

The goal:  
Creating General Artifical Neural Network for solving all Touhou Project games (which seems impossible for me, but let me try)  

## Update
This project is now part of Pattern Recognition and Machine Learning Laboratory Sub-Project.

### 2019-08-08
![image](https://user-images.githubusercontent.com/27724108/62657673-facb2000-b9a1-11e9-997f-3e7d80e4d5f4.png)  
Saved screenshot. Finally.  

### 2019-09-09
Yes, I didn't give up the Linux Systems.  
You know, Computers at Lab has Ubuntu installed, Not Windows!  

### 2019-09-27
Changing Framework into pyTorch!  
Neural network design revised! I am gonna use DQN (Deep Q Network)  
  
I wonder how can i send info of game lively into framework running on  
Linux and Touhou project running in WineHQ Container 🤔  
