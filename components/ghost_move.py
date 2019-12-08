import random

from pysmile.colors import Colors
from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2

from components.move_component import MoveComponent
from events.change_tile import PacmanChangeTileEvent
from events.debug_line import DrawDebugLineEvent
from objects.base_cell import Meta
from objects.path_finder import Afinder


class GhostMoveComponent(Component):
    def __init__(self, field, speed, find_target, color=None):
        super().__init__()
        self.field = field
        self.speed = speed
        self.entity = None
        self.direction = None
        self.path_finder = Afinder(field)
        self.path = None
        self.current_vert = None
        self.find_target = find_target
        if not color:
            self.debug_line_color = Colors.from_rgb(*[random.randint(0, 255) for _ in range(3)]).to_float()
        else:
            self.debug_line_color = color.to_float()

    def update(self, _):
        trans = self.entity.get_component(TransformComponent)
        if not trans:
            return
        if self.path is not None and self.current_vert is not None:
            if self.path[self.current_vert] == trans.pos or self.direction is None:
                self.current_vert += 1
                if self.current_vert >= len(self.path):
                    self.path = None
                    return
                self.update_direction(trans.pos, self.path[self.current_vert])

            trans.position += self.direction * self.speed

    def update_direction(self, pos, tpos):
        new_vec = tpos - pos
        if new_vec.x != 0:
            self.direction = Vector2(1 if new_vec.x > 0 else -1, 0)
        elif new_vec.y != 0:
            self.direction = Vector2(0, 1 if new_vec.y > 0 else -1)

    def update_target(self, event):
        target_pos = self.find_target(event.pacman, self.field)

        trans = self.entity.get_component(TransformComponent)
        self.path = self.path_finder.find_path(trans.pos, target_pos)
        self.current_vert = 0
        self.update_direction(trans.pos, self.path[self.current_vert])
        self.entity.event_manager.trigger_event(
            DrawDebugLineEvent([v + Vector2(16, 16) for v in [trans.pos] + self.path + [target_pos]],
                               self.debug_line_color))

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)
        self.entity.event_manager.unbind(PacmanChangeTileEvent, self.update_target)

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(UpdateEvent, self.update)
        self.entity.event_manager.bind(PacmanChangeTileEvent, self.update_target)