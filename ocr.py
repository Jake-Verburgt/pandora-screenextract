import subprocess
import sys
import os
from re import findall

def threeline_format(string:str) -> bool:
    '''Just checks if input string is three lines'''
    if len(findall("\n", string.strip())) == 2:
        return True
    else:
        return False



def read_image(image_path:str, tesseract_path:str = "/usr/bin/tesseract") -> str:
    '''Simple wrapper around tesseract executable because pytessearct doesn't like my environment
    image_path -  Filepath tom an image
    tesseract_path - Path to tesseract exectuable
    returns  - string of text in the image
    '''
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"{image_path} not Found!")
    
    result = subprocess.run([tesseract_path, 
                             image_path,
                             "stdout"], capture_output=True, text = True)
    if result.returncode == 0:
        return result.stdout
    else:
        raise RuntimeError(f"Could not run Tesseact: {result.stderr}")

def main():
    image_path = sys.argv[1]
    text = read_image(image_path)
    print(text)

if __name__ == "__main__":
    main()

