Please pardon the name of this repository. This is done in Python, not C++

In my free time I wanted to improve my coding skills by making some graphics in OpenGL, which is the same library used in Blender & Rockstar Games & most games not in DirectX.

I originally started in the apex mother language of C++ and all I could have done was a spinning color pyramid that has the colors of the Blocks in Mario Kart 64.

I wanted to go above that and do more, but I noticed that I was just hitting massive roadblocks in C++ and I had limited time. 

I had to bite the bullet & suck it up.

I had to use Python to do anything more. If I wanted to progress in doing Vertex Shaders & Fragment Shaders, I had to suck up my pride and resort to an easier language like Python.

And I feel like I'm making massive gains in my comprehension of OpenGL by using Python. Finally not stuck for now. Everything is ongoing, I'm having a great time, I want to make something more substantial with physics & movement & so forth. With the great PyOpenGL Library, the calls are mostly identical to C++'s GLUT/GLFW/OpenGL libaries!!!

What's beautiful about Python is that I can focus on the algorithm, then always port it back to C++ when I figured out how to do things in Python. Without the Python step, I would be going nowhere, or creepily slow as others figure things out in that same time.

And that's a workflow I've always championed. Use Python when necessary, despite it's reputation as not "low-level" or cool or "close to the metal".

Thanks Python!

I will admit that when I started I was letting the Gordon-Ramsay Sheldon Cooper type elitists get to me with the attitude of "YOU'RE NOT A REAL ENGINEER IF YOU'RE NOT PROGRAMMING A VIDEO GAME IN ASSEMBLY!!!! YOU'RE AN IMPOSTOR WHO DOESN'T BELONG HERE & WORKS ON SOMETHING ELSE". Then I was extremely stupid enough to have this attitude to a lesser extent to others, which is why I was reluctant to even use Python for this task in the workflow.

![](images/1_pyramid_python_smaller.gif)

What you see here is an ongoing process. I figured out how to add more than 1 shape here with a API function called glDrawElementsInstanced. By doing this, the gl_InstanceID variable in the vertex Shader can be used to differentiate between the different instances (this variable is not a uniform variable passed down from the program).

I REALLY WANT TO HAVE THIS do Physics and bounce off each other, and there's various approaches one can take to do this. I'm trying to figure this all out. Should this be done on a compute GPU shader, or in the program as variables passed down. If this is never done, it's all good. This is something for me to incrementally dip into when I want to be challenged or when I feel a little rusty, and I ain't talking about the language Rust.

![](images/2_pyramid_multiple_python_smaller.gif)

![](images/1_pyramid_python_code.png)

