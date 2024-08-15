https://github.com/user-attachments/assets/a6b54c34-0d61-4589-b9ec-12d1b0e84460


## Overview:
This is an in-progress project building a simple DOOM clone using ascii. True to the original game it relies on ray casting to give it a 3D appearance. I'm using the curses library to run it in the terminal and handle text input.



## Usage:
1. clone the repo
   ```bash
   git clone https://github.com/liamstamper/ascii-doom.git
   ```

3. install requirements
    ```bash
    pip install -r requirements.txt
    ```
4. Run the game
   ```bash
   python3 ascii-doom.py
   ```

## Controls   

<sub>
                                                                                                                                                     
                                                                                                                                                         
                                                              1110000000000000000000000000111                                                            
                                                          1110011                        1100011                                                         
                                                         101101                             011101                                                       
                                                        101 101                             11  101                 W - Move Forward                                             
                                                       101   01                             11   00                                                           
                                                       101   01       101  10001  101       11   00                                  
                                                       101   01       101  10001 1001       11   00                                                   
                                                       101   01       1001101100 101        11   00                 S - Move Backward                                     
                                                       101   01        1011011001101        11   00                                                      
                                                       101   01        10001  10001         11   00                                                       
                                                       101   01         1111   1111         11   00                                                      
                                                       101   01                             11   00                 A - Turn Left                                        
                                                       101   01                             11   00                                                       
                                                       101   11                             01   00                                                      
                                                       101   11                             01   00                                                       
                                                       101  10011                         1101   00                 D - Turn Right                                       
                                                       101 1011011111111111111111111111111011101 00                                                      
                                                       100101 11                          101 10100                                                  
                                                        100  11                            101 1001                                                      
                                                         101101                             101101                                                       
                                                          11100000000000000000000000000000000011                                                         
                                                                                                                                                         
                                                                                                                                                         
                                                                                                                                                         
             1111111111111111111111111111111                  1111111111111111111111111111111                  111111111111111111111111111111            
          1000001111111111111111111111100011011           111100011111111111111111111111110001111          11101000011111111111111111111111000011        
        1011101                         111  1101       11011101                           1111101        1011 1111                         1011001      
       101 101                           101   101      001  11                             11  101      101   11                            11  001     
       101 101                           101   101     101   01                             11   00      00    11                            11  101     
       101 101                           101   101     101   01                             11   00      00    11                            11  101     
       101 101           10001           101   101     101   01           1000001           11   00      00    11         100110011          11  101     
       101 101          1001001          101   101     101   01          1001               11   00      00    11         101   1001         11  101     
       101 101          101 101          101   101     101   01          1100111            11   00      00    11         101    1001        11  101     
       101 101         100111001         101   101     101   01             110001          11   00      00    11         101    1001        11  101     
       101 101        1001111100         101   101     101   01          111111001          11   00      00    11         1011111001         11  101     
       101 101        111    1111        101   101     101   01          11111111           11   00      00    11         11111111           11  101     
       101 101                           101   101     101   01                             11   00      00    11                            11  101     
       101 101                           101   101     101  101                             11   00      00    11                            11  101     
       101  01                           101   101     101   11                             01   00      00    10                            11  101     
       101 10011                        10011  101     101  10011                         11011  00      00   11011                        11011 101     
       1011011011111111111111111111111110111011101     10111111011111111111111111111111111001101100      0011111100111111111111111111111111001101101     
       1001  01                         1111 10001     10001 101                           11  1001      10011 101                          01 10001     
        101111                            1011101       1001101                             1111001      10011101                           1011101      
         110011111111111111111111111111111100011         1100011111111111111111111111111111110001          100001111111111111111111111111111100011       
            111111111111111111111111111111111               11111111111111111111111111111111111               111111111111111111111111111111111          
   
   
                                                                                                                                            
                                                            1111111111111111111111111111111                  111111111111111111111111111111            
                                                        111100011111111111111111111111110001111          11101000011111111111111111111111000011        
                                                       11011101                           1111101        1011 1111                         1011001      
                                                      001  11                             11  101      101   11                            11  001     
                    M - Toggle Map                    101   01                             11   00      00    11                            11  101     
                                                      101   01                             11   00      00    11                            11  101     
                                                      101   01         1000   1001         11   00      00    11         100110011          11  101     
                                                      101   01         10001  00001        11   00      00    11       101      1001        11  101     
                                                      101   01        101101 101101        11   00      00    11      101        1001       11  101     
                                                      101   01        001 10110 1001       11   00      00    11       101      10101       11  101     
                    Q - Quit                          101   01       100  10001  101       11   00      00    11        110111100111        11  101     
                                                      101   01       111   1111  111       11   00      00    11          111111  111       11  101     
                                                      101   01                             11   00      00    11                            11  101     
                                                      101  101                             11   00      00    11                            11  101     
                                                      101   11                             01   00      00    10                            11  101     
                                                      101  10011                         11011  00      00   11011                        11011 101     
                                                      10111111011111111111111111111111111001101100      0011111100111111111111111111111111001101101     
                                                      10001 101                           11  1001      10011 101                          01 10001     
                                                       1001101                             1111001      10011101                           1011101      
                                                        1100011111111111111111111111111111110001          100001111111111111111111111111111100011                                                                           
                                                          11111111111111111111111111111111111               111111111111111111111111111111111                                                                                                                                                                                         
                                                       
</sub>



