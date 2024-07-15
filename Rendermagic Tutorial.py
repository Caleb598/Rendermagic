import tkinter as tk

class TutorialWindow:
    def __init__(self, master, tutorial_steps):
        self.master = master
        self.tutorial_steps = tutorial_steps
        self.current_step = 0

        self.text = tk.Text(master, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
        self.text.pack(pady=20)
        self.show_current_step()

        self.prev_button = tk.Button(master, text="Previous", command=self.show_previous_step)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(master, text="Next", command=self.show_next_step)
        self.next_button.pack(side=tk.RIGHT, padx=10)

    def show_current_step(self):
        current_text = self.tutorial_steps[self.current_step]
        self.text.config(state=tk.NORMAL)  # Enable editing temporarily
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, current_text)
        self.text.config(state=tk.DISABLED)  # Disable editing again

    def show_previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()

    def show_next_step(self):
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self.show_current_step()

def main():
    tutorial_steps = [
        "Welcome to Rendermagic. Rendermagic is a 3D making software that can fastly render 3D scenes, both basic and complex. In this tutorial, you will learn how to use Rendermagic and make your own 3D scenes with them.",
        "Note on Rendermagic: Rendermagic is highly technical and it requires coding and programming in order to make edits to your scenes. It does not come with an user interface. You can use this tutorial for help or future reference.",
        "Getting Started \n\nWhen you first open Rendermagic, it will show a basic, rendered scene. It will show the elapsed render time in the console. For example: 00:00.18.",
        "Making Edits \n\nThis is now where this tutorial delves deep in the features of Rendermagic and how to make edits to the example scene when you first open Rendermagic.",
        "Changing the Background Color \n\nYou can change the background color by modifying the RGB values with this code: background_color = [1.0, 1.0, 1.0]",
        "Changing the Camera Properties \n\nYou can change the camera properties by modifying these lines of code: \n\ncamera_pos = [5, 5, 5]\n\ncamera_rot = [0, 0, 0]",
        "Changing Light Position and Intensity \n\nYou can change the position and intensity of a light by modifying these lines of code: \n\nlight1_position = [5.0, 5.0, 5.0, 20.0] \n\nThe first three values are the X, Y and Z positions of the light and the fourth value is the intensity of the light.",
        "Changing A Light's Colors \n\nYou can change a light's ambient, diffuse and specular colors by modifying these lines of code: \n\nlight1_ambient = [0.2, 0.2, 0.2, 1.0] \n\nlight1_diffuse = [0.8, 0.8, 0.8, 1.0] \n\nlight1_specular = [1.0, 1.0, 1.0, 1.0]",
        "Duplicating and Deleting Lights \n\nYou can duplicate lights by copying and pasting the four lines of the light code which include the light's position, intensity and its ambient, diffuse and specular colors. You will have to replace the original number of the light with the next ascending number. For example, if you have light1 and have a recently added light, you would rename it to light2. \n\nTo delete lights, you would just simply delete the four lines of code for the light.",
        "Types of Objects in Rendermagic \n\nThere are six types of objects in Rendermagic: cubes, spheres, cylinders, cones, planes and tori.",
        "Modifying Objects in Rendermagic \n\nYou can modify the position, rotation, size and color of an object by modifying this line of code. For example: \n\ncube1 = GameObject([0, 0, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0, 1.0]) \n\n The first set of brackets is for the position, the second set of brackets is for the rotation, the third set of brackets is for the size and the fourth set of brackets is for the color.",
        "Duplicating and Deleting Objects \n\nYou can duplicate and delete objects in Rendermagic by copying and pasting this line and rename the number at the end of the shape to the next number. For example, cube1 would be renamed to cube2. \n\ncube1 = GameObject([0, 0, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0, 1.0])",
        "Animation in Rendermagic \n\nThe next part on this tutorial focuses on animation in Rendermagic and how to animate certain things.",
        "Animating Objects \n\nYou can animate objects by adding a keyframe to it and then having a second keyframe, for example: \n\ncube2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[0, 0, -4], scale=[1.0, 1.0, 1.0], color=[0.8, 0.0, 0.0, 1.0]) \n\ncube2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[0, 0, 0], scale=[1.0, 1.0, 1.0], color=[1.0, 0.0, 0.0, 1.0])",
        "Animating Objects Continued \n\nWhen animating, you also need to modify this line to include all your objects. For example: \n\nfor obj in [torus1, torus2, plane1, plane2, cone1, cone2, cylinder1, cylinder2, sphere1, sphere2, cube1, cube2]: \n\nInclude all your objects into the lines of code where it says for obj in.",
        "Updating the Draw Object Function \n\nAlong the lines of updating objects, make sure you also update this chunk of code, too: \n\nif obj == torus1 or obj == torus2: \n\ndraw_realistic_torus([0, 0, 0], inner_radius=0.2, outer_radius=0.5, color=obj.color) \n\nelif obj == plane1 or obj == plane2: \n\ndraw_2d_plane(size=2.0, color=obj.color) \n\nelif obj == cone1 or obj == cone2: \n\ndraw_realistic_cone([0, 0, 0], radius=0.5, height=1.0, color=obj.color) \n\nelif obj == cylinder1 or obj == cylinder2: \n\ndraw_realistic_cylinder([0, 0, 0], radius=0.5, height=1.0, color=obj.color) \n\nelif obj == sphere1 or obj == sphere2: \n\ndraw_realistic_sphere([0, 0, 0], radius=0.5, color=obj.color) \n\nelif obj == cube1 or obj == cube2: \n\ndraw_realistic_cube([0, 0, 0], color=obj.color)",
        "Animating Lights \n\nYou can animate lights just like animating objects by adding a keyframe to it and then having a second keyframe, for example: \n\nlight1.add_keyframe(frame=0, position=[5.0, 5.0, 5.0, 20.0], ambient=[0.2, 0.2, 0.2, 1.0], diffuse=[0.8, 0.8, 0.8, 1.0], specular=[1.0, 1.0, 1.0, 1.0]) \n\nlight1.add_keyframe(frame=50, position=[-5.0, -5.0, -5.0, 20.0], ambient=[0.1, 0.1, 0.1, 1.0], diffuse=[0.5, 0.5, 0.5, 1.0], specular=[0.8, 0.8, 0.8, 1.0])",
        "Rendering Images \n\nYou can render images in Rendermagic by modifying the default code for rendering. The default code for rendering in Rendermagic is rendering animations. If you just want to render one single frame, you can remove this part of code: \n\n# Increment the current frame \n\ncurrent_frame += 1 \n\nAlso remove the last chunk of the code below that, but don't go down to the def save_frame_to_disk function.",
        "Rendering Images Continued \n\nReplace the deleted code with this code: \n\n# Print the current frame and render time if not already printedif current_frame <= end_frame and not render_time_printed: \n\n(line for printing out the value of the render time for the designated frame) \n\nrender_time_printed = True",
        "Rendering Animations \n\nYou can render animations by restoring the default code for rendering and running the code as so.",
        "Changing the Start and End Frame of Animations \n\nYou can modify the start of the animation and the end of the animation by modifying these lines of code: \n\ncurrent_frame = 0 \n\nend_frame = 50",
        "Changing the Resolution for Rendering \n\nYou can change the resolution or size of your renders by modifying these lines of code: \n\nwindow_width = 1920 \n\nwindow_height = 1080",
        "Exporting Animations \n\nOne of the features of Rendermagic is the power to export animations as mp4s. You can take your mp4 and leave it the way it is or you can put it into a video editor and play around with it, there. You can also change the frames per second of the mp4 by modifying this line of code: \n\nframes_per_second = 24.0",
        "Thank You for Reading This Tutorial \n\nNow that you've learned how to use Rendermagic, go out and make something cool! Get rendering!",
    ]

    root = tk.Tk()
    root.title("Rendermagic Tutorial")

    tutorial_window = TutorialWindow(root, tutorial_steps)

    root.mainloop()

if __name__ == "__main__":
    main()
