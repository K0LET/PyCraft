from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class Player:
    def __init__(self):
        self.fpc = FirstPersonController(scale=(1, 1, 1), position=(0, 0, 0))
        self.hand = Hand()

    def disable(self):
        self.fpc.disable()
        self.hand.disable()

    def enable(self):
        self.fpc.enable()
        self.hand.enable()

    def set_speed(self, speed):
        self.fpc.speed = speed

    def jump(self):
        self.fpc.jump()


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=load_texture('assets/arm_texture.png'),
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


class Client(Entity):
    def __init__(self, position, color):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=(1.25, 2.5, 1.25)
        )