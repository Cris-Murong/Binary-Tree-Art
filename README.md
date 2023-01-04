# Binary Tree Art

Generate a .jpg file of a random binary tree.

## Requirement 
- python3.11 +
- PIL(Pillow) 9.3.0 +

## Execute

```
> python main.py [option]
```
**Noticed: Images will be saved under the /img folder**

Argparse Option:
    `- num`: numbers of the image.
    `- layer`: layers of the binary tree.



## Examples
<image src="img/readme_img/0.jpg" height = 200>
<image src="img/readme_img/1.jpg" height = 200>
<image src="img/readme_img/2.jpg" height = 200>


## Details 

#### Tree_Node(class)

Attributes:
```py
size: float # the ratio to the parent node's length (size : 1).
angle: float # the direct derived from the parent node's direction
layer: int
left: "Tree_Node"
right: "Tree_Node"
end: bool
```

When printing a `Tree_Node`, its structure will be displayed:
``` py
generator = Tree_Generator()
node: Tree_Node = generator.generate(2)
print(node)
```
```
|size:1
|angle:0
|left:
|     |size:0.746
|     |angle:-18.768      
|     |left:
|     |     |size:0.648   
|     |     |angle:-18.96
|     |     |left: END
|     |     |right: END
|     |right:
|     |     |size:0.612
|     |     |angle:13.32
|     |     |left: END
|     |     |right: END
|right:
|     |size:0.832
|     |angle:16.597
|     |left:
|     |     |size:0.854
|     |     |angle:-17.272
|     |     |left: END
|     |     |right: END
|     |right:
|     |     |size:0.719
|     |     |angle:22.779
|     |     |left: END
|     |     |right: END
```
#### Exponential()

The `Exponential` is used to model the uneven change of color / size / width ...
$$
y = dn^{cx - a} + b
$$

Attributes:
``` py
base: float # n
x_shift: float # a
y_shift: float # b
x_stretch: float # c
y_stretch: float # d
```
Properties:
``` py
get_y() # return the y of the given `x`
```

#### Tree_Generator()

The `Tree_Generator` is used to generate a random binary tree.

Attributes:
``` py
size_base: float # `.base` of `Exponential` for size
size_roof: float # `.y_shift` of `Exponential` for size
size_floor: float # `.y_stretch` of `Exponential` for size
brunching_angle: float # angles derived away from the parent node's `.angle`
vary_size: float # the variation of `.size`
vary_angle: float # the variation of `.angle`
end_rate: float # the chance to stop brunching
```

Properties:
``` py
generate() # return a base `Tree_Node` of a random tree.
_brunching() # brunching the given `base_node`
```

#### Tree_Image()

Attributes:
``` py
image_size: tuple[int] # pixels of the .jpg file (x, y)
layer: int # layers or the `Tree_Node`
width_base: float
color_base: float # `.base` of `Exponential` for width / color
width_roof: float
color_roof: float # `.y_shift` of `Exponential` for width / color
width_floor: float
color_floor: float # `.y_stretch` of `Exponential` for width / color
```

Properties:
``` py
clear() # create the new `self.image` and `self.draw_img`
draw_node() # draw the given `node` on the `self.draw_img`
save_image() # save the `self.image` as a .jpg file under the given `path`
```
