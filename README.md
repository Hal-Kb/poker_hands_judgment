# poker_hands_judgment
The Edge AI that recognizes playing cards and determines poker hands.<br>
Please check the operation on YouTube.<br>
[YouTube](https://www.youtube.com/watch?v=WUNSz5v2cBo)<br>

## Requirement
Please prepare the following items.<br>
* Jetson Nano Development Kit
  * Have [JetPack 4.6.1(Japanese version)](https://developer.nvidia.com/ja-jp/embedded/jetpack) installed<br>    
* Logicool Web Camera C270n
* Playing Cards
* Game Table (other than white color)

## Setup

### Hello AI World
Build the operating environment by referring to the following YouTube video on [Hello AI World](https://github.com/dusty-nv/jetson-inference/blob/master/README.md) GitHub.<br>
* [Hello AI World Setup](https://www.youtube.com/watch?v=QXIwdsyK7Rw&list=PL5B692fm6--uQRRDTPsJDp4o0xbzkoyf8&index=10)
* [Training Image Classification Models](https://www.youtube.com/watch?v=sN6aT9TpltU&list=PL5B692fm6--uQRRDTPsJDp4o0xbzkoyf8&index=12)
* [Training Object Detection Models](https://www.youtube.com/watch?v=2XMkPW_sIGg&list=PL5B692fm6--uQRRDTPsJDp4o0xbzkoyf8&index=14)

### In Addition
* Clone the required files from GitHub.
  ```
  git clone -b master https://github.com/Hal-Kb/poker_hands_judgment.git
  ```
* Overwrite and copy the files in the [bin] folder obtained from GitHub to the following folder.
  ```
  ~/jetson-inference/build/aarch64/bin
  ```
* Copy the folder in the [models] folder obtained from GitHub to the following folder.
  ```
  ~/jetson-inference/python/training/detection/ssd/models
  ```
* Overwrite the folder in the [tools] folder obtained from GitHub to the following folder.
  ```
  ~/jetson-inference/tools
  ```
* Overwrite and copy the [CMakeLists.txt] file obtained from GitHub to the following folder.
  ```
  ~/jetson-inference
  ```

## Run
Execute the following command and show the target card with the camera.
```
cd jetson-inference/build/aarch64/bin/
python3 detectnet_trump.py /dev/video0
```



