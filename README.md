# Aztec Code generator
Aztec Code generator in Python


## Dependencies:  
PIL - Python Imaging Library (or Pillow)


## Usage:
```python
data = 'Aztec Code 2D :)'
aztec_code = AztecCode(data)
aztec_code.save('aztec_code.png', module_size=4)
```

This code will generate an image file "aztec_code.png" with the Aztec Code that contains "Aztec Code 2D :)" text.

![Aztec Code](https://1.bp.blogspot.com/-OZIo4dGwAM4/V7BaYoBaH2I/AAAAAAAAAwc/WBdTV6osTb4TxNf2f6v7bCfXM4EuO4OdwCLcB/s1600/aztec_code.png "Aztec Code with data")

```python
data = 'Aztec Code 2D :)'
aztec_code = AztecCode(data)
aztec_code.print_out()
```

This code will print out resulting 19x19 (compact) Aztec Code to the standard output.

```
      ##  # ## ####
 #   ## #####  ### 
 #  ##  # #   # ###
## #  #    ## ##   
    ## # #    # #  
## ############ # #
 ### #       ###  #
##   # ##### # ## #
 #   # #   # ##    
 # # # # # # ###   
    ## #   # ## ## 
#### # ##### ## #  
  # ##       ## ## 
 ##  ########### # 
  ##    # ##   ## #
     ## # ### #  ##
      ############ 
##   #     # ##   #
##  #    ## ###   #
```

## License:
Released under [The MIT License](https://github.com/delimitry/aztec_code_generator/blob/master/LICENSE).
