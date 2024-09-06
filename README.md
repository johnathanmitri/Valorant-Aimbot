Work in progress Valorant Aimbot. It sounded like a cool idea so I tried it. 

First, python captures from OBS virtual webcam. This is my way of capturing the screen from my code without anti cheat stopping me.

This is streamed over to my laptop, which uses a YOLOv8 model trained on a dataset of valorant players, and detects their location on screen.

Using the location, it moves the mouse using the Arduino. I spliced up an old PS/2 mouse cable, and wired it into the Arduino, and the Arduino is connected to my desktop as though it is a PS/2 mouse. 

I planned to make it much better, but this it for now.

Here it is meandering around on its own, shooting some enemies.

https://github.com/johnathanmitri/Valorant-Aimbot/assets/28831749/90e138c6-ac99-4d36-8f74-2256e3ac9eb3





