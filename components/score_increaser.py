from pysmile.component import Component
from pysmile.components.pygame_renderer import PyGameRendererComponent
from events.collect_grain import CollectSmallGrainEvent, CollectBigGrainEvent


class ScoreIncreaserComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None

    def increase(self, value):
        score = self.entity.get_component(PyGameRendererComponent)
        score.renderer.text = "{:03d}".format(int(score.renderer.text) + value)

    def collect_small_grain(self, _):
        self.increase(1)

    def collect_big_grain(self, _):
        self.increase(10)

    def removed(self):
        self.entity.event_manager.bind(CollectSmallGrainEvent, self.collect_small_grain)
        self.entity.event_manager.bind(CollectBigGrainEvent, self.collect_big_grain)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(CollectSmallGrainEvent, self.collect_small_grain)
        entity.event_manager.bind(CollectBigGrainEvent, self.collect_big_grain)
