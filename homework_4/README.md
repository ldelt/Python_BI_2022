
# README
>Python 3.10.8  
>Operating System: Manjaro Linux  
>KDE Plasma Version: 5.26.3  
>KDE Frameworks Version: 5.99.0  
>Qt Version: 5.15.7  
>Kernel Version: 5.15.78-1-MANJARO (64-bit)  
>Graphics Platform: X11  
>Processors: 4 × Intel® Core™ i5-2500 CPU @ 3.30GHz  
>Memory: 7.7 ГиБ of RAM  
>Graphics Processor: NVC1  
>Manufacturer: Gigabyte Technology Co., Ltd  
>Product Name: P67-DS3-B3  
1. **Preparing the work directory and repository branch**
  ```cd Python_BI_2022```  
  ```git checkout main```  
  ```git checkout -b homework_4```  
  ```mkdir homework_4```  
  ```cd homework_4```  
  ```touch README.md```  
  ```wget https://raw.githubusercontent.com/krglkvrmn/Virtual_environment_research/master/pain.py```  
2. **Create environment**
```python3.10 -m venv hw_4_venv```  
```cd hw_4_venv```  
```source bin/activate```  
```cd ..```  
3. **Installing google package**
The ```pip install google``` command did not help, a stackoverflow search says to use the command:  
```pip install --upgrade google-api-python-client```
4. **Install kivy and bs4 packages**
```pip install kivy```   
```pip install bs4```   
5. **Installing biopython package**
The ``` pip install bio``` command installs package version 1.80. Later it turns out that it is incompatible with the pain.py script. The official biopython repository page says: *The Bio.SubsMat module was deprecated in Release 1.78, and removed in Release 1.80*.Let's install package version 1.77.  
``` pip install biopython==1.77``` 
6. **Installing aiohttp, pandas, scipy, scanpy**
```pip install aiohttp```  
```pip install pandas```  
```pip install scipy```  
```pip install scanpy```  
7. **Installing cv2**
The command ```pip install cv2``` does not work. A search on stackoverflow led me to the command  
```pip install opencv-python```  
8. **Installing lxml**
```pip install lxml```
9. **Successfully run the script**
```python3.10 pain.py```
10. **Create requirements.txt file**
```pip freeze > requirements.txt```
