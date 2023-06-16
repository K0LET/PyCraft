from ursina import *
from ursina import curve
import player


gui = Ursina()


class world:
    def __init__(self):
        self.sky = Sky()
        self.block = Block()
        self.block.disable()
        self.p = player
        self.player = self.p.Player()
        # self.world_space: list[Block] = []

    # def update_world(self):
    #     return self.world_space
    #
    # def add_to_world_space(self, block):
    #     self.world_space.append(block)
    #
    # def remove_from_world_space(self, block):
    #     self.world_space.remove(block)

    def disable(self):
        self.player.disable()
        self.sky.disable()

    def enable(self):
        self.player.enable()
        self.sky.enable()

    def build_world(self):
        for z in range(-20, 20):
            for x in range(-20, 20):
                Block(position=(x, 0, z))

    # def add_block(self, x=0, y=0, z=0):
    #     Block(position=(x, y, z))
    #     self.add_to_world_space(Vec3(x, y, z))

    # def world_input(self, key):
    #     add_remove = self.block.input(key)
    #     if add_remove[0] == "added":
    #         self.add_to_world_space(add_remove[1])
    #     elif add_remove[0] == "destroyed":
    #         self.remove_from_world_space(add_remove[1])


class Block(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/block.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),  # sets the color (not transparent)
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                block = Block(position=self.position + mouse.normal)
                return "added", block

            if key == 'right mouse down':
                block = self
                destroy(self)
                return "destroyed", block
        return "MyNone", None


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture='assets/skybox.png',
            scale=150,
            double_sided=True
        )


class Camera(EditorCamera):
    def __init__(self, x=0, y=50, z=-120, rot_x=25, rot_y=0, rot_z=0, **kwargs):
        super().__init__(**kwargs)
        self.current_cam = None
        self.position = (x, y, z)
        self.rotation_x = rot_x
        self.rotation_y = rot_y
        self.rotation_z = rot_z

    def update_camera(self, cam_num, x=0, y=0, z=0, rot_x=25, rot_y=0, rot_z=0):
        self.current_cam = cam_num
        self.animate_position((x, y, z), duration=0.75, curve=curve.linear)
        self.animate_rotation((rot_x, rot_y, rot_z), duration=0.75, curve=curve.linear)


def update():
    w.block.test()


def main():
    global w
    w = world()
    w.build_world()
    gui.run()


if __name__ == "__main__":
    main()
