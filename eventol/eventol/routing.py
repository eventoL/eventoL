"""
   Routing Module with all Demultiplexers and channel_routing for djnago-channels
"""
# pylint: disable=missing-docstring

from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class

"""
from links.bindings import LinkBinding, TagBinding, LinkTagBinding


class APIDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'links': LinkBinding.consumer,
        'tags': TagBinding.consumer,
        'linktags': LinkTagBinding.consumer,
    }

    def connection_groups(self, **kwargs):
        return ['link-updates', 'tag-updates', 'linktag-updates']


class LinkTagDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'linktags': LinkTagBinding.consumer
    }

    def connection_groups(self, **kwargs):
        return ['linktag-updates']


class LinkDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'links': LinkBinding.consumer
    }

    def connection_groups(self, **kwargs):
        return ['link-updates']


class TagDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'tags': TagBinding.consumer
    }

    def connection_groups(self, **kwargs):
        return ['tag-updates']


# pylint: disable=invalid-name
channel_routing = [
    route_class(APIDemultiplexer, path='^/updates/$'),
    route_class(LinkTagDemultiplexer, path='^/updates/linktags/$'),
    route_class(LinkDemultiplexer, path='^/updates/links/$'),
    route_class(TagDemultiplexer, path='^/updates/tags/$'),
]
"""
channel_routing = []
