# Binary Tree Art

Generate a .jpg file or a series of .jpg sequences of binary trees.

## Requirement 
- python3.11 +
- PIL(Pillow) 9.3.0 +

## Running

```
> python main.py [-h] [-render_to] [-load_from] [-dump_to] [-seq_len] mode
```


Positional arguments:
| argument | description                                     |
| -------- | ----------------------------------------------- |
| mode     | img(generate an image)/seq(generate a sequence) |

Options:

| arguments  | description                                                   |
| ---------- | ------------------------------------------------------------- |
| -h         | show this help message and exit                               |
| -render_to | address to save rendered image to (default: 'img/sample.jpg') |
| -load_from | address to load .json file from                               |
| -dump_to   | address to dump .json file to                                 |
| -seq_len   | length of sequence [only useful at seq mode]                  |

**Noticed: Images will be saved under the /img folder**

## Examples
<image src="readme_file/color1.jpg" height = 200>

<video width="320" height="240" controls>
    <source src="readme_file/demo.mp4" type="video/mp4">
</video>
